#!/usr/local/bin/python3

import shutil
import glob
import re

# use glob to grab all mp4 files in current directory
infile = glob.glob('**/*csv', recursive=True)
outfile = [x.split('/') for x in infile]
outfile = ['_'.join(x) for x in outfile]
[shutil.move(a, b) for (a, b) in zip(infile, outfile)]

# compile pattern for re
pattern = re.compile('_\d{1,2}.mp4')

# use list comprehension to construct new filenames
outfile = [re.sub(pattern, '.mp4', a) for a in infile]

# use list comprehension with shutil and zip to execute the move/rename
[shutil.move(a, b) for (a, b) in zip(infile, outfile)]
