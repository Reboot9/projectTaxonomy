from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications import serializers as notifications_serializers
from apps.notifications.filters.notification_filter import NotificationFilter
from apps.notifications.paginations import CustomPageNumberPagination
from apps.notifications.services.notification_query_service import NotificationQueryService


class NotificationListView(APIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = NotificationFilter
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        notification_query = NotificationQueryService.get_user_notifications(request.user)

        notification_filterset = self.filterset_class(
            data=request.query_params,
            queryset=notification_query,
            request=request,
        )

        filtered_queryset = notification_filterset.qs
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

        user_notification_serializer = notifications_serializers.UserNotificationSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(user_notification_serializer.data)


class NotificationDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('notification_id')
        notification = NotificationQueryService.get_user_notifications_by_id(request.user, notification_id)

        user_notification_serializer = notifications_serializers.UserNotificationSerializer(notification)
        return Response(user_notification_serializer.data)