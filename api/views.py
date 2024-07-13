from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (
    StudentSignupSerializer,
    StudentLoginSerializer,
    ExerciseDetailSerializer,
    ExerciseListSerializer,
    SolutionSerializer,
    ResultSerializer,
)
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.utils import IntegrityError as DjangoIntegrityError
from core.models import Exercise, Result


@api_view(["POST"])
@permission_classes([AllowAny])
def student_login(request):
    username_or_email = request.data.get("username_or_email")
    password = request.data.get("password")

    # Try to authenticate user using username first
    user = authenticate(request, username=username_or_email, password=password)

    if not user:
        # If username authentication fails, try to authenticate using email
        try:
            user_with_email = User.objects.get(email=username_or_email)
            user = authenticate(
                request, username=user_with_email.username, password=password
            )
        except User.DoesNotExist:
            pass

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        student_profile = user.student_profile
        serializer = StudentLoginSerializer(instance=student_profile)
        return Response({"token": token.key, "user": serializer.data})

    # Authentication failed
    return Response(
        {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def student_signup(request):
    serializer = StudentSignupSerializer(data=request.data)

    if serializer.is_valid():
        try:
            # Save the student object
            student = serializer.save()

            # Return success response
            return Response(
                {"message": "Student created successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except DjangoIntegrityError as e:
            # Handle unique constraint error
            if "UNIQUE constraint failed: auth_user.username" in str(e):
                return Response(
                    {
                        "error": "Username already exists. Please choose a different username."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif "UNIQUE constraint failed: auth_user.email" in str(e):
                return Response(
                    {
                        "error": "Email address already exists. Please use a different email."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Return validation errors if serializer is not valid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def exercise_list(request):
    difficulty_level = request.query_params.get("dfl")
    if difficulty_level is None:
        exercises = Exercise.objects.filter(is_visible=True)
    else:
        exercises = Exercise.objects.filter(
            difficulty_level=difficulty_level, is_visible=True
        )
    serializer = ExerciseListSerializer(exercises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def exercise_detail(request, pk):
    try:
        exercise = Exercise.objects.get(pk=pk)
    except Exercise.DoesNotExist:
        return Response(
            {"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ExerciseDetailSerializer(exercise, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def upload_solution(request):
    serializer = SolutionSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Solution uploaded successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_results_by_exercise_and_student(request, pk):
    user = request.user

    results = Result.objects.filter(exercise__id=pk, student__user=user)

    serializer = ResultSerializer(results, context={"request": request}, many=True)

    return Response(serializer.data)
