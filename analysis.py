
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ALPHA = 0.05
TEAL, GOLD, NAVY, RED = "#0E7C86", "#D4A843", "#1B2A4A", "#B03A2E"

pop = pd.read_csv("Players_Shot_Accuracy.csv")
sample = pop.sample(n=30, random_state=42)
sample.to_csv("Random_Sample_Analysis.csv", index=False)

print(f"Population = {len(pop)} players, sample = {len(sample)}\n")


def one_sample(x, mu0, name, unit=""):
    n = len(x)
    mean, sd = x.mean(), x.std(ddof=1)
    t, p = stats.ttest_1samp(x, mu0)
    lo, hi = stats.t.interval(0.95, n - 1, mean, sd / np.sqrt(n))
    decision = "Reject H0" if p < ALPHA else "Fail to reject H0"

    print(f"--- {name} (H0: mu = {mu0}) ---")
    print(f"n = {n}")
    print(f"Mean = {mean:.3f}{unit}")
    print(f"Std deviation = {sd:.3f}{unit}")
    print(f"95% CI = {lo:.3f}{unit} to {hi:.3f}{unit}")
    print(f"t = {t:.3f}, p = {p:.5f}")
    print(f"Decision: {decision}\n")
    return mean, mu0


def histogram(x, mean, mu0, title, xlabel, colour, filename):
    plt.figure(figsize=(5, 3.1), dpi=200)
    plt.hist(x, bins=8, color=colour, edgecolor="white")
    plt.axvline(mean, color=RED, ls="--", label=f"Mean = {mean:.2f}")
    plt.axvline(mu0, color=NAVY, ls=":", label=f"H0 = {mu0:.2f}")
    plt.title(title, fontsize=9.5, fontweight="bold")
    plt.xlabel(xlabel, fontsize=8.5)
    plt.ylabel("Number of players", fontsize=8.5)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# Task 1: shot accuracy against the 40% target-hitting benchmark
m, h = one_sample(sample["ShotAcc"], 40.0, "Task 1: Shot accuracy", "%")
histogram(sample["ShotAcc"], m, h, "Task 1: Shot Accuracy (n=30)",
          "Shot accuracy (%)", TEAL, "task1_shot_accuracy.png")

# Task 2: shooting workload
m, h = one_sample(sample["Shots90"], 3.0, "Task 2: Shots per 90")
histogram(sample["Shots90"], m, h, "Task 2: Shots per 90 (n=30)",
          "Shots per 90 minutes", GOLD, "task2_shots_per90.png")

# Task 3: on target output
m, h = one_sample(sample["SoT90"], 1.0, "Task 3: Shots on target per 90")
histogram(sample["SoT90"], m, h, "Task 3: Shots on Target per 90 (n=30)",
          "Shots on target per 90", NAVY, "task3_sot_per90.png")

# Task 4: does accuracy differ between high and low volume shooters?
high = pop[pop["Shots"] >= 15].sample(n=15, random_state=42)["ShotAcc"]
low = pop[pop["Shots"] < 15].sample(n=18, random_state=42)["ShotAcc"]

t, p = stats.ttest_ind(high, low, equal_var=False)
print("--- Task 4: Accuracy by shot volume (H0: mu1 = mu2) ---")
for label, g in [(">= 15 shots", high), ("< 15 shots", low)]:
    lo, hi = stats.t.interval(0.95, len(g) - 1, g.mean(),
                              g.std(ddof=1) / np.sqrt(len(g)))
    print(f"{label}: n = {len(g)}, mean = {g.mean():.2f}%, "
          f"sd = {g.std(ddof=1):.2f}%, 95% CI = {lo:.2f}% to {hi:.2f}%")
print(f"Welch t = {t:.3f}, p = {p:.4f}")
print("Decision:", "Reject H0" if p < ALPHA else "Fail to reject H0")

plt.figure(figsize=(5, 3.1), dpi=200)
means = [high.mean(), low.mean()]
labels = [">= 15 shots\n(n=15)", "< 15 shots\n(n=18)"]
errors = [g.std(ddof=1) / np.sqrt(len(g)) * stats.t.ppf(0.975, len(g) - 1)
          for g in (high, low)]
plt.bar(labels, means, yerr=errors, color=[TEAL, GOLD], capsize=6, width=0.5)

# Show each player so the overlap between the two groups is visible.
rng = np.random.default_rng(42)
for i, g in enumerate([high, low]):
    plt.scatter(i + rng.uniform(-0.13, 0.13, len(g)), g, s=16,
                color=NAVY, alpha=0.45, zorder=3)
for i, (m, e) in enumerate(zip(means, errors)):
    plt.text(i, m + e + 2.5, f"{m:.1f}%", ha="center", fontweight="bold", fontsize=9)

plt.title("Task 4: Shot Accuracy by Shot Volume", fontsize=9.5, fontweight="bold")
plt.ylabel("Shot accuracy (%)", fontsize=8.5)
plt.ylim(0, 75)
plt.tight_layout()
plt.savefig("task4_group_comparison.png")
plt.close()

print("\nFigures saved.")
