from rest_framework import serializers
from WeddingApp.models import  Event
from rest_framework.validators import ValidationError
from django.utils import timezone
from datetime import date


 
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        errors = {}

        event_date = attrs.get('event_date')
        event_start_time = attrs.get('event_start_time')
        event_end_time = attrs.get('event_end_time')
        created_at = attrs.get('created_at')

        # Validate event date is in the future
        if event_date and event_date < timezone.now().date():
            errors['event_date'] = ['Event date must be in the future.']

        # Validate event start time is before end time
        if event_start_time and event_end_time:
            start_datetime = timezone.datetime.combine(timezone.now().date(), event_start_time)
            end_datetime = timezone.datetime.combine(timezone.now().date(), event_end_time)
            if start_datetime >= end_datetime:
                errors['event_start_time'] = ['Event start time must be before end time.']

        # Validate event duration is at least one hour
        if event_start_time and event_end_time:
            start_datetime = timezone.datetime.combine(timezone.now().date(), event_start_time)
            end_datetime = timezone.datetime.combine(timezone.now().date(), event_end_time)
            time_diff = (end_datetime - start_datetime).total_seconds()
            if time_diff < 3600:  # 3600 seconds = 1 hour
                errors['event_end_time'] = ['The event duration must be at least one hour.']

        # Validate event date is not before creation date
        if event_date and created_at and event_date < created_at.date():
            errors['event_date'] = ['Event date cannot be before the creation date.']

        # Validate bride's age
        bride_age = attrs.get('bride_age')
        if bride_age is not None and bride_age < 18:
            errors['bride_age'] = ["Bride must be at least 18 years old."]

        # Validate groom's age
        groom_age = attrs.get('groom_age')
        if groom_age is not None and groom_age < 21:
            errors['groom_age'] = ["Groom must be at least 21 years old."]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
