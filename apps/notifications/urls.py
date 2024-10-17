from django.urls import path
from apps.notifications import views as notifications_views

urlpatterns = [
    path('api/', notifications_views.NotificationListView.as_view(), name='notifications-list'),
    path('api/<int:notification_id>/', notifications_views.NotificationDetailView.as_view(), name='notifications-detail'),
]