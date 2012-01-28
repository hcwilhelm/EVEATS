# 
#  router.py
#  EVEATS
#  
#  Created by Hans Christian Wilhelm on 2011-09-05.
#  Copyright 2011 scienceondope.org All rights reserved.
# 

class EveDBRouter(object):
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'evedb':
            return 'evedb'
        
        return None
        
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'evedb':
            return 'evedb'
        
        return None
        
    def allow_relation(self, obj_a, obj_b, **hints):
        if obj_a._meta.app_label == 'evedb' or obj_b._meta.app_label == 'evedb':
            return True
            
        return None
        
    def allow_syncdb(self, db, model):
        if db == 'evedb':
            return model._meta.app_label == 'evedb'
        elif model._meta.app_label == 'evedb':
            return False
        return None