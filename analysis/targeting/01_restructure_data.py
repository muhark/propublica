import pandas as pd
import sqlalchemy as sql
import json


# Part of the objective here is to create an operable metric for the `targets`
# column, which is currently relational.

db_engine = sql.create_engine("sqlite:///../../db/ad_database.sqlite3")
df = pd.read_sql(con=db_engine, sql="SELECT \"index\", targets FROM propublica;")
db_engine.dispose()

# Probably overkill to load the entire dataframe at the moment
df = df.set_index("index")
df.dropna(inplace=True)
df.loc[:,'json'] = df['targets'].apply(lambda x: json.loads(x))


# Each entry is a list of dictionaries.
# First step is to check that every dict contains a "target" key.

df['json'].apply(lambda x: all(["target" in d.keys() for d in x])).all()
# It does

# Now check what targets exist
# For each entry, get list of targets

df.loc[:, 'targets'] = df['json'].apply(lambda x: [d['target'] for d in x])

# Figured out a nice way to organise this
# Separate array for targeting information
# Each element contains a comma-separated string of targets
# One column contains total number of targets

# N_targets
df.loc[:, 'n_targets'] = df['targets'].apply(len)

# Generate list of unique targeting labels
targets = []
for entry in df['targets']:
    for item in entry:
        if item not in targets:
            targets.append(item)


# Let's now check the unique instances of each the targets
def target_parser(x, target):
    out = []
    for d in x:
        if d['target']==target:
            if 'segment' in d.keys():
                out.append(str(d['segment']))
            else:
                out.append(str(d['target']))
    out = ", ".join(out)
    return out

for target in targets:
    try:
        df[target] = df['json'].apply(lambda x: target_parser(x, target))
    except KeyError:
        print(target)

df = df.drop('json', axis=1)
df.loc[:, 'targets'] = df['targets'].astype(str)

# Let's save this into the database
df.to_sql(name="targets", con=db_engine, if_exists="replace")

# dict_keys = []
# for entry in df['json'].apply(lambda x: [d.keys() for d in x]):
#     for item in entry:
#         if item not in dict_keys:
#             dict_keys.append(item)

# df[df['json'].apply(lambda x:
#     ['target'] in [list(d.keys()) for d in x])]['json']
