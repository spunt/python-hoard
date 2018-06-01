import pandas as pd
from PyPDF2 import PdfFileMerger
import glob

allpdf = glob.glob("*pdf")
pdfsplit = [x.split('-ch') for x in allpdf]
df = pd.DataFrame(pdfsplit)
courses = list(df[0].unique())

for course in courses:
    pdf = glob.glob(course + '*pdf')
    pdf.sort()
    merger = PdfFileMerger()
    [merger.append(x) for x in pdf]
    merger.write(course + '.pdf')
