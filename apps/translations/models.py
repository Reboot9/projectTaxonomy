from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language'

    @classmethod
    def get_default_pk(cls):
        language_obj, created = cls.objects.get_or_create(name='en')

        return language_obj.id

FIELD_CHOICES = [
    ("name", 1),
    ("title", 2),
    ("description", 3),
    ("text", 4),
    ("question", 5),
    ("answer", 6),
    ("additional", 7),
]

class TranslationString(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.IntegerField()
    related_item = GenericForeignKey("content_type", "object_id")
    translation_field_id = models.IntegerField(
        choices=FIELD_CHOICES,
        default=1,
    )
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=255)

    class Meta:
        managed = False
        unique_together = ("content_type", "object_id", "translation_field_id", "language")
        db_table = "translation_string"

