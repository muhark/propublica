from cli_browser import *
from selenium.webdriver import Firefox
from os import getcwd

# TODO:
# - Handle IndexError
# - Handle SQL Errors
# - Multiline input SQL

CONN = '../db/ad_database.sqlite3'
ADFILE = getcwd() + '/adview.html'
LISTFILE = 'shortlist.txt'

driver = Firefox()
driver.get("file:///" + ADFILE)


def interact_query():
    accept_query = "n"
    while accept_query == "n":
        query = ""
        print("INPUT SQL QUERY: ")
        while ";" not in query:
            query += input() + "\n"
        data_subset = query_db(query=query, conn_string=CONN)
        accept_query = input("ACCEPT DATA? y[es]/n[o]: ")
    return data_subset


def read_action(data_size, active_row=0):
    action = input("Next/Previous/Close/Query/Shortlist/eXclude: ")
    if action == 'n':
        active_row += 1
    elif action == 'p':
        active_row -= 1
    elif action == 'c':
        return 'close', 0
    elif action == 'q':
        return 'query', 0
    elif action == 's':
        return 'shortlist', active_row
    elif action == 'x':
        return 'exclude', active_row
    else:
        print("INVALID INPUT.")
        return 'prompt', active_row
    if active_row < 0 or active_row > data_size:
        print("EXCEEDED ROWS. RETURNING TO ORIGINAL AD.")
        return 'prompt', 0
    return 'viewer', active_row


def generate_view(row, driver=driver):
    generate_ad(row, file=ADFILE)
    print_ad_summary(row)
    driver.get("file:///" + ADFILE)


if __name__ == '__main__':
    print("STARTING ADVIEWER.")
    active = True
    active_row = 0
    data = interact_query()
    while active:
        action, active_row = read_action(data.shape[0], active_row)
        if action == 'prompt':
            continue
        elif action == 'viewer':
            generate_view(data.iloc[active_row, :])
        elif action == 'shortlist':
            with open(LISTFILE, "a+") as shortlist:
                shortlist.write(data.iloc[active_row, :]['id'])
                shortlist.write("\n")
                shortlist.close()
            print(f"ID WRITTEN TO {LISTFILE}")
        elif action == 'exclude':
            exclude_advertiser(data.iloc[active_row, :]['advertiser'], conn_string=CONN)
            data = interact_query()
            active_row = 0
        elif action == 'query':
            data = interact_query()
            active_row = 0
        elif action == 'close':
            print("CLOSING ADVIEWER.")
            active = False
    driver.close()
    exit()
