from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch, Subquery, OuterRef, F
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications import models, serializers
from apps.translations.models import TranslationString


class NotificationListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
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
