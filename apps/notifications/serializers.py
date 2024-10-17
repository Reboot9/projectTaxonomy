from rest_framework import serializers

from apps.notifications import models
from apps.translations.models import TranslationString


class NotificationCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NotificationCategory
        fields = ["name", "title"]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    notification_category = NotificationCategorySerializer(read_only=True)

    class Meta:
        model = models.NotificationTemplate
        fields = '__all__'



class UserNotificationSerializer(serializers.ModelSerializer):
    txt = serializers.SerializerMethodField()
    # notification_template = NotificationTemplateSerializer(read_only=True)
    class Meta:
        model = models.UserNotification
        fields = ['user', 'txt',]

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

