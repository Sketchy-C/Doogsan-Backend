from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction

@receiver(post_save, sender=Transaction)
def transaction_created(sender, instance, created, **kwargs):
    if created:
        print("transaction made✔️")
