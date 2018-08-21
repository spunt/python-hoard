# this assumes you have local json files generated from the Google BigQuery Tables get API:
# https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/get

from glob import glob
import pandas as pd
import numpy as np

fnames = glob('*json')
def extract_schema(fn):

    df0 = pd.read_json(fn)
    ref = '.'.join(df0.tableReference.values[[2,0,3]].tolist())
    df = pd.DataFrame(df0.schema.fields)
    df['table'] = ref
    df = df[['table', 'name', 'type']]
    return df

df = pd.DataFrame()
for fn in fnames:
    df = df.append(extract_schema(fn))

df.to_excel('table_schemas.xlsx')


