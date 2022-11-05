from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
from flask import Flask, render_template, request
from flask import send_file
import pandas as pd
import re

"""
home page logic:
return a list of cities sorted ABC ->
return a set of 10 cities per div / column
"""

app = Flask(__name__)

# global data variable
dataDoc = pd.read_csv("static/data/childDataLatLong.csv")

# create variables to use for city pages
states = []
cities = []

for index, row in dataDoc.iterrows():
    # establish URL syntax to use
    states.append(row['State'].lower())
    city = row['City'].lower()
    # Test removal of hyphen
    cities.append(city.replace(" ","-"))
    

# HOME PAGE ROUTE
@app.route('/')
def home():

    return render_template("home.html")



# INDEX PAGE
"""
This needs to point to the 
county / state index page
"""

@app.route("/index")
def index():
    """
    home page route that accepts child care data as a parameter
    """
    dataDoc
    # create a unique list of counties
    counties = list(dataDoc['Country'].unique())
    # blank dictionary
    indexNavDict = {}
    # appends each unique county to our indexNavDict
    for i in counties:
        indexNavDict[i] = None
    for county in counties:
        indexNavDict[county] = list(dataDoc.loc[dataDoc.Country == county]['City'].unique())

    citiesList = []
    for city in dataDoc.City.unique():
        city = city.lower()
        citiesList.append(city)
    
    # create city dictionary
    cityDict = {}
    # create variable that takes length of list
    cityLen = len(citiesList)
    # create keys variable from city length
    keys = range(cityLen)
    # loop through city list and create dictionary object
    for i in keys:
        # add items to dictionary and pair it to value sin list
        cityDict[i] = citiesList[i]
    
    
    # return render_template("index.html")
    return render_template("county-state-index.html",
    titleTag="Child Care Search",
    datasource=indexNavDict
    )
    

@app.route('/<state>/<city>')
def city_page(state,city):
    if city in cities:
        # filter to only use city specific data on page template
        data = pd.read_csv("static/data/childDataLatLong.csv") 
        city = city.upper()
        city = city.replace("-"," ")
        pageTitle = city.lower()
        pageTitle = pageTitle.title().replace("-"," ")
        dataSource = data.loc[data.City == f"""{city}"""]
        # total number of facilities
        allCenters = len(dataSource)
        # total number of child care facilities
        childCare = len(dataSource.loc[dataSource.Type == "Child Care Center"])
        # total number of family home centers
        familyCare = len(dataSource.loc[dataSource.Type == "Family Child Care Home"])
        # total number of subsidized
        enrolled = len(dataSource.loc[dataSource.subsidized == "Yes"])

        dataNav = pd.read_csv("static/data/indexNav.csv")
        County = dataSource['Country'].unique()
        County = str(County).replace("['","")
        County = County.replace("']","")
        County = re.sub(r"'.*","" , County)

        relatedCities = dataNav.loc[dataNav.Country == f"""{County}"""]

        cityMap = f"""/{city}_map.html"""

        # render AI blurb
        sentence = pd.read_csv("static/data/sentence.csv")
        sentence = sentence.loc[sentence.City == f"""{city}"""]

        """ if there is a match return City Landing Page Template"""
        # testing out swapping between various templates
        # city.html
        # city2.html
        return render_template("city-template.html",
        cityMap=cityMap,
        title=pageTitle,
        County=County,
        relatedCities=relatedCities,
        titleTag = "Child Care Facilities in " + pageTitle + ", NC",
        dataSource = dataSource,
        city=city,
        allCenters=allCenters,
        childCare=childCare,
        familyCare=familyCare,
        enrolled=enrolled,
        sentence=sentence
        )




if __name__ == '__main__':
    app.run()