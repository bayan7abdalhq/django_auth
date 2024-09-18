from django.urls import path
from .views import LoginView, StudentView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('student/', StudentView.as_view(), name='student')
]
