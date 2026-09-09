"""
Merging the two leaderboards and deriving the shooting variables.
"""
import pandas as pd

shots = pd.read_csv("Total_Shots.csv")
sot = pd.read_csv("Shots_on_Target.csv")

df = shots.merge(sot[["Player", "SoT"]], on="Player", how="left")

# Accuracy needs both figures, so players missing SoT are excluded.
dropped = df[df["SoT"].isna()]
print(f"Excluded ({len(dropped)} players with shots but no published SoT):")
print(dropped[["Player", "Squad", "Shots"]].to_string(index=False), "\n")

df = df.dropna(subset=["SoT"]).copy()
df["SoT"] = df["SoT"].astype(int)

df["ShotAcc"] = (df["SoT"] / df["Shots"] * 100).round(2)
df["Shots90"] = (df["Shots"] / df["Min"] * 90).round(3)
df["SoT90"] = (df["SoT"] / df["Min"] * 90).round(3)

df = df.sort_values("ShotAcc", ascending=False).reset_index(drop=True)
df.to_csv("Players_Shot_Accuracy.csv", index=False)

print(f"Players with both figures: {len(df)} of {len(shots)}")
print(f"Mean shot accuracy: {df['ShotAcc'].mean():.2f}%\n")

# Ties are broken on SoT90 so the top 4 is a strict ranking.
top4 = df[df["Shots"] >= 15].sort_values(
    ["ShotAcc", "SoT90"], ascending=False
).head(4)

print("TOP 4 BY SHOT ACCURACY (15+ shots)")
print(top4[["Player", "Squad", "Shots", "SoT", "ShotAcc"]].to_string(index=False))
