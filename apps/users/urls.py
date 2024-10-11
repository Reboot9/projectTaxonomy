from django.urls import path
from apps.users import views as users_views

urlpatterns = [
    path('api/register/', users_views.RegisterView.as_view(), name='register'),
    path('api/login/', users_views.LoginView.as_view(), name='login'),
]