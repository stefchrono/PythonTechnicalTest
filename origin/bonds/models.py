import requests
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

class Bond(models.Model):
    isin = models.CharField(max_length=50)
    size = models.IntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=50)
    legal_name = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # Customise instance save to source Legal Name
    def save(self, *args, **kwargs):
        lei_url = f"https://leilookup.gleif.org/api/v2/leirecords?lei={self.lei}"
        response = requests.get(lei_url).json()
        self.legal_name = response[0]['Entity']['LegalName']['$']
        super(Bond, self).save(*args, **kwargs)

# Post-Save signal to create Auth Token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        

