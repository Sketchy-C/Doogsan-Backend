from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    EmailPhoneLoginView,
    RegisterView,
    TripViewSet,
    TripBookingViewSet,
    TransactionViewSet,
    TripAllBookingViewSet,
    UserListViewSet,
    TripImageViewSet,
)

router = DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'bookings', TripBookingViewSet, basename='booking')
router.register(r'all_bookings', TripAllBookingViewSet, basename='all_bookings')
router.register(r'transactions', TransactionViewSet),
router.register(r'users', UserListViewSet, basename='users'),
router.register(r'trip-images', TripImageViewSet, basename='trip-images')

urlpatterns = [
    # Auth
    path('auth/login/', LoginView.as_view()),
    path('auth/login-identifier/', EmailPhoneLoginView.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),

    # API
    path('', include(router.urls)),
]
