from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    EmailPhoneLoginView,
    RegisterView,
    TripViewSet,
    TripBookingViewSet,
    TripAllBookingViewSet,
    TransactionViewSet,
    UserListViewSet,
    TripImageViewSet,
)

router = DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'bookings', TripBookingViewSet, basename='booking')
router.register(r'all-bookings', TripAllBookingViewSet, basename='all-bookings')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'users', UserListViewSet, basename='users')
router.register(r'trip-images', TripImageViewSet, basename='trip-images')

urlpatterns = [
    # Auth
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/login-identifier/', EmailPhoneLoginView.as_view(), name='login-identifier'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # API
    path('', include(router.urls)),
]
