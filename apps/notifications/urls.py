from django.urls import path
from apps.notifications import views as notifications_views

urlpatterns = [
    path('api/', notifications_views.NotificationListView.as_view(), name='notifications-list'),
    # path(),
]