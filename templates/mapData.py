import requests
import urllib.parse
import pandas as pd
from geopy.geocoders import Nominatim

lat = []
lon = []
addresses = []
licenses = []

# create data doc
dataDoc = pd.read_csv("/home/jordan/Desktop/programmaticSEO/childCare/childData.csv")
for index, row in dataDoc.iterrows():
  address = row['Street'] + "," + row['City'] + ',' + row['State'] + "," + str(row['Zip']).replace(".0","")
  url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
  response = requests.get(url).json()
  try:
    addresses.append(response[0]["display_name"])
    licenses.append(row['License'])
  except IndexError:
    pass
  try:
    lat.append(response[0]["lat"])
  except IndexError:
    pass
  try:
    lon.append(response[0]["lon"])
  except IndexError:
    pass

# create address dict from geo data
geoData = {'License': licenses, 'ADDRESS': addresses, 'LATITUDE': lat, 'LONGITUDE': lon}

# create dataframe
geoData_df = pd.DataFrame.from_dict(geoData)

localDF = pd.merge(geoData_df, dataDoc, on='License', how='left')
localDF.to_csv('/home/jordan/Desktop/programmaticSEO/childCare/childDataLatLong.csv', index=False)