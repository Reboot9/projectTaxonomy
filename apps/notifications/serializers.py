from django.contrib.contenttypes.models import ContentType
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
    txt_1 = serializers.SerializerMethodField()
    # notification_template = NotificationTemplateSerializer(read_only=True)
    class Meta:
        model = models.UserNotification
        fields = ['user', 'txt', 'txt_1']

    def get_txt(self, obj):
        translation = TranslationString.objects.filter(
            # content_type=ContentType.objects.get_for_model(models.NotificationTemplate),
            # object_id=obj.notification_template.pk,
            language=obj.user.language
        ).first()

        return translation.text

    def get_txt_1(self, obj):
        notification_options = models.UserNotificationOption.objects.filter(user_notification=obj)

        field_replacements ={}#  {key: val for key, val in notification_options}
        for option in notification_options:
            field_replacements[option.field_id] = option.txt
        print(field_replacements)

        formatted_text = obj.notification_template.txt
        for key, value in field_replacements.items():
            formatted_text = formatted_text.replace(f'{{{key}}}', value)
        print(formatted_text)

        return formatted_text