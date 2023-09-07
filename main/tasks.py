from celery import shared_task

from main.services import resize_image, update_comment_file_field


@shared_task
def image_processing(file_bytes: bytes, filename: str, content_type: str, comment_id: int):
    image = resize_image(file_bytes, filename, content_type)
    update_comment_file_field(comment_id, image)
