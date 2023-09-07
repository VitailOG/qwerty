import re

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_captcha.serializers import RestCaptchaSerializer

from main.models import Comment


class CreateCommentSerializer(RestCaptchaSerializer, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'text',
            'homepage',
            'file',
            'author',
            'parent',
            'captcha_key',
            'captcha_value'
        )

    def validate_text(self, value):
        regex_pattern = r'<(?!\/?(%s)\b)[^>]+>' % '|'.join(settings.ALLOWED_TAGS)

        filtered_tags = re.findall(regex_pattern, value)

        if filtered_tags:
            raise serializers.ValidationError("Field have disable tags")

        # tags = re.findall("<[^>]+\/?>", value)
        # print(tags)
        # test tags parametrize with nullcontext

        for tag in settings.ALLOWED_TAGS:
            if value.count(f'<{tag}') != value.count(f'</{tag}>'):
                raise serializers.ValidationError(f"Invalid tag - {tag}")

        return value


class RecursiveSerializer(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ParentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')


class CommentSerializer(serializers.ModelSerializer):
    parent = ParentCommentSerializer(allow_null=True)
    author = AuthorSerializer()
    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'children',
            'parent',
            'file',
            'author',
            'text'
        )
