from WeddingApp.models import Device
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    device = serializers.CharField(max_length=250)

    class Meta:
        model = Device
        fields = (
            'device',
            'type',
            'token',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'user': {'write_only': True}
        }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data.get('device'):
            data['device_id'] = data.pop('device')
        return data

    def create(self, validated_data):
        device, created = Device.objects.get_or_create(**validated_data)
        return device

    def validate(self, attrs):
        if not attrs.get('device_id'):
            raise serializers.ValidationError({'device': 'Device can not be blank.'})
        return attrs
