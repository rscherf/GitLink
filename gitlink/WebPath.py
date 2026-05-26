from pathlib import PurePosixPath
from urllib.parse import quote


class Path(object):
    def __init__(self, *args, **kwargs):
        self.real_path = PurePosixPath(*args, **kwargs)

    @property
    def name(self):
        return quote(self.real_path.name)

    @property
    def parent(self):
        return quote(str(self.real_path.parent).lstrip('.'))

    def __str__(self):
        return quote(str(self.real_path))
