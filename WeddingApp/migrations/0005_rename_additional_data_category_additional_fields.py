# Generated by Django 5.0.4 on 2024-05-28 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingApp', '0004_alter_category_additional_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='additional_data',
            new_name='additional_fields',
        ),
    ]
