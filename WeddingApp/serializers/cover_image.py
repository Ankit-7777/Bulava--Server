from rest_framework import serializers
from WeddingApp.models import CoverImage
from rest_framework.validators import ValidationError



class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = '__all__'
    
    def validate_image(self, value):
        """
        Validate the image field.
        """
        if not value:
            raise serializers.ValidationError("Image field is required.")

        # Check if an image with the same content already exists
        if CoverImage.objects.filter(image=value).exists():
            raise serializers.ValidationError("An image with the same content already exists.")

        return value

    def create(self, validated_data):
        """
        Create and return a new CoverImage instance, given the validated data.
        """
        return CoverImage.objects.create(**validated_data)
    
    def retrieve(self, pk):
        """
        Retrieve and return a CoverImage instance, given the validated data.
        """
        return CoverImage.objects.get(pk=pk)
     