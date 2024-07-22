from django.core.exceptions import ValidationError
from django.conf import settings

def validate_image_size(image):
    if image.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f"The maximum file size that can be uploaded is {settings.MAX_UPLOAD_SIZE / (1024 * 1024)} MB")