from rest_framework import serializers
from WeddingApp.models import Category
from rest_framework.validators import ValidationError



class CategorySerializer(serializers.ModelSerializer):
    additional_fields = serializers.JSONField(required=True)
    category_image = serializers.ImageField(required=True)

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        additional_fields = validated_data.pop('additional_fields')
        category_image = validated_data.pop('category_image')
        category_name = validated_data.pop('category_name')

        if Category.objects.filter(category_name__iexact=category_name).exists():
            raise serializers.ValidationError("Category Name Already Exists")
        
        category = Category.objects.create(category_name=category_name, **validated_data)
        category.additional_fields = additional_fields
        category.category_image = category_image
        category.save()

        return category

    def update(self, instance, validated_data):
        additional_fields = validated_data.get('additional_fields', instance.additional_fields)
        category_image = validated_data.get('category_image', instance.category_image)
        category_name = validated_data.get('category_name', instance.category_name).lower()

        if Category.objects.filter(category_name__iexact=category_name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Category Name Already Exists")

        instance.category_name = category_name
        instance.additional_fields = additional_fields
        instance.category_image = category_image

        instance.save()
        return instance
  
