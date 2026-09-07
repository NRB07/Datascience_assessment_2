import pandas as pd
import numpy as np


df = pd.read_csv("raw_data.csv", encoding="latin1")

# Convert numeric columns
for col in ["Fouls Committed", "90s played", "Age"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Keep outfield players only (drop goalkeepers)
df["Pos_primary"] = df["Pos"].astype(str).str.split(",").str[0]
df = df[df["Pos_primary"] != "GK"]

# Drop players who never played
df = df.dropna(subset=["Fouls Committed", "90s played"])
df = df[df["90s played"] > 0]


df = df.drop_duplicates(subset=["Player", "Squad"])

# Clean squad names, tag knockout vs group-stage-exit
df["Squad_clean"] = df["Squad"].str.split(" ", n=1).str[1]

GROUP_STAGE_ELIMINATED = {"Haiti", "Tunisia", "Türkiye", "Jordan", "Panama", "Qatar",
    "Czechia", "Curaçao", "Iraq", "Uruguay", "Saudi Arabia", "New Zealand",
    "Scotland", "Uzbekistan", "Korea Republic", "IR Iran"}

df["Stage"] = np.where(df["Squad_clean"].isin(GROUP_STAGE_ELIMINATED),
                        "Group Stage Exit", "Reached Knockouts")

df.to_csv("wrangled_output.csv", index=False)
print("Final shape:", df.shape)
print(df["Stage"].value_counts())