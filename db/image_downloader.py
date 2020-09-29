import pandas as pd
import requests
from time import sleep

df = pd.read_pickle('temp.pickle')[['id', 'images', 'targets']]
df = df[df['targets'].apply(lambda x: len(x) > 3)].copy()
df = df.iloc[8087:,:]

for i, row in enumerate(df.iterrows(), 1):
    if i%100==0:
        print("{:.3f}% complete".format(107158/i*100))
    try:
        url = row[1]['images'][1:-1]
        r = requests.get(url)
        with open(f"images/{row[1]['id']}.jpg", "wb+") as f:
            f.write(r.content)
    except requests.exceptions.MissingSchema:
        continue
    except requests.exceptions.ConnectionError:
        print(url)
        continue
