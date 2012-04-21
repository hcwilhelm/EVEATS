from django.db import models
from django_extensions.db.models import TimeStampedModel

class MarketOrders(TimeStampedModel):
  orderID       = models.BigIntegerField(primary_key=True)
  invType       = models.OneToOneField('evedb.invTypes')
  region        = models.OneToOneField('evedb.mapRegions')
  station       = models.OneToOneField('eve.Station')
  price         = models.FloatField()
  vol_remain    = models.BigIntegerField()
  min_volume    = models.BigIntegerField()
  expires       = models.DateTimeField()