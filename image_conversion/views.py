from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageUploadSerializer
from .utils import compress_image
from .models import CompressedImage
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import SuspiciousFileOperation
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class ImageCompressionView(APIView):

    
    @swagger_auto_schema(
        request_body=ImageUploadSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Image successfully compressed.",
                schema=ImageUploadSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input data."
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Failed to compress image."
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            original_image = request.FILES.get('original_image')
            compressed_image_data = compress_image(original_image)
            
            if compressed_image_data:
                compressed_image = CompressedImage(
                    original_image=original_image, 
                    compression_quality=20
                )
                compressed_image.compressed_image.save('compressed_image.jpg', compressed_image_data)
                compressed_image.save()

                response_serializer = ImageUploadSerializer(compressed_image)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to compress image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Compressed image retrieved successfully.",
            content={
                'image/jpeg': openapi.Schema(
                    type='string',
                    format='binary'
                )
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Compressed image not found."
        ),
    }
)
def compressed_image_view(request, pk):
    try:
        compressed_image = CompressedImage.objects.get(pk=pk)
    except CompressedImage.DoesNotExist:
        return HttpResponseNotFound("Compressed image not found")
    
    original_image_path = compressed_image.original_image.path
    compressed_image_path = compressed_image.compressed_image.path

    original_image_size = os.path.getsize(original_image_path)
    compressed_image_size = os.path.getsize(compressed_image_path)

    print(original_image_size, compressed_image_size)

    try:
        with open(compressed_image.compressed_image.path, 'rb') as f:
            image_data = f.read()
    except (FileNotFoundError, SuspiciousFileOperation):
        return HttpResponseNotFound("Compressed image file not found")

    response = HttpResponse(image_data, content_type='image/jpeg')
    return response
