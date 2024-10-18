from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications import models as notifications_models
from apps.notifications import serializers as notifications_serializers
from apps.notifications.filters.notification_filter import NotificationFilter
from apps.translations import models as translation_models


class NotificationListView(APIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = NotificationFilter

    def get(self, request, *args, **kwargs):
        notification_query = notifications_models.UserNotification.objects.filter(
            user=request.user
        ).select_related(
            "notification_template__notification_category"
        ).prefetch_related(
            Prefetch(
                'notification_template__translations',
                queryset=translation_models.TranslationString.objects.filter(
                    language_id=request.user.language_id,
                ).select_related('language'),
                to_attr='prefetched_translations'
            ),
            Prefetch(
                'options',
                queryset=notifications_models.UserNotificationOption.objects.filter(user_notification__user=request.user),
                to_attr='prefetched_options'
            ),

        )

        notification_filterset = self.filterset_class(
            data=request.query_params,
            queryset=notification_query,
            request=request,
        )
        user_notification_serializer = notifications_serializers.UserNotificationSerializer(notification_filterset.qs, many=True)
        return Response(user_notification_serializer.data)


class NotificationDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('notification_id')
        notification = get_object_or_404(
            notifications_models.UserNotification.objects.filter(
                user=request.user
            ).select_related(
                "notification_template__notification_category"
            ).prefetch_related(
                Prefetch(
                    'notification_template__translations',
                    queryset=translation_models.TranslationString.objects.filter(
                        language_id=request.user.language_id,
                    ),
                    to_attr='prefetched_translations'
                ),
                Prefetch(
                    'options',
                    queryset=notifications_models.UserNotificationOption.objects.filter(
                        user_notification__user=request.user
                    ),
                    to_attr='prefetched_options'
                )
        ),
            pk=notification_id
        )

        user_notification_serializer = notifications_serializers.UserNotificationSerializer(notification)
        return Response(user_notification_serializer.data)