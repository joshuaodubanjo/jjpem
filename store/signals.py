from .models import Customer,User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_customer_for_user(sender, instance,created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

# post_save.connect(create_customer_for_user, sender=User, weak=False)        

# @receiver(post_save, sender=User)
# def create_customer_for_user(sender, **kwargs):
#     if kwargs['created']:
#         Customer.objects.create(user=kwargs['instance'])