# Generated by Django 5.0.6 on 2024-07-04 10:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeddingApp', '0022_category_category_category_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.CharField(default=1, max_length=255, verbose_name='Event ID'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='WeddingApp.event')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('ignored', 'Ignored'), ('declined', 'Declined')], default='ignored', max_length=12)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_events', to='WeddingApp.event')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
