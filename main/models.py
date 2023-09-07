from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from comments.models import TimeStampMixin
from comments.utils import gen_upload_path
from comments.utils import select_file_storage


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class CommentQuerySet(models.QuerySet):

    def get_orphaned_items(self, order_by: str):
        return (
            self
            .select_related('author', 'parent')
            .filter(parent__isnull=True)
            .order_by(order_by)
        )


class Comment(TimeStampMixin):
    objects = CommentQuerySet.as_manager()

    text = models.TextField(verbose_name='Текст коментаря')
    homepage = models.URLField(blank=True, null=True)
    file = models.FileField(
        blank=True,
        null=True,
        upload_to=gen_upload_path,
        storage=select_file_storage,
        validators=[FileExtensionValidator(allowed_extensions=['txt', 'png', 'jpeg', 'gif'])]
    )

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    def __str__(self):
        return f"{self.author.username} -> {self.text[:25]}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
