from django.db import models

# Create your models here.
class Currency(models.Model):
    rank = models.IntegerField()
    image = models.CharField(max_length=500)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    market_cap = models.IntegerField()
    market_share = models.FloatField()
    price = models.FloatField()
    day_change = models.FloatField()

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name + "(" + self.symbol + ")"

