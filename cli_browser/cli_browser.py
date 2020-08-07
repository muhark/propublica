import pandas as pd
import sqlalchemy as sql
import json


def query_db(query, conn_string):
    """
    Initiates database connection and makes query.
    Returns dataframe.
    """
    engine = sql.create_engine('sqlite:///' + conn_string)
    print("CONNECTION ESTABLISHED WITH DATABASE.")
    data = pd.read_sql(con=engine, sql=query)
    engine.dispose()
    print(f"DATA RETRIEVED: {data.shape[0]} ROWS.")
    return data


def exclude_advertiser(advertiser, conn_string):
    engine = sql.create_engine('sqlite:///' + conn_string)
    conn = engine.connect()
    stmt = sql.sql.text(f"INSERT INTO blacklist VALUES ('{advertiser}')")
    conn.execute(stmt)
    engine.dispose()
    print(f"{advertiser} ADDED TO BLACKLIST.")


def print_ad_summary(row):
    """
    Prints summary of ad to STDOUT.
    """
    # First parse targets
    target_string = ""
    try:
        targets = json.loads(row['targets'])
    except TypeError:
        targets = []
    for target in targets:
        for key in target.keys():
            target_string += f"{target[key]}"
            target_string += "/"
        target_string += "\n            "
    # Then build string
    s = f"""
ID:         {row['id']}
TITLE:      {row['title']}
CREATED:    {row['created_at']}
PAID BY:    {row['paid_for_by']}
ADVERTISER: {row['advertiser']}
TARGETS:    {target_string}
POL PROB:   {"{:.6f}".format(row['political_probability'])}
TGT SCORE:  {"{:.3g}".format(row['targetedness'])}
"""
    print(s)


def generate_ad(row, file):
    """
    Generates html of ad.
    """
    template_head = """
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>\"""" + row['title'] + """\"</title>
    <meta name="generator" content="Jekyll v3.8.7">
    <meta property="og:title" content="Sample Advertisement">
    <meta name="author" content="Musashi Harukawa">
    <meta property="og:locale" content="en_US">
    <meta name="description" content="">
    <meta property="og:description" content="">
    <meta property="og:site_name" content="">
    <script type="application/ld+json">
        {
            "@type": "WebSite",
            "url": \"""" + file + """\",
            "headline": \"""" + row['title'] + """\",
            "name": "Sample Advertisement",
            "author": {
                "@type": "Person",
                "name": "Musashi Harukawa"
            },
            "description": "",
            "@context": "https://schema.org"
        }</script>
    <!-- End Jekyll SEO tag -->

    <link rel="stylesheet" href="webpage_files/style.css">
    <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.min.js"></script>
    <![endif]-->
</head>
"""
    out_html = template_head + row['html'] + "</html>"
    with open(file=file, mode="w") as f:
        f.write(out_html)
