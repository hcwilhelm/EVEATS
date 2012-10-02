# ===========================================================================
# = Import general python modules                                           =
# ===========================================================================
from functools import wraps

# ===========================================================================
# = Import django modules                                                   =
# ===========================================================================
from django.core.cache import cache
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
# ===========================================================================
# = Decorator to allow only one update task for each object at time         =
# ===========================================================================

# TODO: FInd a way to get the logger! And log exceptions
LOCK_EXPIRE = 60 * 5        # Lock expires after 5 minutes
def locktask(function):
    @wraps(function)
    def wrapper(object, *args, **kwargs):
        lock_id = function.__name__ + "-" + str(object)
        acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
        release_lock = lambda: cache.delete(lock_id)
        
        if acquire_lock(): 
            try:
                logger.debug("Locked task: %s" % lock_id)
                return function(object, *args, **kwargs)
            #except Exception as ex:
                logger.error("Exception in Task: %s" % ex)
            finally:
                release_lock()
                logger.debug("Unlocked task: %s" % lock_id)
    
    return wrapper