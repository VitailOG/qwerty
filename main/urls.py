from django.urls import path
from rest_framework import routers

from main.views import CreateCommentAPI, ListCommentsAPI

router = routers.SimpleRouter()

router.register('list', ListCommentsAPI, basename='comment')

urlpatterns = [path('', CreateCommentAPI.as_view())]

urlpatterns += router.urls
