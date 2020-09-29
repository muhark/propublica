import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from collections import Counter


engine = create_engine("sqlite:///../db/ad_database.sqlite3")
df = pd.read_sql("SELECT * FROM ads WHERE targets IS NOT NULL;", engine)

# Goal is to see what tasks might be possible. Let's pick apart the targetings column.
df['targets'] = df['targets'].apply(lambda x: json.loads(x))

df['target_and_segment'] = df['targets'].copy()
df['targets'] = df['target_and_segment'].apply(lambda x: [entry['target'] for entry in x if 'target' in entry.keys()])
df['segment'] = df['target_and_segment'].apply(lambda x: [entry['segment'] for entry in x if 'segment' in entry.keys()])

df.to_pickle("../db/temp.pickle")


targets = df['target_and_segment'].sum()

# Unique Keys:
a = [list(x) for x in [entry.keys() for entry in targets]]
b = list()
for item in a:
    b += item
set(b)
del a, b, item

# Unique targets
Counter([item['target'] for item in targets])

def browse_targets(targets, target):
    out = pd.Series(Counter([item['segment'] for item in targets if item['target']==target])).sort_values()
    return out

# Possible: Predict Targetings based on Image?
