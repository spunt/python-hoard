# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
from glob import glob
import os
import hashlib


class Files:

    def __init__(self, pattern, recursive=True, omitdirs=True, verbose=True):

        self.cwd = os.getcwd()
        self.pattern = os.path.expanduser(pattern)
        self.omitdirs = omitdirs
        self.recursive = recursive
        self.abs = glob(self.pattern, recursive=self.recursive)
        if self.abs:
            self.abs = [os.path.abspath(n) for n in self.abs]
            if self.omitdirs:
                self.abs = [s for s in self.abs if os.path.isfile(s)]
        print('{} item(s) found'.format(len(self.abs)))
        if any(self.abs):
            display(self.abs)
            self.path, self.file = zip(*[os.path.split(n) for n in self.abs])
            self.relpath = [i.replace(self.cwd, '') for i in self.abs]
            self.name, self.ext = zip(
                *[os.path.splitext(n) for n in self.file])
            self.file = list(self.file)
            self.path = list(self.path)
            self.name = list(self.name)
            self.ext = list(self.ext)

    def copy_as_unique(self, outdir=None):

        if not outdir:
            outdir = self.cwd
        if self.cwd not in outdir:
            outdir = os.path.join(self.cwd, outdir)
        if not os.path.exists(outdir):
            try:
                os.mkdir(outdir)
            except:
                print('Error creating directory: {}', outdir)

        outfile = [os.path.join(outdir, i.replace(self.cwd, '').replace(
            '/', '_').replace('__', '_')[1:]) for i in self.abs]

        from shutil import copy

        [copy(a, b) for a, b in zip(self.abs, outfile)]

    def move_as_unique(self, outdir=None):

        if not outdir:
            outdir = self.cwd
        if self.cwd not in outdir:
            outdir = os.path.join(self.cwd, outdir)
        if not os.path.exists(outdir):
            try:
                os.mkdir(outdir)
            except:
                print('Error creating directory: {}', outdir)

        outfile = [os.path.join(outdir, i.replace(self.cwd, '').replace(
            '/', '_').replace('__', '_')[1:]) for i in self.abs]

        from shutil import move

        [move(a, b) for a, b in zip(self.abs, outfile)]

    def remove(self):

        [os.remove(i) for i in self.abs]

    def get_zip_ext(self):

        ZIP = {'gz': 'gzip', 'bz2': 'bzip2', 'zip': 'zip',
               'tbz': 'tar:bz2', 'tar.bz2': 'tar:bz2', 'tb2': 'tar:bz2',
               'tgz': 'tar:gz', 'tar.gz': 'tar:gz'}
        """Return a string listing the accepted compressed format extensions."""
        return ", ".join(list(ZIP.keys()))

    def check_for_duplicates(self, hash=hashlib.sha1):

        def chunk_reader(fobj, chunk_size=1024):
            """Generator that reads a file in chunks of bytes"""
            while True:
                chunk = fobj.read(chunk_size)
                if not chunk:
                    return
                yield chunk

        def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
            hashobj = hash()
            file_object = open(filename, 'rb')

            if first_chunk_only:
                hashobj.update(file_object.read(1024))
            else:
                for chunk in chunk_reader(file_object):
                    hashobj.update(chunk)
            hashed = hashobj.digest()

            file_object.close()
            return hashed

        hashes_by_size = {}
        hashes_on_1k = {}
        hashes_full = {}

        for path in self.abs:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    try:
                        file_size = os.path.getsize(full_path)
                    except (OSError,):
                        # not accessible (permissions, etc) - pass on
                        pass

                    duplicate = hashes_by_size.get(file_size)

                    if duplicate:
                        hashes_by_size[file_size].append(full_path)
                    else:
                        # create the list for this file size
                        hashes_by_size[file_size] = []
                        hashes_by_size[file_size].append(full_path)

        # For all files with the same file size, get their hash on the 1st 1024 bytes
        for __, files in hashes_by_size.items():
            if len(files) < 2:
                continue    # this file size is unique, no need to spend cpy cycles on it

            for filename in files:
                small_hash = get_hash(filename, first_chunk_only=True)

                duplicate = hashes_on_1k.get(small_hash)
                if duplicate:
                    hashes_on_1k[small_hash].append(filename)
                else:
                    # create the list for this 1k hash
                    hashes_on_1k[small_hash] = []
                    hashes_on_1k[small_hash].append(filename)

        # For all files with the hash on the 1st 1024 bytes, get their hash on the full file - collisions will be duplicates
        for __, files in hashes_on_1k.items():
            if len(files) < 2:
                continue    # this hash of fist 1k file bytes is unique, no need to spend cpy cycles on it

            for filename in files:
                full_hash = get_hash(filename, first_chunk_only=False)

                duplicate = hashes_full.get(full_hash)
                if duplicate:
                    print("Duplicate found: {} and {}".format(
                        filename, duplicate))
                else:
                    hashes_full[full_hash] = filename
