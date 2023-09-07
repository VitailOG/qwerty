import os

from typing import TypeVar

from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage, Storage

from comments.storage_backends import PublicMediaStorage


BaseStorageType = TypeVar('BaseStorageType', bound=Storage)


def select_file_storage() -> BaseStorageType:
    if settings.USE_S3:
        return PublicMediaStorage()
    return FileSystemStorage()


def gen_upload_path(instance, filename):
    now = timezone.now()
    return f"{now.year}/{now.month}/{now.day}/{filename}"


def is_txt_file(filename: str):
    _, t = os.path.splitext(filename)
    return t == ".txt"
