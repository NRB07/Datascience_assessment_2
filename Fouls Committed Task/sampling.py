import pandas as pd

RANDOM_STATE = 42
SAMPLE_PER_GROUP = 60


df = pd.read_csv("wrangled_output.csv")

df["Fls_per90"] = df["Fouls Committed"] / df["90s played"]


print("Population size:", len(df))

# Stratified random sample: 60 players per group (Reached Knockouts / Group Stage Exit)
sample = pd.concat([
    grp.sample(n=SAMPLE_PER_GROUP, random_state=RANDOM_STATE)
    for _, grp in df.groupby("Stage")
])

print("Sample size:", len(sample))
print(sample["Stage"].value_counts().to_dict())

sample.to_csv("sample_output.csv", index=False)