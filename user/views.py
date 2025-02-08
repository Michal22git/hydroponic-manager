from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer


class UserRegister(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    create:
    Register a new user.
    * Requires username, email, and matching passwords
    * Validates password strength
    * Checks for unique username and email
    """
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """
    API endpoint for user authentication.
    
    create:
    Obtain JWT token pair.
    * Requires username and password
    * Returns access and refresh tokens
    * Access token includes user details
    """
    
    serializer_class = MyTokenObtainPairSerializer
