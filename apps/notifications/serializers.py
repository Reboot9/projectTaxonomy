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
        translation = TranslationString.objects.filter(
            # content_type=ContentType.objects.get_for_model(models.NotificationTemplate),
            # object_id=obj.notification_template.pk,
            language=obj.user.language
        ).first()

        notification_options = models.UserNotificationOption.objects.filter(user_notification=obj)

        # Create dict which contains field_id and text for replacement
        field_replacements = {option.field_id: option.txt for option in notification_options}

        # Replace text with Notification Option values
        formatted_text = translation.text
        for key, value in field_replacements.items():
            formatted_text = formatted_text.replace(f'{{{key}}}', value)

        return formatted_text

