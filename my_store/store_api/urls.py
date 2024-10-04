from django.urls import path
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views

app_name = 'store_api'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/reviews/', views.ReviewListView.as_view(), name='product-reviews'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]

if settings.DEBUG:
    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='store_api:schema'), name='swagger'),
        path('redoc/', SpectacularRedocView.as_view(url_name='store_api:schema'), name='redoc'),
    ]
