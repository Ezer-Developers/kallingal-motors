from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageUploadSerializer
from .utils import compress_image
from .models import CompressedImage

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageUploadSerializer
from .utils import compress_image
from rest_framework.reverse import reverse
import os
class ImageCompressionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            original_image = request.FILES.get('original_image')
            compressed_image_data = compress_image(original_image)
            print(compressed_image_data)
            print(type(compressed_image_data),"blah blah")
            if compressed_image_data:
                # Save compressed image data to the 'compressed_image' field of the model
                compressed_image = CompressedImage(original_image=original_image, compression_quality=20)
                compressed_image.compressed_image.save('compressed_image.jpg', compressed_image_data)
                compressed_image.save()
                print(compressed_image)
                print("shit")

                # Generate URL to access the compressed image
                compressed_image_url = f"/api/compressed-images/{compressed_image.pk}/"
                print(compressed_image_url)
                print("dfsasdfasdfasdfasdf")
                response_data = {
                    'compressed_image': compressed_image_url,
                    'compression_quality': 20
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to compress image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import SuspiciousFileOperation
from .models import CompressedImage

def compressed_image_view(request, pk):
    try:
        compressed_image = CompressedImage.objects.get(pk=pk)
    except CompressedImage.DoesNotExist:
        return HttpResponseNotFound("Compressed image not found")
    
    # Get the path to the original image and compressed image
    original_image_path = compressed_image.original_image.path
    compressed_image_path = compressed_image.compressed_image.path

    # Get the size of the original image before compression
    original_image_size = os.path.getsize(original_image_path)
    compressed_image_size = os.path.getsize(compressed_image_path)

    print(original_image_size, compressed_image_size)

    try:
        # Open the compressed image file and read its content
        with open(compressed_image.compressed_image.path, 'rb') as f:
            image_data = f.read()
    except (FileNotFoundError, SuspiciousFileOperation):
        return HttpResponseNotFound("Compressed image file not found")

    # Set the content type of the response to image/jpeg
    response = HttpResponse(image_data, content_type='image/jpeg')
    return response

