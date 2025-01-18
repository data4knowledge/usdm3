class APIInstance():

    def __init__(self, globals):
        self._globals = globals

    def create(self, klass, params):
        try:
          klass_name = klass if isinstance(klass, str) else klass.__name__
          params['id'] = self.globals.id_manager.build_id(klass_name)
          params['instanceType'] = klass_name
          return klass(**params)
        except Exception as e:
          self._general_exception(f"Failed to create {klass_name} object", e)
          return None
