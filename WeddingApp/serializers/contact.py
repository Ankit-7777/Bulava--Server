from rest_framework import serializers
from WeddingApp.models import ContactUs
from rest_framework.validators import ValidationError

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = [
            'id',
            'name',
            'email',
            'message',
        ]
    
    def validate(self, data):
        errors = {}
        message = data.get('message', None)
        if not message:
            errors['message'] = ['Message field is required.']
        if message and len(message) <= 180:
            errors['message'] = ['Message must be more than 30 characters.']
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self, validated_data):
        return ContactUs.objects.create(**validated_data)
