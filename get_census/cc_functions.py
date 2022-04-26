import os
import pandas as pd
import requests
from qgis.core import (QgsVectorLayer, QgsVectorFileWriter,
                       QgsProject, QgsVectorLayerJoinInfo)
from csv import QUOTE_NONNUMERIC
import urllib.request, urllib.error, urllib.parse


project_home = QgsProject.instance().absolutePath()


def get_table(get_vars, pred_for, pred_in, year, table_name = "table"):
    '''
    This function is used to make the Census API request, convert the resulting JSON into 
    a pandas dataframe, and export the dataframe to the project home as a CSV along with
    a CSVT file to reinforce datatypes.
    
    Required Input: the desired variables from the Census Bureau in the form of a list, the
    geography level i.e. 'county' or 'tract', and the containing geography in the form
    of a state FIPS code or '*' indicating all states.
    
    Optional Input: desired name for the CSV output. If omitted, defaults to 'table.csv'
    '''
    
    HOST = "https://api.census.gov/data"
    year = f"{year}"
    dataset = "dec/sf1"
    base_url = "/".join([HOST, year, dataset])
    predicates = {}
    predicates["get"] = ",".join(get_vars)  
    predicates["for"] = f"{pred_for}:*" 
    predicates["in"] = f"state:{pred_in}" 
    r = requests.get(base_url, params=predicates)
    col_names = r.json()[0:1][0]
    df = pd.DataFrame(columns=col_names, data=r.json()[1:])   
    geocols = list(df.columns)[len(get_vars):] 
    df["GEOID"] = df[geocols].apply("".join, axis=1)    
    df.to_csv(f"{table_name}.csv", quoting = QUOTE_NONNUMERIC, index=False)
    out_file = open(f"{table_name}.csvt", "w")
    csvt_text = '"Integer",' * len(get_vars) + '"String",' * (len(geocols)) + '"String"'
    out_file.write(csvt_text)
    out_file.close()
    return table_name

def fetchZip(geo_url):
    '''Fetch binary web content located at 'geo_url'
    and write it in the output directory'''
    response = urllib.request.urlopen(geo_url)
    binContents = response.read()
    response.close()
    
    outfile = os.path.basename(geo_url)
    with open(outfile, 'wb') as outf:
        outf.write(binContents)

def get_geo(geo_level, year, state):
    project_home = QgsProject.instance().absolutePath()
    url_prefix="https://www2.census.gov/geo/tiger/" 
    url_tiger= "TIGER{}".format(year)          
    url_geo_level = geo_level.upper()   
    url_year = year            
    url_state = state         
    url_geo_lower = geo_level + f"{year[2:]}" 
    url_suffix="tl_{0}_{1}_{2}.zip".format(url_year,url_state,url_geo_lower)
    shp_join_field='GEOID{}'.format(year[2:])
    geo_url = "{0}{1}/{2}/{3}/{4}".format(url_prefix, url_tiger, url_geo_level, url_year, url_suffix)
    fetchZip(geo_url) 
    return geo_url, url_suffix, shp_join_field




def join_to_geog (shp, csv, shp_join_field):   
    '''
    Joins the CSV to the geometry and loads the layers to QGIS project.
    
    Required Input: shapefile, CSV, shapefile join field i.e. the common field
    between the CSV and shapefile that will be used to perform the join.
    '''
    
    joinObject=QgsVectorLayerJoinInfo()
    joinObject.setJoinFieldName("GEOID")
    joinObject.setTargetFieldName(shp_join_field)
    joinObject.setJoinLayerId(csv.id())
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(csv)
    shp.addJoin(joinObject)

