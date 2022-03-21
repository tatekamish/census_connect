import os
from qgis.core import (QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsVectorLayerJoinInfo)

#add csv to QGIS project
pop_table = r'file:///C:/Users/tuo25083/Documents/app_dev/census_connect/pa_county_pop.csv?delimiter=,'
csv = QgsVectorLayer(pop_table, 'pa_county_pop', 'delimitedtext')
QgsProject.instance().addMapLayer(csv)

#add shapefile to QGIS project
zip_path = '/vsizip/C:/Users/tuo25083/Documents/app_dev/census_connect/tl_2010_42_county00.zip'
shp = QgsVectorLayer(zip_path, 'tl_2010_42_county00', 'ogr')
QgsProject.instance().addMapLayer(shp)

#join csv to shapefile
csv_join_field='county'
shp_join_field='COUNTYFP00'
joinObject=QgsVectorLayerJoinInfo()
joinObject.setJoinFieldName(csv_join_field)
joinObject.setTargetFieldName(shp_join_field)
joinObject.setJoinLayerId(csv.id())
joinObject.setUsingMemoryCache(True)
joinObject.setJoinLayer(csv)
shp.addJoin(joinObject)



             