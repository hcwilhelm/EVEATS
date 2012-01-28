# 
#  models.py
#  EVEATS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 


from django.db import models


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
        db_table        = "invmarketgroups"
        managed         = False

    def __unicode__(self):
        return unicode(self.marketGroupID)



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
