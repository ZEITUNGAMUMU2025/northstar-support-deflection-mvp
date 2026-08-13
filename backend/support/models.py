from django.db import models

# Create your models here.
from django.db import models


class Order(models.Model):
    order_id = models.IntegerField(unique=True)
    status = models.CharField(max_length=50)
    expected_delivery = models.DateField()

    def __str__(self):
        return str(self.order_id)