from __future__ import division
import numpy as np
import pandas as pd
import sys
import re

file_name = sys.argv[1]

print("Reading file: " + file_name)

df = pd.read_csv(file_name)

df["candidate"] = df["candidate"].str.lower()

# develop regex conditional statements to change values
# into standard naming convention
def format_values(str):
    johnson = '(johnson)'
    obama = '(obama)'
    romney = '(romney)'
    stein = '(stein)'

    if re.search(johnson, str):
        return "johnson"
    elif re.search(stein, str):
        return "stein"
    elif re.search(romney, str):
        return "romney"
    elif re.search(obama, str):
        return "obama"
    else:
        return "other"

# call conditional regex function to format the values for each candidate
df["candidate"] = df["candidate"].map(format_values)

# ensure votes is an integer and nulls are set to 0
df["votes"] = df["votes"].fillna(0.0).astype(int)

# pivot table so candidates are dimensions and fips/county are index
df = df.pivot_table(index=["fips","county"],columns='candidate',values='votes')

# flatten column headers to index row - "level 0" the data
df = pd.DataFrame(df.to_records())

# calc total votes
df["totalvotes"] = df["obama"] + df["stein"] + df["johnson"] + df["romney"] + df["other"]

# calculate other dimensions
df["dPct"] = df["obama"]/df["totalvotes"]
df["rPct"] = df["romney"]/df["totalvotes"]
df["otherPct"] = df["other"]/df["totalvotes"]
df["dDRPct"] = df["obama"]/(df["obama"]+df["romney"])
df["rDRPct"] = df["romney"]/(df["obama"]+df["romney"])
df["leanD"] = df["obama"]/df["romney"]
df["leanR"] = df["romney"]/df["obama"]

# match column naming structure
df.rename(columns={"fips": "County", "county":"CountyName"}, inplace=True)

# pull out the state abbreviation from the filename
stateAbbr = file_name[:2]

# uppercase state abbreviation
df["StateAbbr"] =  stateAbbr.upper()

# define the out file name
file_name_out = stateAbbr + "_12.csv"

print("Writing to CSV...")

df.to_csv(file_name_out, index=False)

print("Script completed...")