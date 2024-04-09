

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize the instance if needed
        self.debug_enabled = None
        self.page = None
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# Example usage:
# singleton1 = Singleton.get_instance()
# singleton2 = Singleton.get_instance()

# print(singleton1 is singleton2)  # Output: True (singleton1 and singleton2 refer to the same instance)
