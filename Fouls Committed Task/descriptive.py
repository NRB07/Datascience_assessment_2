import pandas as pd

sample = pd.read_csv("sample_output.csv")

overall = sample["Fls_per90"].describe().round(2)
by_group = sample.groupby("Stage")["Fls_per90"].describe().round(2).T

summary = pd.DataFrame({
    "Overall": overall,
    "Group Stage Exit": by_group["Group Stage Exit"],
    "Reached Knockouts": by_group["Reached Knockouts"],
})
summary = summary.loc[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]]
summary.index = ["Count", "Mean", "Std dev", "Min", "25th pct", "Median (50th)", "75th pct", "Max"]

print(summary)