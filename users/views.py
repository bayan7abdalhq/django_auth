from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, User
from .serializers import LoginSerializer, StudentSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

class StudentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response({
            "status": True,
            "data": serializer.data
        })

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            new_serializer = StudentSerializer(student)
            return Response({
                "status": True,
                "message": "Student created successfully!",
                "data": new_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.errors
            })
        username = serializer.data['username']
        password = serializer.data['password']

        user_obj = authenticate(username=username, password=password)
        if user_obj:
            token, _ = Token.objects.get_or_create(user=user_obj)
            return Response({
                "status": True,
                "data": {'token': str(token)}
            })
        return Response({
            "status": False,
            "data": {},
            "message": "invalid credentials"
        })
class SignupView(APIView):
    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response({'message': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

