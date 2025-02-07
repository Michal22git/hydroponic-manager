from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegister, LoginView

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]