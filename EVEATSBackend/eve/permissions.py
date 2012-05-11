# 
#  permissions.py
#  Backend
#  
#  Created by Hans Christian Wilhelm on 2012-04-21.
#  Copyright 2012 scienceondope.org All rights reserved.
# 

from permission import registry
from permission import PermissionHandler

from models import *

class CharacterAssetListPermissionHandler(PermissionHandler):
  
  def has_perm(self, user_obj, perm, obj=None):
    user_has_permission = False
    
    if perm == 'eve.viewAssetList_character':
      for key in obj.apiKeys.all():
        if key.user == user_obj:
          user_has_permission = True
    
    return user_has_permission

registry.register(Character, CharacterAssetListPermissionHandler)