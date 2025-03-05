class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        name = cls.__name__
        print(f"SINGLETON __class__ 1: {cls.__name__} {cls._instances}")
        if name not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[name] = instance
        print(f"SINGLETON __call__ 2: {cls._instances}")
        return cls._instances[name]
    
    @classmethod
    def clear(cls, the_cls):
        print(f"SINGLETON clear 1: {cls._instances}")
        name = the_cls.__name__
        del cls._instances[name]
        print(f"SINGLETON clear 2: {cls._instances}")
