import requests
from bs4 import BeautifulSoup

""" This is to scrape the teaming table on ARPA-H's program pages.
They seem to be using the same template. So, you should be 
able to use this code without any changes except the URL.
"""

url = 'https://arpa-h.gov/research-and-funding/programs/upgrade/teaming'
prettify_file = 'prettify.txt'      # for debugging, just in case
output_file = 'out.csv'             # save the teaming table to this file as a csv

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

with open(prettify_file,'w') as outFile:
    outFile.write(soup.prettify())

# The page has only 1 table. If there are more, you'll need to find the right one.
tables = soup.find_all('table')
if len(tables) > 1:
    print('More than 1 table found. Make sure you are using the right one')
table = tables[0]

for row in table.tbody.find_all('tr'):
    columns = row.find_all('td')

    # Some text has " in it. Replace that with ' since we'll use " to encapsulate the strings. Also replace \xa0 special character.
    # For some reason, they have a column named 'Alt' which is not needed. Remove that.
    # Some cells are empty and mess up alignment. So, remove those too.
    coltext = ['"'+ str(col.text).strip().replace('"','\'').replace('\xa0','') + '"' for col in columns if str(col.text).lower() != 'alt' and len(col.text.strip())]   
    outstr = ','.join(coltext)

    # Write to a csv file. Can be opened directly from Excel.
    with open(output_file,'a') as outFile:
        outFile.write(outstr+'\n')
