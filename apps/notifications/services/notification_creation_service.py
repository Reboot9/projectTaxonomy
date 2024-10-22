from apps.notifications import models as notifications_models


class NotificationCreationService:
    @staticmethod
    def _get_user_notification_setting(user, notification_template):
        """
        Retrieve user notification setting for specified notification template.
        If the settings is not found, return default settings.
        """
        user_setting = user.notification_settings.filter(
            notification_template=notification_template
        ).values('push_notification', 'system_notification').first()

        if not user_setting:
            user_setting = {
                'push_notification': 1,
                'system_notification': 1,
            }

        return user_setting

    def create_notification_if_allowed(self, notification_template, notification_type, user):
        """
        Create notification for the user based on their notification settings.
        If the setting doesn't exist, both system and push notifications can be created.
        """

        user_setting = self._get_user_notification_setting(user, notification_template)

        # Notification type mapping to corresponding settings key
        notification_type_key = {
            2: 'push_notification',
            1: 'system_notification'
        }.get(notification_type)

        # Determine notification type based on user settings
        if notification_type_key and user_setting.get(notification_type_key, False):

            return notifications_models.UserNotification.objects.create(
                user=user,
                notification_template=notification_template,
                notification_type=notification_type,
                status=0,
            )

        # Notification was not created
        return None
