import pandas as pd
import sqlalchemy as sql
from res_lib.misc import get_logger


def main():
    """
    TODO: Make this a script that actually synchronises with online version.
    This script is designed to automatically check whether the data in the locally stored sql database is up-to-date.
    The script consists of three main parts:
    - Download the data.
    - Check if it has changed.
    - Update the sql database to reflect the changes.
    """


if __name__ == '__main__':
    new_data = pd.read_pickle("new_data.pkl")
    #new_data = pd.read_csv("https://fbpac-images.s3.amazonaws.com/fbpac/en-US.csv.gz")
    engine = sql.create_engine("sqlite:///ad_database.sqlite3")
    #old_data = pd.read_sql(con=engine, sql="SELECT * FROM ads;")

    # Merge data on id
    new_data.to_sql('propublica', con=engine)
    engine.dispose()