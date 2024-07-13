from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Student, Exercise, Solution, Result


class StudentLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Student
        fields = ["username", "email"]


class StudentSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(source="user.password", write_only=True)
    first_name = serializers.CharField(
        source="user.first_name", required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        source="user.last_name", required=False, allow_blank=True
    )

    class Meta:
        model = Student
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_assistant",
            "phone_number",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "username": {"required": True},
        }

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError(
                "Email address already exists. Please use a different email."
            )
        return lower_email

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(
            username=user_data["username"].lower(),
            email=user_data["email"].lower(),
            password=user_data["password"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
        )
        student = Student.objects.create(
            user=user,
            is_assistant=validated_data.get("is_assistant", False),
            phone_number=validated_data.get("phone_number", None),
        )
        return student


class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "title", "difficulty_level"]


class ExerciseDetailSerializer(serializers.ModelSerializer):
    java_definition_url = serializers.SerializerMethodField()
    cpp_definition_url = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            "id",
            "title",
            "exercise_content",
            "java_definition_url",
            "cpp_definition_url",
            "difficulty_level",
        ]

    def get_java_definition_url(self, obj):
        request = self.context.get("request")
        if obj.java_definition:
            return request.build_absolute_uri(obj.java_definition.url)
        return None

    def get_cpp_definition_url(self, obj):
        request = self.context.get("request")
        if obj.cpp_definition:
            return request.build_absolute_uri(obj.cpp_definition.url)
        return None


class SolutionSerializer(serializers.ModelSerializer):
    exercise_id = serializers.IntegerField(write_only=True)
    solution_file = serializers.FileField(write_only=True)

    class Meta:
        model = Solution
        fields = ["exercise_id", "solution_file", "language"]

    def validate(self, attrs):
        exercise_id = attrs.pop("exercise_id")

        # Validate exercise exists
        try:
            exercise = Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            raise serializers.ValidationError("Exercise does not exist")

        # Get user from request
        user = self.context["request"].user

        # Ensure the user is a student
        if not hasattr(user, "student_profile"):
            raise serializers.ValidationError("User is not a student")

        student = user.student_profile

        attrs["exercise"] = exercise
        attrs["student"] = student
        return attrs

    def create(self, validated_data):
        solution = Solution.objects.create(
            student=validated_data["student"],
            exercise=validated_data["exercise"],
            solution_file=validated_data["solution_file"],
            language=validated_data["language"],
        )
        return solution


class ResultSerializer(serializers.ModelSerializer):
    reference_id = serializers.SerializerMethodField()
    solution_file = serializers.SerializerMethodField()

    class Meta:
        model = Result
        exclude = ["id", "student", "exercise", "solution"]

    def get_solution_file(self, obj):
        request = self.context.get("request")
        if obj.solution:
            return request.build_absolute_uri(obj.solution.solution_file.url)
        return None

    def get_reference_id(self, obj):
        return f"{obj.exercise.id}_{obj.student.user.username}_{obj.solution.id}"
