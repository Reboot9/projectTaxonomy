from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

User = get_user_model()


class NotificationCategory(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification_category'


class NotificationTemplate(models.Model):
    notification_category = models.ForeignKey(NotificationCategory, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    txt = models.CharField(max_length=255, blank=True, null=True)
    translations = GenericRelation('translations.TranslationString')

    class Meta:
        managed = False
        db_table = 'notification_template'


class UserNotification(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='notifications')
    notification_template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING, blank=True, null=True)
    notification_type = models.IntegerField(default=1)
    status = models.IntegerField(default=0,)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_notification'


class UserNotificationOption(models.Model):
    user_notification = models.ForeignKey(UserNotification, models.DO_NOTHING, blank=True, null=True, related_name='options')
    field_id = models.IntegerField(blank=True, null=True)
    txt = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_notification_option'


class UserNotificationSetting(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='notification_settings')
    notification_template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING, blank=True, null=True)
    system_notification = models.IntegerField(default=1)
    push_notification = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'user_notification_setting'