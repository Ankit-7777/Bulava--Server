from rest_framework import serializers
from WeddingApp.models import Event, SubEvent, Category, UserProfile
from datetime import datetime
import re
from WeddingApp.serializers import CoverImageSerializer, UserProfileSerializer

class SubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEvent
        fields = '__all__'


def check_validation(additional_fields, errors):
    for field in additional_fields:
        if not isinstance(field, dict):
            errors.append("Each field should be a dictionary.")
            continue

        field_errors = []
        key = field.get('key')
        value = field.get('value')
        field_type = field.get('type')
        label = field.get('label')
        is_mandatory = field.get('is_mandatory', False)

        if is_mandatory and (value is None or value == ''):
            field_errors.append(f'{label} is required.')

        if field_type == "number" and label == "Phone Number":
            phone_number_pattern = r'^\+?(\d{1,3})?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}$'
            phone_number_digits = re.sub(r'\D', '', value)
            if not re.match(phone_number_pattern, value) or len(phone_number_digits) != 10:
                field_errors.append(f'{label} must be a valid phone number with exactly 10 digits.')

        if field_type == "string" and label == "Email":
            if not value or not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
                field_errors.append(f'{label} must be a valid email address.')

        if field_type == "date" and value:
            try:
                date_value = datetime.strptime(value, "%Y-%m-%d").date()
                if date_value < datetime.now().date():
                    field_errors.append(f'{label} must be a future date.')
            except ValueError:
                field_errors.append(f'{label} must be a valid date in YYYY-MM-DD format.')

        if field_type == "time" and value:
            try:
                time_value = datetime.strptime(value, "%H:%M").time()
                if key == "event_start_time":
                    start_time = time_value
                if key == "event_end_time":
                    end_time = time_value
                    if start_time >= end_time:
                        field_errors.append(f'{label} must be before end time.')
                    if (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute) < 60:
                        field_errors.append(f'The event duration must be at least one hour.')
            except ValueError:
                field_errors.append(f'{label} must be a valid time in HH:MM format.')

        if field_type == "int" and value:
            if not str(value).isdigit():
                field_errors.append(f'{label} must be a valid integer.')
            else:
                int_value = int(value)
                if key == "bride_age" and int_value < 18:
                    field_errors.append("Bride must be at least 18 years old.")
                if key == "groom_age" and int_value < 21:
                    field_errors.append("Groom must be at least 21 years old.")

        if field_errors:
            errors.append({key: field_errors})
        else:
            errors.append({})

    return errors


class EventSerializer(serializers.ModelSerializer):
    cover_image_id = CoverImageSerializer()
    additional_fields = serializers.JSONField(required=True)
    sub_events = SubEventSerializer(many=True, read_only=True, source='event')
    invited_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), many=True, write_only=True, required=False)
    invited = UserProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'image',
            'cover_image_id',
            'invited',
            'invited_id',
            'user',
            'event_category',
            'sub_events',
            'additional_fields',
            'is_published',
            'is_seen',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        errors = []
        additional_fields = attrs.get('additional_fields', [])
        if additional_fields:
            errors = check_validation(additional_fields, errors)

        created_at = attrs.get('created_at')
        event_date = attrs.get('event_date')
        if event_date and created_at and event_date < created_at.date():
            errors.append({'event_date': 'Event date cannot be before the creation date.'})
        if any([True for error in errors if error]):
            raise serializers.ValidationError({'data': errors})
        return attrs

    def create(self, validated_data):
        subevents_data = self.context['request'].data.get('sub_events', [])
        invited_events = validated_data.pop('invited_id', [])
        event = Event.objects.create(**validated_data)
        subevent_instances = []
        for subevent_data in subevents_data:
            category_id = subevent_data.pop('category')
            category = Category.objects.get(id=category_id)
            subevent_instance = SubEvent(event=event, category=category, **subevent_data)
            subevent_instances.append(subevent_instance)
        SubEvent.objects.bulk_create(subevent_instances)
        if invited_events:
            event.invited.set(invited_events)
        return event

    def update(self, instance, validated_data):
        invited = validated_data.pop('invited_id', [])
        subevents_data = self.context['request'].data.get('sub_events', [])
        subevent_ids = [item.get('id') for item in subevents_data]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if invited is not None:
            instance.invited.set(invited)

        existing_subevents = SubEvent.objects.filter(event=instance)
        existing_subevents_ids = [subevent.id for subevent in existing_subevents]

        for subevent_data in subevents_data:
            subevent_id = subevent_data.get('id')
            category_id = subevent_data.pop('category')
            category = Category.objects.get(id=category_id)
            if subevent_id and subevent_id in existing_subevents_ids:
                subevent = SubEvent.objects.get(id=subevent_id, event=instance)
                for attr, value in subevent_data.items():
                    setattr(subevent, attr, value)
                subevent.category = category
                subevent.save()
            else:
                SubEvent.objects.create(
                    event=instance,
                    category=category,
                    name=subevent_data.get('name'),
                    image=subevent_data.get('image'),
                    additional_fields=subevent_data.get('additional_fields', {})
                )

        for subevent_id in existing_subevents_ids:
            if subevent_id not in subevent_ids:
                SubEvent.objects.get(id=subevent_id).delete()

        return instance
