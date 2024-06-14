from rest_framework import serializers
from WeddingApp.models import Event
from rest_framework.validators import ValidationError
from datetime import datetime
import re

class EventSerializer(serializers.ModelSerializer):
    additional_fields = serializers.JSONField(required=True)

    class Meta:
        model = Event
        exclude = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        errors = {}
        additional_fields = attrs.get('additional_fields', [])

        for field in additional_fields:
            key = field.get('key')
            value = field.get('value')
            field_type = field.get('type')
            label = field.get('label')
            
            if field_type == "number" and label == "Phone Number":
                phone_number_pattern = r'^\+?(\d{1,3})?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}$'
                phone_number_digits = re.sub(r'\D', '', value)
                if not re.match(phone_number_pattern, value) or len(phone_number_digits) != 10:
                    errors[key] = [f'{label} must be a valid phone number with exactly 10 digits.']

            if field_type == "string" and label == "Email":
                if not value or not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
                    errors[key] = [f'{label} must be a valid email address.']

            if field_type == "date" and value:
                try:
                    date_value = datetime.strptime(value, "%Y-%m-%d").date()
                    if date_value < datetime.now().date():
                        errors[key] = [f'{label} must be a future date.']
                except ValueError:
                    errors[key] = [f'{label} must be a valid date in YYYY-MM-DD format.']

            if field_type == "time" and value:
                try:
                    time_value = datetime.strptime(value, "%H:%M").time()
                    if key == "event_start_time":
                        start_time = time_value
                    if key == "event_end_time":
                        end_time = time_value
                        if start_time >= end_time:
                            errors[key] = [f'{label} must be before end time.']
                        if (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute) < 60:
                            errors[key] = [f'The event duration must be at least one hour.']
                except ValueError:
                    errors[key] = [f'{label} must be a valid time in HH:MM format.']

            if field_type == "int" and value:
                if not str(value).isdigit():
                    errors[key] = [f'{label} must be a valid integer.']
                else:
                    int_value = int(value)
                    if key == "bride_age" and int_value < 18:
                        errors[key] = ["Bride must be at least 18 years old."]
                    if key == "groom_age" and int_value < 21:
                        errors[key] = ["Groom must be at least 21 years old."]

        created_at = attrs.get('created_at')
        event_date = attrs.get('event_date')
        if event_date and created_at and event_date < created_at.date():
            errors['event_date'] = ['Event date cannot be before the creation date.']

        if errors:
            raise serializers.ValidationError(errors)
        return attrs
