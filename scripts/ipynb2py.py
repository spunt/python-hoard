import json
import os
import re
from glob import glob

def fileparts(fn):
    p,ne = zip(*[os.path.split(n) for n in fn])
    n,e = zip(*[os.path.splitext(n) for n in ne])
    return p,n,e

def files(pat, recursive=True):
    fn = glob(os.path.expanduser(pat), recursive=recursive)
    if fn:
        # fn = [os.path.join(os.getcwd(), n) for n in fn]
        fn = [os.path.abspath(n) for n in fn]
    return fn

def extractpy(nbfile):
    with open(nbfile) as data_file:
        ipynb = json.load(data_file)
    code = ""
    for c in ipynb["cells"]:
        if c["cell_type"] == "code":
            source = c["source"]
            for s in source:
                if s[0] != "%":
                    code += s.rstrip('\n') + "\n"
    return code   


outdir = os.path.join(os.getcwd(), 'ipynb2py')
os.mkdir(outdir)
nb = files('**/*ipynb')
path,name,ext = fileparts(nb)
py = [os.path.join(outdir, n + '.py') for n in name]

for idx, fn in enumerate(nb):
    
    code = extractpy(fn)
    with open(py[idx], 'w') as out_file:
        out_file.write(code)

