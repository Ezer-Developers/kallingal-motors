from PIL import Image
import io

def compress_image(image):
    try:
        img = Image.open(image)
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=20)
        output.seek(0)
        return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
