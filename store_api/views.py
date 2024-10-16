from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema

from . import models, serializers, permissions, tasks


@extend_schema(tags=['Tokens'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Tokens'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Registration'])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


@extend_schema(tags=['Categories'])
class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser | permissions.ReadOnly]

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    # @extend_schema(
    #     request=serializers.CategorySerializer,
    #     responses={201: serializers.CategorySerializer},
    #     description='Create a new category',
    # )
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)


@extend_schema(tags=['Products'])
class ProductListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser | permissions.ReadOnly]

    queryset = models.Product.objects.get_queryset().order_by('id')
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['categories__name']
    ordering_fields = ['price']

    # @extend_schema(
    #     request=serializers.ProductSerializer,
    #     responses={201: serializers.ProductSerializer},
    #     description='Create a new product',
    # )
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)


@extend_schema(tags=['Cart'])
class CartView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.CartSerializer

    def get_object(self):
        cart, created = models.Cart.objects.get_or_create(user=self.request.user)
        return cart


@extend_schema(tags=['Cart'])
class AddToCartView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.CartItemSerializer

    def perform_create(self, serializer):
        cart, created = models.Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


@extend_schema(tags=['Product Reviews'])
class ReviewListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save(user=None)


@extend_schema(tags=['Orders'])
class OrderListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        tasks.send_confirmation_email.delay(self.request.user.username, order.id)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@extend_schema(tags=['Orders Detailed View'])
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
