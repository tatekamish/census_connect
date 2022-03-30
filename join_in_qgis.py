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

# execute request
r = requests.get(base_url, params=predicates)
print(r.json())
# col_names = ["name", "total_pop", "state", "county"] # renaming columns
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
theURL = 'https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_42_county10.zip'
fetchZip(theURL, outputDir)
print('{0}{1} created.'.format(outputDir, os.path.basename(theURL)))


#add shapefile to QGIS project
zip_path = '/vsizip/' + project_home + os.path.basename(theURL)
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