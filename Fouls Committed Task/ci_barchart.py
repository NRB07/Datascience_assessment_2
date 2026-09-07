import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt

sample = pd.read_csv("sample_output.csv")

groups = ["Group Stage Exit", "Reached Knockouts"]
means = []
ci_errors = []  

for g in groups:
    x = sample.loc[sample["Stage"] == g, "Fls_per90"]
    mean = x.mean()
    sem = st.sem(x)
    ci_low, ci_high = st.t.interval(0.95, df=len(x) - 1, loc=mean, scale=sem)
    means.append(mean)
    ci_errors.append((ci_high - ci_low) / 2)  

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(groups, means, yerr=ci_errors, capsize=8, color=["#4C72B0", "#DD8452"])
ax.set_ylabel("Mean Fouls per 90 Minutes")
ax.set_xlabel("Tournament Stage")
ax.set_title("Mean Fouls per 90 Mins by Tournament Stage (with 95% CI)")

# Label each bar with its mean value
for bar, mean in zip(bars, means):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
             f"{mean:.2f}", ha="center", va="bottom")

plt.tight_layout()
plt.savefig("fouls_ci_barchart.png", dpi=150)
print("Saved fouls_ci_barchart.png")
print(f"Means: {dict(zip(groups, [round(m, 2) for m in means]))}")
print(f"CI half-widths: {dict(zip(groups, [round(e, 2) for e in ci_errors]))}")