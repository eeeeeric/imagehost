class ImageHost():
    """Base class for all image hosts"""

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def upload(self, *args, **kwargs):
        pass
        
