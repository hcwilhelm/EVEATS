# 
#  tree.py
#  EVEATS
#  
#  Created by Hans Christian Wilhelm on 2011-05-07.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

from django.http import HttpResponse
from django.core import serializers

# ===========================================================
# = Abstract Tree Class used as helper for complex queryies =
# ===========================================================

serializer     = serializers.get_serializer("json")()

class Node:
    def __init__(self, data="root"):
        self.data = data
        self.quantity = 0
        self.childs = []

    def insert(self, data):
        self.childs.append(Node(data))

    def find(self, data):
        node = None;

        if self.data == data:
            node = self

        else:            
            for child in self.childs:
                node = child.find(data)

        return node

    def create_quantity(self):
        
        if self.childs:
            for child in self.childs:
                child.create_quantity()
                self.quantity += child.quantity

        else:
            self.quantity = self.data.quantity

    def get_data(self):

        if self.data == "root":
            return {'typeName': 'root', 'quantity':self.quantity}

        else:
            location = None

            if self.data.locationID:
                location = self.data.locationID.itemName

            invTypeID = None

            if self.data.typeID.groupID.categoryID.categoryName == "Station" :
                invTypeID = self.data.locationID.typeID.typeID

            else :
                invTypeID = self.data.typeID.typeID

            return {
                'typeName':self.data.typeID.typeName,
                'quantity':self.quantity,
                'location': location,
                'flag':self.data.flag.flagName,
                'invTypeID': invTypeID,
                'categoryName': self.data.typeID.groupID.categoryID.categoryName
            }
            
    
    def serializable_object(self):
        obj = {'data':self.get_data(), 'childs':[]}

        for child in self.childs:
            obj['childs'].append(child.serializable_object())
            
        return obj