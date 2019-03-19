#repeat necessary steps until adding latlong
#import the necessary items 

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Parse the lxml to get the table Headers
# and each individual row of data
def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_headers = row.find_all('th')
        if table_headers:
            results.append([headers.get_text() for headers in table_headers])

        table_data = row.find_all('td')
        if table_data:
            results.append([data.get_text() for data in table_data])
    return results

# Filter out the junk lines, Not assigned Boroughs
# and replace the Not assigned Neighborhoods with
# the Borough name
def filter_rows(rows):
    """ Filter unwanted data from rows """
    index = 0
    results = []
    for row in rows:
      if row[0]:

         if row[0][0] == 'M' and row[1] != 'Not assigned' or index == 0:
            row[2] = row[2].replace("\n","")
            if row[2] == 'Not assigned':
               row[2] = row[1]
            results.append(row)
      index += 1
    return results

# Get the website as text
# Soup the web text into lxml
# Extract the table with a CSS class of wikitable sortable attribute
website_url = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M").text
soup = BeautifulSoup(website_url,'lxml')
My_table = soup.find('table',{'class':'wikitable sortable'})

# get The table rows
# parse the extra HTML/lxml junk from the rows
# Filter out junk and Not assigned Boroughs
codes = soup.find_all('tr')
Rcodes = parse_rows (codes)
Pcodes = filter_rows (Rcodes)

# Merge Neighborhoods with the same Postal code into one record
index = 0
while index < len(Pcodes):
   if Pcodes[index][0] == Pcodes[index-1][0]:
       Pcodes[index-1][2] += ", "
       Pcodes[index-1][2] += Pcodes[index][2]
       Pcodes.remove(Pcodes[index])
   else:
       index += 1


#use csv for lat longs as problems with geocoder
#defining the path of the csv file containing latlong for postalcode
path = ('C:\\Users\\ASUS\\Desktop\\Python\\PostCodeLatLong.csv')
#make a variable to hold the data
latlongs = pd.read_csv(path)


#covert dataframe into list
Pcodeloc = latlongs.values.tolist()

#iterate through both lists, assigning pcode to Pcodes and loc to Pcodeloc
# if the postal codes match then append the second and third element from loc to the Pcode element 

for pcode, loc in [(pcode,loc) for pcode in Pcodes for loc in Pcodeloc]:

   if pcode[0] == loc[0]:
       pcode.append(loc[1])
       pcode.append(loc[2])
       

junk = Pcodes.pop(0)

   
# make a Panda dataframe.
df = pd.DataFrame()

#add headers to dataset
df = pd.DataFrame(Pcodes,columns=['PostalCode','Borough','Neighborhood','Latitude','Longitude'])

print (df)

#view columns and rows of dataframe
df.shape




