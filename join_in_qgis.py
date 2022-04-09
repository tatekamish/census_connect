import os
import pandas as pd
import requests
from qgis.core import (QgsVectorLayer, QgsVectorFileWriter,
                       QgsProject, QgsVectorLayerJoinInfo)
from csv import QUOTE_NONNUMERIC
import urllib.request, urllib.error, urllib.parse

# setting working directory to project home
os.chdir(QgsProject.instance().readPath("./"))
project_home = os.getcwd()

HOST = "https://api.census.gov/data"
year = "2010"
dataset = "dec/sf1"
base_url = "/".join([HOST, year, dataset])
predicates = {}

# "for" counties "in" pennsylvania
get_vars = ["NAME", "P001001"]  # P001001 = population
predicates["get"] = ",".join(get_vars)  # get vars
predicates["for"] = "county:*"
predicates["in"] = "state:42"  # state code for Pennsylvania
#^other geography levels? 


# execute request
r = requests.get(base_url, params=predicates)
print(r.json())
# renaming columns
col_names = r.json()[0:1][-1]

df = pd.DataFrame(columns=col_names, data=r.json()[1:])
df["P001001"] = df["P001001"].astype(int)
#add a new field that is a concatenation of state + county ID (GEOID); this will be the join field
#or access columns by index df[number of variables requested:]

print(df[0:1])
print(col_names[-1])
print(df.columns[-1])


if df.columns[-1] == "state":
    csv_join_field = "state"
    shp_join_field = "STATEFP10"
elif df.columns[-1] == "county":
    df["GEOID"] = df["state"] + df["county"]
    csv_join_field = "GEOID"
else:
    pass


df.to_csv("table.csv", quoting = QUOTE_NONNUMERIC, index=False)


# add csv to QGIS project
#pop_table = r'file:///C:/Users/tuo25083/Documents/app_dev/census_connect/pa_county_pop.csv?delimiter=,'
csv = QgsVectorLayer(r'file:///' + project_home + '\\table.csv', 'table', 'delimitedtext')
QgsProject.instance().addMapLayer(csv)


def fetchZip(url, outputDir):
    '''Fetch binary web content located at 'url'
    and write it in the output directory'''
    response = urllib.request.urlopen(url)
    binContents = response.read()
    response.close()

    # Save zip file to output dir (write it in 'wb' mode).
    outFileName = outputDir + os.path.basename(url)
    with open(outFileName, 'wb') as outf:
        outf.write(binContents)

outputDir = project_home


#Get Geometry  (Function not completely finished--mostly unsure of local/global variables and what all needs to be in the function since theres a get zip and build url function)
def get_geo(tiger, geo_type, year, state):

    url_prefix="https://www2.census.gov/geo/tiger/" #Not User Input
    url_tiger= f"{tiger}"           # "TIGER####"
    url_geo_type = f"{geo_type}"    # "COUNTY", "STATE", etc. 
    url_year = f"{year}"            # "####"
    url_state = f"{state}"          #2-dig state code
    url_geo_lower = url_geo_type.lower() #used in url_suffix (file name)
    url_suffix="tl_{0}_{1}_{2}.zip".format(url_year,url_state,url_geo_lower)
    
    #not sure if this needs to be global for future referance
    geo_url = "{0}{1}/{3}/{4}/{5}".format(url_prefix, url_tiger, url_geo_type, url_year, url_suffix)
    #STATE ex: https://www2.census.gov/geo/tiger/TIGER2010/STATE/2010/tl_2010_01_state10.zip
    #theURL = 'https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_42_county10.zip' #original grab
   
    fetchZip(geo_url, outputDir) #change to geo_url once user input final
    print('{0}{1} created.'.format(outputDir, os.path.basename(geo_url)))

    print("FOR GIT HUB TO RECOGNIZE AS UPDATED TEXT DELTE LATER")
#add shapefile to QGIS project
#let's generalize this more, and turn into a function
zip_path = '/vsizip/' + project_home + os.path.basename(geo_url)
shp = QgsVectorLayer(zip_path, 'tl_2010_42_county10', 'ogr')
QgsProject.instance().addMapLayer(shp)

shp_join_field='GEOID10'

#make a function to join csv to shapefile

def join (shp, csv, shp_join_field, csv_join_field):
    joinObject=QgsVectorLayerJoinInfo()
    joinObject.setJoinFieldName(csv_join_field)
    joinObject.setTargetFieldName(shp_join_field)
    joinObject.setJoinLayerId(csv.id())
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(csv)
    shp.addJoin(joinObject)

join(shp, csv, shp_join_field, csv_join_field)

