from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Student, Exercise, Solution


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
    class Meta:
        model = Exercise
        fields = [
            "id",
            "title",
            "exercise_content",
            "java_definition",
            "cpp_definition",
            "difficulty_level",
        ]


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["student", "exercise", "solution_file"]

    def validate_solution_file(self, value):
        # Ensure the file size is within the limit
        max_size = 1 * 1024 * 1024  # 1MB
        if value.size > max_size:
            raise serializers.ValidationError("File size must be under 1MB")
        return value

    def create(self, validated_data):
        student = self.context["request"].user.student_profile
        solution = Solution.objects.create(
            student=student,
            exercise=validated_data["exercise"],
            solution_file=validated_data["solution_file"],
        )
        return solution
