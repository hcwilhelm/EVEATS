# 
#  models.py
#  EVEATS
#  
#  Created by Hans Christian Wilhelm on 2011-04-30.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

from django.db import models
from django.db.models import Sum

# =================
# = corpAssetList =
# =================

class corpAssetList(models.Model):
    itemID 					= models.BigIntegerField(primary_key=True)
    locationID 				= models.ForeignKey('mapDenormalize', db_column='locationID', null=True, blank=True)
    typeID					= models.ForeignKey('invTypes', db_column='typeID')
    quantity				= models.IntegerField()
    flag					= models.ForeignKey('invFlags', db_column='flag')
    singleton 				= models.BooleanField()
    parentID				= models.ForeignKey('self', null=True, blank=True)
    isContainer				= models.BooleanField(default=False)

    def __unicode__(self):
        return (unicode(self.typeID.typeName) +  unicode(self.itemID))

    def get_Root(self):
        if self.parentID == None:
            return self
        else:
            return self.parentID.get_Root()

    def get_path(self):
        path 	= [self]
        parent 	= self.parentID

        while(parent):
            path.append(parent)
            parent = parent.parentID

        return path

# ===================
# = invMarketGroups =
# ===================

class invMarketGroups(models.Model):
    marketGroupID			= models.SmallIntegerField(primary_key=True)
    parentGroupID			= models.ForeignKey('self', null=True, db_column='parentGroupID')
    marketGroupName			= models.CharField(max_length=100)
    description				= models.CharField(max_length=3000)
    iconID					= models.ForeignKey('eveIcons', null=True, db_column='iconID')
    hasTypes				= models.BooleanField()

    class Meta:
        db_table			= "invmarketgroups"
        managed				= False

    def __unicode__(self):
        return unicode(self.marketGroupID)

    def get_iconID(self):
        if self.iconID == None:
            return None
        else:
            return self.iconID.iconID

    @staticmethod
    def get_marketGroupTree(groupTree):
        return	[
                {
                    "marketGroupID":x.marketGroupID,
                    "marketGroupName":x.marketGroupName,
                    "description":x.description,
                    "iconID":x.get_iconID(),
                    "hasTypes":x.hasTypes,
                    "childMarketGroups": invMarketGroups.get_marketGroupTree(x.invmarketgroups_set.all())
                }
            for x in groupTree
        ]

# ============
# = invTypes =
# ============

class invTypes(models.Model):
    typeID					= models.IntegerField(primary_key=True)
    groupID					= models.ForeignKey('invGroups', null=True, db_column='groupID')
    typeName				= models.CharField(max_length=100)
    description				= models.CharField(max_length=3000)
    graphicID				= models.SmallIntegerField()
    radius					= models.FloatField()
    mass					= models.FloatField()
    volume					= models.FloatField()
    capacity 				= models.FloatField()
    portionSize				= models.IntegerField()
    raceID					= models.SmallIntegerField()
    basePrice				= models.FloatField()
    published				= models.BooleanField()
    marketGroupID			= models.ForeignKey('invMarketGroups', null=True, db_column='marketGroupID')
    chanceOfDuplicating		= models.FloatField()
    iconID					= models.ForeignKey('eveIcons', null=True, db_column='iconID')

    class Meta:
        db_table			= "invTypes"
        managed				= False

    def __unicode__(self):
        return unicode(self.typeID)

    def units_available(self):
        return self.corpassetlist_set.all().aggregate(Sum('quantity'))['quantity__sum']


    def get_IconID(self):
        if self.iconID == None:
            return None
        else:
            return self.IconID.IconID

# =============
# = invGroups =
# =============

class invGroups(models.Model):
    groupID					= models.SmallIntegerField(primary_key=True)
    categoryID				= models.ForeignKey('invCategories', null=True, db_column='categoryID')
    groupName				= models.CharField(max_length=100)
    description				= models.CharField(max_length=3000)
    iconID					= models.ForeignKey('eveIcons', null=True, db_column='iconID')
    useBasePrice			= models.BooleanField()
    allowManufacture		= models.BooleanField()
    allowRecycler			= models.BooleanField()
    anchored				= models.BooleanField()
    anchorable				= models.BooleanField()
    fittableNonSingleton	= models.BooleanField()

    class Meta:
        db_table			= 'invGroups'
        managed				= False

    def __unicode__(self):
        return unicode(self.groupID)

# =================
# = invCategories =
# =================

class invCategories(models.Model):
    categoryID				= models.SmallIntegerField(primary_key=True)
    categoryName			= models.CharField(max_length=100)
    description				= models.CharField(max_length=3000)
    iconID					= models.ForeignKey('eveIcons', null=True, db_column='iconID')
    published				= models.BooleanField()

    class Meta:
        db_table			= 'invCategories'
        managed				= False

    def __unicode__(self):
        return unicode(self.categoryID)

# ============
# = eveIcons =
# ============

class eveIcons(models.Model):
    iconID					= models.SmallIntegerField(primary_key=True)
    iconFile				= models.CharField(max_length=500)
    description				= models.CharField(max_length=1600)

    class Meta:
        db_table			= 'eveIcons'
        managed				= False

    def __unicode__(self):
        return unicode(self.iconID)

# ==================
# = mapDenormalize =
# ==================

class mapDenormalize(models.Model):
    itemID					= models.IntegerField(primary_key=True)
    typeID 					= models.ForeignKey('invTypes', db_column='typeID')
    groupID 				= models.SmallIntegerField()
    solarSystemID 			= models.IntegerField()
    constellationID 		= models.IntegerField()
    regionID				= models.IntegerField()
    orbitID					= models.IntegerField()
    x						= models.FloatField()
    y						= models.FloatField()
    z						= models.FloatField()
    radius					= models.FloatField()
    itemName				= models.CharField(max_length=100)
    security				= models.FloatField()
    celestialIndex			= models.SmallIntegerField()
    orbitIndex				= models.SmallIntegerField()

    class Meta:
        db_table	= "mapDenormalize"
        managed		= False

    def __unicode__(self):
        return unicode(self.itemID)

# ============
# = invFlags =
# ============

class invFlags(models.Model):
    flagID				= models.IntegerField(primary_key=True)
    flagName			= models.CharField(max_length=200)
    flagText		 	= models.CharField(max_length=200)
    orderID				= models.IntegerField()

    class Meta:
        db_table	= "invFlags"
        managed		= False

    def __unicode__(self):
        return unicode(self.flagID)
