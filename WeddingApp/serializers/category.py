from rest_framework import serializers
from WeddingApp.models import Category
from rest_framework.validators import ValidationError



class CategorySerializer(serializers.ModelSerializer):
    additional_fields = serializers.JSONField(required=True)
    category_image = serializers.ImageField(required=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'category_name',
            'category_image',
            'additional_fields',
            'sub_category',
            "category",
        ]

    def validate(self, attrs):
        if attrs.get('sub_category'):
            if attrs.get('category') is None:
                raise serializers.ValidationError("Category field is required")
        return attrs

    def create(self, validated_data):
        category_name = validated_data.get('category_name').lower()

        if Category.objects.filter(category_name__iexact=category_name).exists():
            raise serializers.ValidationError("Category Name Already Exists")
        
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        category_name = validated_data.get('category_name', instance.category_name).lower()

        if Category.objects.filter(category_name__iexact=category_name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Category Name Already Exists")

        instance.category_name = category_name
        instance.additional_fields = validated_data.get('additional_fields', instance.additional_fields)
        instance.category_image = validated_data.get('category_image', instance.category_image)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)
        instance.category = validated_data.get('category', instance.category)

        instance.save()
        return instance
