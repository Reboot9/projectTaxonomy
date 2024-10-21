from rest_framework import serializers

from apps.notifications import models as notifications_models
from apps.translations.models import Language


class NotificationCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = notifications_models.NotificationCategory
        fields = ["name", "title"]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    notification_category = NotificationCategorySerializer(read_only=True)

    class Meta:
        model = notifications_models.NotificationTemplate
        fields = ['notification_category', 'name', 'txt',]



class UserNotificationSerializer(serializers.ModelSerializer):
    txt = serializers.SerializerMethodField()
    notification_category = NotificationCategorySerializer(
        read_only=True,
        source="notification_template.notification_category"
    )
    language = serializers.SerializerMethodField()

    class Meta:
        model = notifications_models.UserNotification
        fields = ['id', 'user', 'language', 'notification_type', 'status', 'txt', 'notification_category', 'created']

    def get_txt(self, obj):
        notification_template = obj.notification_template
        translations = getattr(notification_template, 'prefetched_translations', [])
        if notification_template and translations:
            translation = notification_template.prefetched_translations[0]
            txt = translation.text
        else:
            txt = obj.notification_template.txt

        notification_options = getattr(obj, 'prefetched_options', {})
        # Create dict which contains field_id and text for replacement
        field_replacements = {option.field_id: option.txt for option in notification_options}

        # Replace text with Notification Option values
        for key, value in field_replacements.items():
            txt = txt.replace(f'{{{key}}}', value)

        return txt

    def get_language(self, obj):
        notification_template = obj.notification_template
        translations = getattr(notification_template, 'prefetched_translations', [])
        if translations:
            return translations[0].language.name

        # Return default Language
        return Language.objects.get(pk=Language.get_default_pk()).name
