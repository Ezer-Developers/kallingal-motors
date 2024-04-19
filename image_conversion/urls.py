from django.urls import path
from .views import ImageCompressionView
from .views import compressed_image_view

urlpatterns = [
    path('compress/', ImageCompressionView.as_view(), name='compress_image'),
    path('compressed-images/<int:pk>/', compressed_image_view, name='compressed_image'),

]