import google.auth

__all__ = [
    'EmulatorCreds'
]


class EmulatorCreds(google.auth.credentials.Credentials):

    def __init__(self):
        self.token = b'secret'
        self.expiry = None

    @property
    def valid(self):
        return True

    def refresh(self, _):
        pass
