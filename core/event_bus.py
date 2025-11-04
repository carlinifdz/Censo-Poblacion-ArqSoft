# core/event_bus.py
class EventBus:
    def __init__(self):
        self._subs = {}
        self.debug = False  # pon True para ver prints

    def subscribe(self, event, fn):
        self._subs.setdefault(event, []).append(fn)
        if self.debug:
            print(f"[BUS] subscribed {event} -> {getattr(fn, '__name__', fn)}")

    def emit(self, event, *args, **kwargs):
        if self.debug:
            print(f"[BUS] emit {event}")
        for fn in self._subs.get(event, []):
            try:
                fn(*args, **kwargs)
            except Exception as e:
                print(f"[BUS] listener error on {event}: {e}")

bus = EventBus()
# bus.debug = True
