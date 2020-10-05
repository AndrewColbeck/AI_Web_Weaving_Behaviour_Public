import uuid


class Web(object):
    def __init__(self, resolution=20):
        self.id = str(uuid.uuid4())
        self.resolution = resolution
        self.strands = []
