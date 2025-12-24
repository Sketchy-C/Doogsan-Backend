from django.contrib import admin
from .models import User, Role, Trip, Transaction, TripBooking, TripImage
# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Trip)
admin.site.register(Transaction)
admin.site.register(TripBooking)
admin.site.register(TripImage)

