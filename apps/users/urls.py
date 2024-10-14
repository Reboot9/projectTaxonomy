from django.urls import path
from apps.users import views as users_views

urlpatterns = [
    path('api/', users_views.UserListView.as_view(), name='user-list'),
    path('api/register/', users_views.RegisterView.as_view(), name='register'),
    path('api/login/', users_views.LoginView.as_view(), name='login'),
    path('api/<int:user_id>/', users_views.UserObtainView.as_view(), name='user-detail'),
]