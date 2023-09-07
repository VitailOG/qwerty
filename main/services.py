import sys

from PIL import Image
from io import BytesIO
from typing import NamedTuple

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from main.models import Comment


class SizeResolution(NamedTuple):
    width: int = settings.DEFAULT_WIDTH_PIXELS
    min: int = settings.DEFAULT_HEIGHT_PIXELS


def resize_image(file_bytes: bytes, filename: str, content_type: str) -> InMemoryUploadedFile:
    img = Image.open(BytesIO(file_bytes))

    image_size = SizeResolution(*img.size)
    max_size = SizeResolution()

    if not (image_size.width > max_size.width or image_size.min > max_size.min):
        content_file = ContentFile(file_bytes)
        return InMemoryUploadedFile(
            content_file, 'FileField', filename, content_type, content_file.tell, None
        )

    new_img = img.convert('RGB')
    new_img.thumbnail(max_size)
    filestream = BytesIO()
    new_img.save(filestream, img.format, quality=90)

    filestream.seek(0)
    return InMemoryUploadedFile(
        filestream, 'FileField', filename, content_type, sys.getsizeof(filestream), None
    )


def update_comment_file_field(comment_id: int, image: InMemoryUploadedFile) -> None:
    comment = Comment.objects.get(id=comment_id)
    comment.file = image
    comment.save(update_fields=['file'])
