#
#  models.py
#  EVEATS
#
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
#

from django.db import models
import datetime

# ============
# = invTypes =
# ============

class invTypes(models.Model):
    typeID                  = models.IntegerField(primary_key=True)
    groupID                 = models.ForeignKey('invGroups', null=True, db_column='groupID')
    typeName                = models.CharField(max_length=100)
    description             = models.CharField(max_length=3000)
    graphicID               = models.SmallIntegerField()
    radius                  = models.FloatField()
    mass                    = models.FloatField()
    volume                  = models.FloatField()
    capacity                = models.FloatField()
    portionSize             = models.IntegerField()
    raceID                  = models.SmallIntegerField()
    basePrice               = models.FloatField()
    published               = models.BooleanField()
    marketGroupID           = models.ForeignKey('invMarketGroups', null=True, db_column='marketGroupID')
    chanceOfDuplicating     = models.FloatField()
    iconID                  = models.ForeignKey('eveIcons', null=True, db_column='iconID')

    class Meta:
        db_table            = "invTypes"
        managed             = False

    def __unicode__(self):
        return unicode(self.typeID)

# =============
# = invGroups =
# =============

class invGroups(models.Model):
    groupID                 = models.SmallIntegerField(primary_key=True)
    categoryID              = models.ForeignKey('invCategories', null=True, db_column='categoryID')
    groupName               = models.CharField(max_length=100)
    description             = models.CharField(max_length=3000)
    iconID                  = models.ForeignKey('eveIcons', null=True, db_column='iconID')
    useBasePrice            = models.BooleanField()
    allowManufacture        = models.BooleanField()
    allowRecycler           = models.BooleanField()
    anchored                = models.BooleanField()
    anchorable              = models.BooleanField()
    fittableNonSingleton    = models.BooleanField()

    class Meta:
        db_table            = 'invGroups'
        managed             = False

    def __unicode__(self):
        return unicode(self.groupID)



# ===================
# = invMarketGroups =
# ===================

class invMarketGroups(models.Model):
    marketGroupID       = models.SmallIntegerField(primary_key=True)
    parentGroupID       = models.ForeignKey('self', null=True, db_column='parentGroupID')
    marketGroupName     = models.CharField(max_length=100)
    description         = models.CharField(max_length=3000)
    iconID              = models.ForeignKey('eveIcons', null=True, db_column='iconID')
    hasTypes            = models.BooleanField()

    class Meta:
        db_table        = "invMarketGroups"
        managed         = False

    def __unicode__(self):
        return unicode(self.marketGroupID)

    def findMarketGroupIDs(self):
      list = [self.pk]
      
      for group in self.invmarketgroups_set.all():
        list.append(group.pk)
        list.extend(group.findMarketGroupIDs())
        
      return list


# ============
# = eveIcons =
# ============

class eveIcons(models.Model):
    iconID          = models.SmallIntegerField(primary_key=True)
    iconFile        = models.CharField(max_length=500)
    description     = models.CharField(max_length=1600)

    class Meta:
        db_table    = 'eveIcons'
        managed     = False

    def __unicode__(self):
        return unicode(self.iconID)



# =================
# = invCategories =
# =================

class invCategories(models.Model):
    categoryID      = models.SmallIntegerField(primary_key=True)
    categoryName    = models.CharField(max_length=100)
    description     = models.CharField(max_length=3000)
    iconID          = models.ForeignKey('eveIcons', null=True, db_column='iconID')
    published       = models.BooleanField()

    class Meta:
        db_table    = 'invCategories'
        managed     = False

    def __unicode__(self):
        return unicode(self.categoryID)


# ==================
# = mapDenormalize =
# ==================

class mapDenormalize(models.Model):
    itemID              = models.IntegerField(primary_key=True)
    typeID              = models.ForeignKey('invTypes', db_column='typeID')
    groupID             = models.SmallIntegerField()
    solarSystemID       = models.IntegerField()
    constellationID     = models.IntegerField()
    regionID            = models.IntegerField()
    orbitID             = models.IntegerField()
    x                   = models.FloatField()
    y                   = models.FloatField()
    z                   = models.FloatField()
    radius              = models.FloatField()
    itemName            = models.CharField(max_length=100)
    security            = models.FloatField()
    celestialIndex      = models.SmallIntegerField()
    orbitIndex          = models.SmallIntegerField()

    class Meta:
        db_table        = "mapDenormalize"
        managed         = False

    def __unicode__(self):
        return unicode(self.itemID)

# ============
# = invFlags =
# ============

class invFlags(models.Model):
    flagID          = models.IntegerField(primary_key=True)
    flagName        = models.CharField(max_length=200)
    flagText        = models.CharField(max_length=200)
    orderID         = models.IntegerField()

    class Meta:
        db_table    = "invFlags"
        managed     = False

    def __unicode__(self):
        return unicode(self.flagID)

# ===============
# = staStations =
# ===============

class staStations(models.Model):
  stationID     = models.PositiveIntegerField(primary_key=True)
  stationName   = models.CharField(max_length=100)
  stationTypeID = models.ForeignKey('staStationTypes', db_column='stationTypeID')
  solarSystemID = models.IntegerField('mapSolarSystems')
  corporationID = models.ForeignKey('eve.Corporation', db_column='corporationID')
  cachedUntil = datetime.datetime.utcnow() + datetime.timedelta(days=1)

  def expired(self):
    return False

  class Meta:
    db_table = "staStations"
    managed = False

  def __unicode__(self):
    return unicode(self.stationID)

# ===================
# = staStationTypes =
# ===================

class staStationTypes(models.Model):
  stationTypeID = models.IntegerField(primary_key=True)

  class Meta:
    db_table = u'staStationTypes'
    managed = False

  def __unicode__(self):
    return unicode(self.stationID)

class mapSolarSystems(models.Model):
  solarSystemID = models.IntegerField(primary_key=True)

  class Meta:
    db_table = u'mapSolarSystems'
    managed = False

class mapRegions(models.Model):
  regionID = models.IntegerField(primary_key=True)

  class Meta:
    db_table = u'mapRegions'
    managed = False
