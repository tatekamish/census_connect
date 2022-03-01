import requests
import pandas as pd

# setting up API request for summary file 1 from 2010 census
HOST = "https://api.census.gov/data"
year = "2010"
dataset = "dec/sf1"
base_url = "/".join([HOST, year, dataset])
predicates = {}

# specifying the variables we want 
get_vars = ["NAME", "P001001"] #P001001 = population
predicates["get"] = ",".join(get_vars) #get vars
predicates["for"] = "state:*" #for all states
# execute request
r = requests.get(base_url, params = predicates)

print(r.json()) # right now the data is a list of lists

col_names = ["name", "total_pop", "state"] # renaming columns

# converting json to dataframe
df = pd.DataFrame(columns = col_names, data = r.json()[1:])
df["total_pop"] = df["total_pop"].astype(int)  


# requesting population for specific city & state
HOST = "https://api.census.gov/data"
year = "2010"
dataset = "dec/sf1"
base_url = "/".join([HOST, year, dataset])
predicates = {}

get_vars = ["NAME", "P001001"] #P001001 = population
predicates["get"] = ",".join(get_vars) #get vars
predicates["for"] = "place:16000,14000" # city is classified as a place; code for Chicago
predicates["in"] = "state:17" # state code for Illinois
# execute request
r = requests.get(base_url, params = predicates)
print(r.text) 

                  