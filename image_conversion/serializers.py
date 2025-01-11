from rest_framework import serializers
from .models import CompressedImage

class ImageUploadSerializer(serializers.ModelSerializer):
    compressed_image = serializers.ImageField(required=False) 
    id = serializers.IntegerField(read_only=True)  # Include the ID field

    class Meta:
        model = CompressedImage
        fields = ['id','original_image', 'compressed_image', 'compression_quality']

