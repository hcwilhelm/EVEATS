import inspect
import logging

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
  
func_logger = _FunctionLogger()