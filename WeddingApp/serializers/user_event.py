from rest_framework import serializers
from WeddingApp.models import Event, UserEvent, UserProfile
from datetime import datetime
from WeddingApp.serializers import UserProfileSerializer, EventSerializer
from django.utils import timezone




class UserEventSerializer(serializers.ModelSerializer):
    guest = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = UserEvent
        fields = [
            'id',
            'uuid',
            'guest',
            'event',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        if data['guest'] == data['event'].user:
            raise serializers.ValidationError("The guest cannot be the event creator.")
        return data