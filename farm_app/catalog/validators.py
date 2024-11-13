from django.core.exceptions import ValidationError


def validate_image_size(image):
    if image.size > 5242880:
        raise ValidationError('The image should be up to 5 MB!')
