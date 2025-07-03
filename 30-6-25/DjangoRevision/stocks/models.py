from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Stocks(models.Model):
    ticker   =  models.CharField(max_length=10)
    name =  models.CharField(max_length=300)
    description  =  models.CharField(max_length =5000)
    curr_price =  models.FloatField()

    def __str__(self):
        return  self.name

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField(default=0)

class Transaction(models.Model):
    ACTIONS = (('BUY', 'Buy'), ('SELL', 'Sell'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    action = models.CharField(max_length=4, choices=ACTIONS)
    amount = models.PositiveIntegerField()
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000)  # Starting balance

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)