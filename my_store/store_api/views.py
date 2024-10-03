from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User

from . import models
from . import serializers
from .permissions import ReadOnly


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]

    queryset = models.Product.objects.get_queryset().order_by('id')
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['categories__name']
    ordering_fields = ['price']


class ReviewListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
