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


def get_table(get_vars, pred_for, pred_in, year):
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "dec/sf1"
    base_url = "/".join([HOST, year, dataset])
    predicates = {}
    predicates["get"] = ",".join(get_vars)  # get vars is a list of strings, ex. ["NAME", "P001001"]
    predicates["for"] = f"{pred_for}:*" #county:* or tract:*
    predicates["in"] = f"state:{pred_in}" #state:42 or state:*
    r = requests.get(base_url, params=predicates)
    col_names = r.json()[0:1][0]
    df = pd.DataFrame(columns=col_names, data=r.json()[1:])   
    geocols = list(df.columns)[len(get_vars):]
    df["GEOID"] = df[geocols].apply("".join, axis=1)    
    df.to_csv("table.csv", quoting = QUOTE_NONNUMERIC, index=False)
    out_file = open("table.csvt", "w")
    csvt_text = "Integer," * len(get_vars) + "String," * len(geocols)
    out_file.write(csvt_text)
    out_file.close()
    return df

df = get_table(["NAME", "P001001"], "county", "42", "2010")


#create csvt file: 
    #`"Integer",` * [get_vars].len() 
    
#df["P001001"] = df["P001001"].astype(int)
#add a new field that is a concatenation of state + county ID (GEOID); this will be the join field
#or access columns by index df[number of variables requested:]

# add csv to QGIS project
#pop_table = r'file:///C:/Users/tuo25083/Documents/app_dev/census_connect/pa_county_pop.csv?delimiter=,'
csv = QgsVectorLayer(r'file:///' + project_home + '\\table.csv', 'table', 'delimitedtext')
QgsProject.instance().addMapLayer(csv)


def fetch_zip(url, outputDir):
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
fetch_zip(theURL, outputDir)
print('{0}{1} created.'.format(outputDir, os.path.basename(theURL)))

#add shapefile to QGIS project
#let's generalize this more, and turn into a function
zip_path = '/vsizip/' + project_home + os.path.basename(theURL)
shp = QgsVectorLayer(zip_path, 'tl_2010_42_county10', 'ogr')
QgsProject.instance().addMapLayer(shp)

shp_join_field='GEOID10'
# 

#make a function to join csv to shapefile
def join_to_geog (shp, csv, shp_join_field):   
    joinObject=QgsVectorLayerJoinInfo()
    joinObject.setJoinFieldName("GEOID")
    joinObject.setTargetFieldName(shp_join_field)
    joinObject.setJoinLayerId(csv.id())
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(csv)
    shp.addJoin(joinObject)

join_to_geog(shp, csv, shp_join_field)

