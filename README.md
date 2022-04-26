# Census Connect QGIS Plugin
#### Download Census Geography and Tables Directly into QGIS
[Github Repository](https://github.com/tatekamish/census_connect)
Updated: April 25, 2022

## Description
Census Connect is a QGIS compatible plugin designed for the purpose of streamlining the workflow for retrieving, joining, and opening Census geography and tabular data directly within QGIS. While Census Connect is not yet available in the QGIS Plugin Repository, the code found within the Github repository is compatible within the QGIS Python Console. The current version of Census Connect is only capable of working with the Decennial Census Summary File (2000-2020).

## Getting Started

#### Dependencies
[**Pandas** ](https://pandas.pydata.org/docs/user_guide/index.html)(v1.2.4) **|** [**QGIS**](https://qgis.org/en/site/) (v3.18.3)

#### Installation
To get started:
1. Clone repository the census_connect github repository locally.
2. Once you have a local copy of the directory, use the envrironment.yml file to create an anaconda environment. for this project. This environment includes a copy of QGIS.
3. Within your newly created environment, launch QGIS.
4. Once QGIS launches open the Processing Toolbar. Click the Python icon at the top of the menu and select Open an existing script on the drop down menu.
5. Open census_connect_functions.py from your directory and run the entire script.
6. NOTE: On lines 46 and 86 you can configure which tables and geography you wish to download. As currently written this script will download Total Population for Tracts within Philadelphia County, Pennsylvania.

## Next Steps
* QGIS Repository Availability
* American Community Survey Compatibility
* Configurable File Storage
* Selectable sub-geographies, across multiple geographies (i.e. select specific counties across state lines)
* Select from multiple years in on call

## Authors
**Steven Francisco** | *[Github](https://github.com/stfran22)* <br>
**Tate Kamish** | *[Github](https://github.com/tatekamish)* <br>
**Casey Smith** | *[Github](https://github.com/caseysmithpgh)* <br>
## Version History
**v 0.1.9**
* Decennial Census, Summary File 1
* Collect multiple variables at once
* Not yet available within the QGIS Plugin repository
