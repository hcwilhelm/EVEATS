import inspect
import logging

# internal class to get a logger including the function name
# we will cache our created loggers in a dict (_loggers) to
# speed it all up a little bit
class _FunctionLogger(object):
    def __init__(self):
        self._loggers = {}
  
    def _get_caller(self):
        frm = inspect.stack()[2]
        mod = inspect.getmodule(frm[0])
        return '%s.%s' % (mod.__name__, frm[3])
  
    def __getattr__(self, name):
        caller = self._get_caller()
        if caller not in self._loggers:
            self._loggers[caller] = logging.getLogger(caller)
        return getattr(self._loggers[caller], name)

# this will be used as logger in all functions
func_logger = _FunctionLogger()