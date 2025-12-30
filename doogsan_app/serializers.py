from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Role, Trip, TripImage, TripBooking, Transaction
import cloudinary.uploader

User = get_user_model()

# =========================
# AUTH SERIALIZERS
# =========================

class EmailPhoneLoginSerializer(TokenObtainPairSerializer):
    username = None

    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier').strip()
        password = attrs.get('password')

        user = (
            User.objects.filter(email=identifier).first()
            or User.objects.filter(phone=identifier).first()
        )

        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        data = super().validate({
            'username': user.username,
            'password': password
        })

        data['user'] = UserSerializer(user).data
        return data


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')

    def create(self, validated_data):
        role = Role.objects.get(name='customer')
        return User.objects.create_user(
            role=role,
            **validated_data
        )


# =========================
# USER
# =========================

class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'role')


# =========================
# TRIP
# =========================
class TripImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all()
    )

    class Meta:
        model = TripImage
        fields = ('id', 'trip', 'image', 'image_url')
        read_only_fields = ('image_url',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        trip = validated_data.pop('trip')

        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            image,
            folder='trip_images'
        )

        image_url = upload_result.get('secure_url')

        # Save TripImage instance
        trip_image = TripImage.objects.create(
            trip=trip,
            image_url=image_url
        )

        return trip_image


class TripSerializer(serializers.ModelSerializer):
    images = TripImageSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'


# =========================
# BOOKINGS
# =========================

class TripBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trip = TripSerializer(read_only=True)

    class Meta:
        model = TripBooking
        fields = '__all__'


# =========================
# TRANSACTIONS
# =========================
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    AcctNo = serializers.CharField(source="acct_no")
    Amount = serializers.DecimalField(
        max_digits=15, decimal_places=2, source="amount"
    )
    BookedBalance = serializers.CharField(source="booked_balance")
    ClearedBalance = serializers.CharField(source="cleared_balance")
    Currency = serializers.CharField(source="currency")

    CustMemoLine1 = serializers.CharField(
        source="cust_memo_line1", allow_blank=True, required=False
    )
    CustMemoLine2 = serializers.CharField(
        source="cust_memo_line2", allow_blank=True, required=False
    )
    CustMemoLine3 = serializers.CharField(
        source="cust_memo_line3", allow_blank=True, required=False
    )

    EventType = serializers.CharField(source="event_type")
    ExchangeRate = serializers.CharField(
        source="exchange_rate", allow_blank=True, required=False
    )
    Narration = serializers.CharField(source="narration")
    PaymentRef = serializers.CharField(source="payment_ref")
    PostingDate = serializers.CharField(source="posting_date")
    ValueDate = serializers.CharField(source="value_date")
    TransactionDate = serializers.CharField(source="transaction_date")
    TransactionId = serializers.CharField(source="transaction_id")

    class Meta:
        model = Transaction
        fields = [
            "AcctNo",
            "Amount",
            "BookedBalance",
            "ClearedBalance",
            "Currency",
            "CustMemoLine1",
            "CustMemoLine2",
            "CustMemoLine3",
            "EventType",
            "ExchangeRate",
            "Narration",
            "PaymentRef",
            "PostingDate",
            "ValueDate",
            "TransactionDate",
            "TransactionId",
        ]
