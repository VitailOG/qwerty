from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from comments.utils import is_txt_file
from comments.pagination import BasePagination
from main.models import Comment
from main.tasks import image_processing
from main.consumers import broadcast_websocket_data
from main.serializers import CommentSerializer
from main.serializers import CreateCommentSerializer


class CreateCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data.update({"author": request.user.id})
        comment = CreateCommentSerializer(data=request.data)
        comment.is_valid(raise_exception=True)
        file = comment.validated_data.get('file', None)

        if file is not None and not is_txt_file(file.name):
            comment.validated_data.pop('file', None)
            comment.save()
            image_processing.delay(file.read(), file.name, file.content_type, comment.instance.id)
        else:
            comment.save()

        created_comment_data = CommentSerializer(comment.validated_data | {"id": comment.instance.id}).data
        broadcast_websocket_data(created_comment_data)
        return Response(created_comment_data, status=status.HTTP_201_CREATED)


class ListCommentsAPI(ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    pagination_class = BasePagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', '-id')
        return Comment.objects.get_orphaned_items(order_by)
