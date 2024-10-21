from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from apps.notifications import models as notifications_models
from apps.translations import models as translation_models


class NotificationQueryService:
    @staticmethod
    def _build_notification_query(user):
        """
        Private method to construct base query for user notifications,
        with related templates, categories, translations and options.
        """
        return notifications_models.UserNotification.objects.filter(
            user=user
        ).select_related(
            "notification_template__notification_category"
        ).prefetch_related(
            Prefetch(
                'notification_template__translations',
                queryset=translation_models.TranslationString.objects.filter(
                    language_id=user.language_id,
                ).select_related('language'),
                to_attr='prefetched_translations'
            ),
            Prefetch(
                'options',
                queryset=notifications_models.UserNotificationOption.objects.filter(
                    user_notification__user=user),
                to_attr='prefetched_options'
            ),
        )


    @staticmethod
    def get_user_notifications(user):
        """
        Fetch a queryset for user notifications.
        """
        return NotificationQueryService._build_notification_query(user)

    @staticmethod
    def get_user_notifications_by_id(user, notification_id):
        """
        Fetch a single user notification by id.
        """
        return get_object_or_404(
            NotificationQueryService._build_notification_query(user),
            pk=notification_id
        )