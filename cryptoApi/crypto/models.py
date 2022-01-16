from django.db import models

# Create your models here.
class Currency(models.Model):
    rank = models.IntegerField(null=True)
    image = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=255, null=True)
    symbol = models.CharField(max_length=10, null=True)
    market_cap = models.IntegerField(null=True)
    market_share = models.FloatField(null=True)
    price = models.FloatField(null=True)
    day_change = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name + " (" + self.symbol + ")"

