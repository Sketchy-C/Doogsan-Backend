# doogsan_app/views.py
from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Trip, TripBooking, Transaction,TripImage
from .serializers import (
    LoginSerializer,
    EmailPhoneLoginSerializer,
    RegisterSerializer,
    TripSerializer,
    TripBookingSerializer,
    TransactionSerializer,
    UserSerializer,
    TripImageSerializer
)
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role.name if user.role else None
                }
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

class EmailPhoneLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailPhoneLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


##CRUD Views for Trip, TripBooking, Transaction

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        trip = self.get_object()
        
        # Create a new booking
        seats = request.data.get('seats', 1)
        booking = TripBooking.objects.create(
            trip=trip,
            user=request.user,
            seats=seats
        )

        serializer = TripBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TripBookingViewSet(viewsets.ModelViewSet):
    serializer_class = TripBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TripBooking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TripAllBookingViewSet(viewsets.ModelViewSet):
    serializer_class = TripBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TripBooking.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



User = get_user_model()

class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['phone', 'email']


class TripImageViewSet(viewsets.ModelViewSet):
    queryset = TripImage.objects.all()
    serializer_class = TripImageSerializer
    permission_classes = [IsAuthenticated]



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # Make sure to handle string/related object role
        role_name = getattr(user.role, "name", str(user.role))  # works for both cases
        if role_name.strip().lower() != "admin":
            logger.warning("Permission denied: User is not admin %s", role_name)
            raise PermissionDenied("Admin access required")

        return super().list(request)


    def create(self, request):
        """
        POST /transactions/ --> Authenticated users
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # no user field assumed
        return Response(
            {
                "MessageCode": "200",
                "Message": "Successfully received data",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
