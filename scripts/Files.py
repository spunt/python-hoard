# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
from glob import glob
import os


class Files:

    def __init__(self, pattern, recursive=True, omitdirs=True):

        self.omitdirs = omitdirs
        self.recursive = recursive
        self.pattern = os.path.expanduser(pattern)
        self.abs = glob(self.pattern, recursive=self.recursive)
        if self.abs:
            self.abs = [os.path.abspath(n) for n in self.abs]
            if self.omitdirs:
                self.abs = [s for s in self.abs if os.path.isfile(s)]
        if any(self.abs):
            self.path, self.file = zip(*[os.path.split(n) for n in self.abs])
            self.name, self.ext = zip(
                *[os.path.splitext(n) for n in self.file])
            self.path = list(self.path)
            self.file = list(self.file)
            self.name = list(self.name)
            self.ext = list(self.ext)
