from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.notifications import models, serializers
from apps.translations.models import TranslationString


class NotificationListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        preferred_user_language_id = request.user.language_id


        # notification_template = models.NotificationTemplate.objects.prefetch_related(
        #     Prefetch(
        #         'translation_string',
        #         queryset=TranslationString.objects.filter(
        #             language_id=request.user.language_id),
        #         to_attr='prefetched_translations'
        #     )
        # )
        #
        # notification_template_serializer = serializers.NotificationTemplateSerializer(
        #     notification_template, context={'preferred_user_language_id': preferred_user_language_id}
        # )
        query = models.UserNotification.objects.filter(user=request.user).select_related()
        # .prefetch_related(
        #     Prefetch(
        #         'translation_string',
        #         queryset=TranslationString.objects.filter(
        #             language_id=request.user.language_id),
        #         to_attr='prefetched_translations'
        #     )
        # )

        user_notification_serializer = serializers.UserNotificationSerializer(query, many=True)

        #print(user_notification_serializer.data)
        return Response(user_notification_serializer.data)
