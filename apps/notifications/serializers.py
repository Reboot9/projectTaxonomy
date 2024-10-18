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

        if notification_template and notification_template.prefetched_translations:
            translation = notification_template.prefetched_translations[0]
            txt = translation.text
        else:
            txt = obj.notification_template.txt

        notification_options = obj.prefetched_options
        # Create dict which contains field_id and text for replacement
        field_replacements = {option.field_id: option.txt for option in notification_options}

        # Replace text with Notification Option values
        formatted_text = txt
        for key, value in field_replacements.items():
            formatted_text = formatted_text.replace(f'{{{key}}}', value)

        return formatted_text

    def get_language(self, obj):
        notification_template = obj.notification_template

        if notification_template and notification_template.prefetched_translations:
            translation = notification_template.prefetched_translations[0]
            lang = translation.language.name
        else:
            lang = Language.objects.get(pk=Language.get_default_pk()).name

        return lang
