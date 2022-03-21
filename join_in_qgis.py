import os
import pandas as pd
import requests
from qgis.core import (QgsVectorLayer, QgsVectorFileWriter,
                       QgsProject, QgsVectorLayerJoinInfo)

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
r_pa = requests.get(base_url, params=predicates)
print(r_pa.json())
# col_names = ["name", "total_pop", "state", "county"] # renaming columns
col_names = r_pa.json()[0:1]
print(col_names)
pa_df = pd.DataFrame(columns=col_names, data=r_pa.json()[1:])
pa_df.to_csv("census_connect_table.csv", index=False)


# add csv to QGIS project
#pop_table = r'file:///C:/Users/tuo25083/Documents/app_dev/census_connect/pa_county_pop.csv?delimiter=,'
csv = QgsVectorLayer(r'file:///' + project_home +
                     '\\census_connect_table.csv', 'table', 'delimitedtext')

# to keep leading zeros on join field (county)
# option 1: make schema.ini --> how do we soft code column number and name?
# option 2: add user input for join column number and name?

# csv.str.zfill(3)
QgsProject.instance().addMapLayer(csv)
#
# add shapefile to QGIS project
#zip_path = '/vsizip/C:/Users/tuo25083/Documents/app_dev/census_connect/tl_2010_42_county00.zip'
#shp = QgsVectorLayer(zip_path, 'tl_2010_42_county00', 'ogr')
# QgsProject.instance().addMapLayer(shp)
#
# join csv to shapefile
# csv_join_field='county'
# shp_join_field='COUNTYFP00'
# joinObject=QgsVectorLayerJoinInfo()
# joinObject.setJoinFieldName(csv_join_field)
# joinObject.setTargetFieldName(shp_join_field)
# joinObject.setJoinLayerId(csv.id())
# joinObject.setUsingMemoryCache(True)
# joinObject.setJoinLayer(csv)
# shp.addJoin(joinObject)
#
#
#
#
