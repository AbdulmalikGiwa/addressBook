from django.db import models
from user.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(blank=False, max_length=25)
    state = models.CharField(blank=False, max_length=25)
    city = models.CharField(blank=False, max_length=25)
    postal_code = models.CharField(blank=True, max_length=25)
    line_1 = models.CharField(blank=False, verbose_name="Address line 1", max_length=1000)
    line_2 = models.CharField(blank=True, verbose_name="Address line 2", max_length=1000)
    line_3 = models.CharField(blank=True, verbose_name="Address line 3", max_length=1000)

    class Meta:
        unique_together = [
            'user', 'line_1',
            'country', 'state',
            'city', 'postal_code'
        ]
