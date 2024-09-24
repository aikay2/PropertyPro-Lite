from rest_framework import serializers
from .models import Property, PropertyImage, Flags

class PropertyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyImage
        fields = ['id', 'image_url']
        read_only_fields = ['id']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False) 
    
    class Meta:
        model = Property
        fields = ['id', 'owner', 'status', 'price', 'state', 'city', 'address', 'type', 'created_on', 'images']
        read_only_fields = ['id', 'created_on', 'owner']
        
        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Price must be a positive value.")
            return value
        
    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        property_instance = Property.objects.create(**validated_data)
        
        if images_data:
            for image in images_data:
                PropertyImage.objects.create(property=property_instance, **image)
        
        return property_instance
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if images_data:
            instance.images.all().delete()
            for image in images_data:
                PropertyImage.objects.create(property=instance, **image)
        
        return instance
    

class PropertyStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Property
        fields = ['id', 'owner', 'status', 'price', 'state', 'city', 'address', 'type', 'created_on']
        read_only_fields = ['id', 'owner', 'price', 'state', 'city', 'address', 'type', 'created_on']

        
class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flags
        fields = '__all__'
        read_only_fields = ['id', 'property_id', 'created_by']