import time
import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import plotly.graph_objects as go
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

geolocator = Nominatim(user_agent="arpah_app")

""" Scrape the awardees table data on ARPA-H's site.
"""

ARPAH_URL = 'https://arpa-h.gov/research-and-funding/mission-office-iso/awardees'
ARPAHDATA_FILE = 'arpadata.csv'     # for information from the project awardees table
PRETTIFY_FILE = 'prettify.txt'      # for debugging, just in case
LATLONG_FILE = 'latlong.csv'        # for saving latitude and longitude values
HTML_OUTPUT_FILE = 'arpah.html'

def get_arpa_data():
    """ Get information from the ARPA-H project awardees site
        Save this into a csv file
        Parameters: None
        Returns: None
    """

    url=ARPAH_URL
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    with open(PRETTIFY_FILE,'w') as outFile:
        outFile.write(soup.prettify())

    tables = soup.find_all("div",class_="block-awardees")
    if len(tables) > 1:
        print('More than 1 table found. Make sure you are using the right one')
    table = tables[0]

    colheaders = 'Amount,Location,Prime\n'
    with open(ARPAHDATA_FILE,'w') as outFile:
        outFile.write(colheaders)

    for row in table.find_all("div",class_="custom-award-row"):
        li_elements = row.find_all("li")
        for li_element in li_elements:
            litext = li_element.get_text(strip=True)
            if 'Amount Awarded' in litext:
                amttext = litext.replace('Amount Awarded','').strip()
                mitems = amttext.split('$')
                amount = mitems[1].replace('M','')
                amount = amount.replace('million','').strip()
            elif 'Prime' in litext:
                primetext = litext.replace('Prime Awardee Institution','').strip()
            elif 'Location' in litext:
                loctext = litext.replace('Location','').strip()
                coltext = '"' + amount + '","' + loctext + '","' + primetext + '"\n'

                # Write to a csv file. Can be opened directly from Excel.
                with open(ARPAHDATA_FILE,'a') as outFile:
                    outFile.write(coltext)

def get_lat_long(inDF):
    """ Obtain the latitude and longitude values for a list of cities in a dataframe
        Parameters: pandas dataframe containing a list of cities
        Returns: None
    """

    outstr = 'city,amount,prime,latitude,longitude\n'
    with open(LATLONG_FILE,'w') as outF:
        outF.write(outstr)

    for row in df.itertuples(index=False):
        amount = row[0]
        city = row[1]
        print('Found city = ',city)
        prime = row[2]

        time.sleep(1)       # try not to overload the OpenStreetMap servers
        try:
            location = geolocator.geocode(city)
            if location:
                latitude = str(location.latitude)
                longitude = str(location.longitude)
                outstr = '"' + city + '",' + str(amount) + ',"' + prime + '",' + latitude + ',' + longitude + '\n'
                with open(LATLONG_FILE,'a') as outF:
                    outF.write(outstr)
                print('..success')
            else:
                print(f"Could not find coordinates for {city}")
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Error: {e}")

def create_map():
    """ Create a map showing the lat/long of a city with a circle around it to indicate the funding amount.
        Larger circle represents larger amounts.
        Parameters: None
        Returns: None
    """

    df = pd.read_csv(LATLONG_FILE)
    df['marker_size'] = df['amount']

    fig = go.Figure(data=go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['city'] + '<br>Amount: $' + df['amount'].astype(str) + ' million' + '<br>Prime: ' + df['prime'].astype(str),
        hovertemplate = '<b>%{text}</b><extra></extra>',
        mode = 'markers',
        marker = dict(
            size = df['marker_size'],
            opacity = 0.5,
            colorscale = 'Viridis',
            color='black',
        )
    ))

    fig.update_layout(
        title = 'Size of circle directly proportional to funding amount. Hover for more details.',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            landcolor = "rgb(17, 217, 17)",
        ),
    )

    fig.show()
    fig.write_html(HTML_OUTPUT_FILE)

# Get data from ARPA-H website only if you don't have it already.
# This will prevent unnecessary requests to the server, which sometimes can be throttled

print('### Getting data from ARPA-H...')
file_path = Path(ARPAHDATA_FILE)
if file_path.is_file():
    print("File already exists with ARPA-H data. Skipping new request to server.")
else:
    get_arpa_data()

df = pd.read_csv(ARPAHDATA_FILE)

# Get data from OpenStreetMap server only if you don't have it already.
# This will prevent unnecessary requests to the server, which sometimes can be throttled

print('### Getting latitude and longitude data for cities')
file_path = Path(LATLONG_FILE)
if file_path.is_file():
    print("File already exists with lat/long data. Skipping new request to server.")
else:
    get_lat_long(df)

print('### Creating final map')
create_map()

