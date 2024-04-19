from rest_framework import serializers
from .models import CompressedImage

class ImageUploadSerializer(serializers.ModelSerializer):
    compressed_image = serializers.ImageField(required=False) 
    class Meta:
        model = CompressedImage
        fields = ['original_image', 'compressed_image', 'compression_quality']

