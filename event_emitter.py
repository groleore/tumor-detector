from const import EVENT_PREFIX


class EventEmitter:

    def __init__(self):
        self.EVENT_MAPPING = None

    def generate_mapping(self):
        self.EVENT_MAPPING = {self.get_event_name(f): f for f in dir(self) if self.is_event(f)}

    def emit(self, name, *args, **kwargs):
        if not self.EVENT_MAPPING:
            self.generate_mapping()
        return getattr(self, self.EVENT_MAPPING[name])(*args, **kwargs)

    def is_event(self, func: str):
        return func.startswith(EVENT_PREFIX) and callable(getattr(self, func))

    @staticmethod
    def get_event_name(func: str):
        return func[len(EVENT_PREFIX):]
