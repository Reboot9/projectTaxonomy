from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications import models, serializers
from apps.translations.models import TranslationString


class NotificationListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # project_id = kwargs.get('project_id')
        # print(project_id)
        notification_query = models.UserNotification.objects.filter(
            user=request.user
        ).select_related(
            "notification_template"
        ).prefetch_related(
            Prefetch(
                'notification_template__translations',
                queryset=TranslationString.objects.filter(
                    language_id=request.user.language_id,
                ),
                to_attr='prefetched_translations'
            ),
            Prefetch(
                'options',
                queryset=models.UserNotificationOption.objects.filter(user_notification__user=request.user),
                to_attr='prefetched_options'
            )
        )

        user_notification_serializer = serializers.UserNotificationSerializer(notification_query, many=True)
        return Response(user_notification_serializer.data)


class NotificationDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('notification_id')
        notification = get_object_or_404(
            models.UserNotification.objects.filter(
                user=request.user
            ).select_related(
                "notification_template"
            ).prefetch_related(
                Prefetch(
                    'notification_template__translations',
                    queryset=TranslationString.objects.filter(
                        language_id=request.user.language_id,
                    ),
                    to_attr='prefetched_translations'
                ),
                Prefetch(
                    'options',
                    queryset=models.UserNotificationOption.objects.filter(
                        user_notification__user=request.user
                    ),
                    to_attr='prefetched_options'
                )
        ),
            pk=notification_id
        )

        user_notification_serializer = serializers.UserNotificationSerializer(notification)
        return Response(user_notification_serializer.data)