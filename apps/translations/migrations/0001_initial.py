# Generated by Django 5.1.2 on 2024-10-14 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('title', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'language',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TranslationString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('translation_field_id', models.IntegerField(choices=[('name', 1), ('title', 2), ('description', 3), ('text', 4), ('question', 5), ('answer', 6), ('additional', 7)], default=1)),
                ('text', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'translation_string',
                'managed': False,
            },
        ),
    ]
