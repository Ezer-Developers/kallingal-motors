from django.db import models

class CompressedImage(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    compressed_image = models.ImageField(upload_to='compressed_images/')
    compression_quality = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compressed Image {self.id}"
