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
  cachedUntil   = datetime.datetime.utcnow() + datetime.timedelta(days=1)

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

# ======================================================================================================
# = dgmTables                                                                                          =
# ======================================================================================================

class dgmAttributeCategories(models.Model):
  categoryID                          = models.IntegerField(primary_key=True)
  categoryName                        = models.CharField(max_length=50, null=True)
  categoryDescription                 = models.CharField(max_length=200, null=True)
  
  class Meta:
    db_table  = "dgmAttributeCategories"
    managed   = False
    
  def __unicode__(self):
    return unicode(self.categoryID)

class dgmAttributeTypes(models.Model):
  attributeID                         = models.IntegerField(primary_key=True)
  attributeName                       = models.CharField(max_length=100, null=True)
  description                         = models.CharField(max_length=1000, null=True)
  iconID                              = models.ForeignKey('eveIcons', db_column='iconID', null=True)
  defaultValue                        = models.FloatField(null=True)
  published                           = models.NullBooleanField()
  displayName                         = models.CharField(max_length=100, null=True)
  unitID                              = models.ForeignKey('eveUnits', db_column='unitID', null=True)
  stackable                           = models.NullBooleanField()
  highIsGood                          = models.NullBooleanField()
  categoryID                          = models.ForeignKey('dgmAttributeCategories', db_column='categoryID', null=True)
  
  class Meta:
    db_table  = "dgmAttributeTypes"
    managed   = False
    
  def __unicode__(self):
    return unicode(self.attributeID)
    
class dgmEffects(models.Model):
  effectID                            = models.IntegerField(primary_key=True)
  effectName                          = models.CharField(max_length=400, null=True)
  effectCategory                      = models.IntegerField(null=True)
  preExpression                       = models.IntegerField(null=True)
  postExpression                      = models.IntegerField(null=True)
  description                         = models.CharField(max_length=1000, null=True)
  guid                                = models.CharField(max_length=60, null=True)
  iconID                              = models.ForeignKey('eveIcons', db_column='iconID', null=True)
  isOffensive                         = models.NullBooleanField()
  isAssistance                        = models.NullBooleanField()
  durationAttributeID                 = models.ForeignKey('dgmAttributeTypes', related_name="durationAttribute_set", db_column='durationAttributeID', null=True)
  trackingSpeedAttributeID            = models.ForeignKey('dgmAttributeTypes', related_name="trackingSpeedAttribute_set", db_column='trackingSpeedAttributeID', null=True)
  dischargeAttributeID                = models.ForeignKey('dgmAttributeTypes', related_name="dischargeAttribute_set", db_column='dischargeAttributeID', null=True)
  rangeAttributeID                    = models.ForeignKey('dgmAttributeTypes', related_name="rangeAttribute_set", db_column='rangeAttributeID', null=True)
  falloffAttributeID                  = models.ForeignKey('dgmAttributeTypes', related_name="falloffAttribute_set", db_column='falloffAttributeID', null=True)
  disallowAutoRepeat                  = models.NullBooleanField()
  published                           = models.NullBooleanField()
  displayName                         = models.CharField(max_length=100, null=True)
  isWarpSafe                          = models.NullBooleanField()
  rangeChance                         = models.NullBooleanField()
  electronicChance                    = models.NullBooleanField()
  propulsionChance                    = models.NullBooleanField()
  distribution                        = models.IntegerField(null=True)
  sfxName                             = models.CharField(max_length=20, null=True)
  npcUsageChanceAttributeID           = models.ForeignKey('dgmAttributeTypes', related_name="npcUsageChanceAttribute_set", db_column='npcUsageChanceAttributeID', null=True)
  npcActivationChanceAttributeID      = models.ForeignKey('dgmAttributeTypes', related_name="npcActivationChanceAttribute_set", db_column='npcActivationChanceAttributeID', null=True)
  fittingUsageChanceAttributeID       = models.ForeignKey('dgmAttributeTypes', related_name="fittingUsageChanceAttribute_set", db_column='fittingUsageChanceAttributeID', null=True)
  
  class Meta:
    db_table  = "dgmEffects"
    managed   = False
    
  def __unicode__(self):
    return unicode(self.effectID)

#
# Altered table cause Django dosen't support combined primary key
#

class dgmTypeAttributes(models.Model):
  typeAttributeID                     = models.IntegerField(primary_key=True)
  typeID                              = models.ForeignKey('invTypes', db_column='typeID', null=True)
  attributeID                         = models.ForeignKey('dgmAttributeTypes', db_column='attributeID', null=True)
  valueInt                            = models.IntegerField(null=True)
  valueFloat                          = models.FloatField(null=True)
  
  class Meta:
    db_table = "dgmTypeAttributes"
    managed   = False
    
  def __unicode__(self):
    return unicode(self.typeID)


#
# Altered table cause Django dosen't support combined primary key
#    

class dgmTypeEffects(models.Model):
  typeEffectID                        = models.IntegerField(primary_key=True)
  typeID                              = models.ForeignKey('invTypes', db_column='typeID', null=True)
  effectID                            = models.ForeignKey('dgmEffects', db_column='effectID', null=True)
  isDefault                           = models.NullBooleanField()
  
  class Meta:
    db_table = "dgmTypeEffects"
    managed   = False
  
  def __unicode__(self):
    return unicode(self.typeID)  
        
        
# ======================================================================================================
# = eveTables                                                                                          =
# ======================================================================================================

class eveIcons(models.Model):
    iconID                            = models.SmallIntegerField(primary_key=True)
    iconFile                          = models.CharField(max_length=500)
    description                       = models.CharField(max_length=1600)

    class Meta:
        db_table    = 'eveIcons'
        managed     = False

    def __unicode__(self):
        return unicode(self.iconID)
        
class eveUnits(models.Model):
  unitID                              = models.IntegerField(primary_key=True)
  unitName                            = models.CharField(max_length=100, null=True)
  displayName                         = models.CharField(max_length=50, null=True)
  description                         = models.CharField(max_length=1000, null=True)
  
  class Meta:
      db_table    = 'eveUnits'
      managed     = False

  def __unicode__(self):
      return unicode(self.unitID)