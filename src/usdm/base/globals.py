from usdm.api import __all__ as api_classes
from usdm.base.id_manager import IdManager

class Globals():

  def __init__(self):
    self.errors = None
    self.id_manager = None

  def clear(self):
    self.id_manager = IdManager(api_classes)
    