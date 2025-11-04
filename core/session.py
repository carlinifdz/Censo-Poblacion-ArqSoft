# core/session.py
class Session:
    _inst = None
    def __new__(cls):
        if not cls._inst:
            cls._inst = super().__new__(cls)
            cls._inst.user = None
            cls._inst.is_auth = False
        return cls._inst

    def login(self, username):
        self.user = username
        self.is_auth = True

    def logout(self):
        self.user = None
        self.is_auth = False

session = Session()
