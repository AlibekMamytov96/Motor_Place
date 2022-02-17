from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .serializers import *
from .permissions import IsSeller, IsBuyer


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy']:
            permissions = [IsSeller]
        elif self.action == 'create':
            permissions = [IsSeller]
        else:
            permissions = [IsSeller, IsBuyer]
        return [permission() for permission in permissions]


class CarViewSet(PermissionMixin, ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=query) or
                                              Q(brand__icontains=query))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        user = request.user
        comment = get_object_or_404(Comment, pk=pk)
        if user.is_authenticated:
            if user in comment.likes.all():
                comment.likes.remove(user)
                message = 'Unliked!'
            else:
                comment.likes.add(user)
                message = 'Liked!'
        context = {'status': message}
        return Response(context, status=status.HTTP_200_OK)


class BrandViewSet(PermissionMixin, ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
