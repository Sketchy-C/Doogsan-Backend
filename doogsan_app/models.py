
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = []


class Role(models.Model):
    ADMIN = 'admin'
    CUSTOMER = 'customer'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
    )

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

from django.db import models

class Transaction(models.Model):
    acct_no = models.CharField(max_length=50,  )
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    booked_balance = models.CharField(max_length=50,  )
    cleared_balance = models.CharField(max_length=50,  )

    currency = models.CharField(max_length=10,  )

    cust_memo_line1 = models.CharField(max_length=255, blank=True,  )
    cust_memo_line2 = models.CharField(max_length=255, blank=True,  )
    cust_memo_line3 = models.CharField(max_length=255, blank=True,  )

    event_type = models.CharField(max_length=20,  )
    exchange_rate = models.CharField(max_length=50, blank=True,  )

    narration = models.CharField(max_length=255,  )

    payment_ref = models.CharField(
        max_length=100,
        unique=True,
         
    )

    posting_date = models.CharField(max_length=50,  )
    value_date = models.CharField(max_length=50,  )
    transaction_date = models.CharField(max_length=50,  )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
         
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id



class TripBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

class TripImage(models.Model):
    trip = models.ForeignKey(
        Trip,
        related_name='images',
        on_delete=models.CASCADE
    )
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.trip.title}"
