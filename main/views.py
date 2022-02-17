from django.db.models import Q

from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *
from .permissions import *


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny, ]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]

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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    # @action(detail=True, methods=['get'])
    # def like(self, request, pk):
    #     user = request.user
    #     comment = get_object_or_404(Comment, pk=pk)
    #     comment.likes.set(user)
    #     if user.is_authenticated:
    #         if user in comment.likes.all():
    #             comment.likes.remove(user)
    #             message = 'Unliked!'
    #         else:
    #             comment.likes.add(user)
    #             message = 'Liked!'
    #     context = {'status': message}
    #     return Response(context, status=status.HTTP_200_OK)


class CarImageView(generics.ListCreateAPIView):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [AllowAny, ]

    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request}


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny, ]

    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]
