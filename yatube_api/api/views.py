from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorPermission
from .serializers import CommentSerializer, GroupSerializer, PostSerializer

from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка групп и отдельной группы."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AuthorPermission,)


class PostViewSet(viewsets.ModelViewSet):
    """Получение и управление постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение и управление комментариями поста."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorPermission,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
