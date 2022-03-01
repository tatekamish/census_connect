import requests
import pandas as pd

# setting up API request from ACS
HOST = "https://api.census.gov/data"
dataset = "acs/acs1"
# sex by age
get_vars = ["B01001_" + str(i + 1).zfill(3) + "E" for i in range(19)]
get_vars = ["NAME"] + get_vars
print(get_vars)

predicates = {} 
predicates["get"] = ",".join(get_vars)
predicates["for"] = "us:*"

# requesting same variables for multiple years
# initialize DataFrame collector
dfs = []
# request data for range of years and convert json to DataFrame
for year in range(2011, 2018):
    base_url = "/".join([HOST, str(year), dataset])
    r = requests.get(base_url, params = predicates)
    df = pd.DataFrame(columns = r.json()[0], data = r.json()[1:])
    # add column to hold the year value
    df["year"] = year
    dfs.append(df)

# concatenate all DataFrames in collector
us = pd.concat(dfs)
print(us.head())
