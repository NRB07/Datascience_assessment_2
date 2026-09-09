
import io
import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt



# Loading and and cleaning data

"""Student note:
This section loads the World Cup data set and fixes some 
formatting issues in the  CSV so Python can extract and read
data correctly. Also only the relevant columns for the analysis were selected this step is important 
as not all of the data in the is required for the tasks."""

with open("world_cup_data.csv", encoding="latin1") as f:
    lines = f.readlines()

cleaned_lines = []

for line in lines[1:]:
    line = line.strip("\r\n")

    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]

    cleaned_lines.append(line)

df = pd.read_csv(io.StringIO("\n".join(cleaned_lines)))



# Only the relevant columns needed for the four analytical tasks are kept.
# Making the analysis focused on goalkeeper performance, playing time and workload.

df = df[["Player", "Squad", "Min", "GA90",
         "SoTA", "Saves", "Save%"]]


# These columns are converted to numbers so that calculations such
# as mean, standard deviation, confidence intervals and t-tests can be performed correctly.

for column in ["Min", "GA90", "SoTA", "Saves", "Save%"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# Saves per 90 minutes is calculated because Task 3 measures goalkeeper
# workload while still allowing differences in playing time making goal keepers more comparable with different play times.


df["Saves_per90"] = df["Saves"] / df["Min"] * 90



# Data set overview

print("DATASET OVERVIEW")
print("----------------")

print("Total goalkeepers:", len(df))
print("Valid Save%:", df["Save%"].notna().sum())
print("Undefined Save%:", df["Save%"].isna().sum())

print("Goalkeepers >180 minutes:",
      (df["Min"] > 180).sum())

print("Goalkeepers <=180 minutes:",
      (df["Min"] <= 180).sum())

print()

# The dataset overview shows how many goalkeepers are available
# and relevant for  Save% values. This is important because
# goalkeepers without a Save% cannot be included 

# The playing-time counts are useful for Task 4 because two sample t test uses
# goalkeepers from two different time zones >180 minute and
# <=180 minute.


# Creating figures folders

# The folder is created automaticaly even if
# it does not already exist.

os.makedirs("figures", exist_ok=True)



# TASK 1 — SAVE%


print("=" * 60)
print("TASK 1: SAVE%")
print("=" * 60)


"""Save% was selected for Task 1 because it measures how effective
 a goalkeeper is at stopping shots. The analysis uses a sample
of goalkeepers to make an inference about the broader group."""

# Remove missing Save% values
save = df["Save%"].dropna()


# Missing Save% values are removed because they cannot be used in the
# calculation or in the t-test.

# Creating random sample of 50
sample1 = save.sample(n=50, random_state=42)


# A random sample is used so that the goalkeepers are not
# selected biaselly based on their performance. Using
# random_state=42 means the same sample is selected each time
# the code is run.

print("Sample size:", len(sample1))
print("Mean Save%:", round(sample1.mean(), 2))
print("Median Save%:", round(sample1.median(), 2))
print("Standard deviation:", round(sample1.std(), 2))
print("Minimum:", round(sample1.min(), 2))
print("Maximum:", round(sample1.max(), 2))


# Calculating the mean median and standard deviation describe the centre
# and spread of Save% before carrying out the hypothesis test.


# 95% confidence interval
confidence_interval = stats.t.interval(
    0.95,
    len(sample1) - 1,
    loc=sample1.mean(),
    scale=stats.sem(sample1)
)

print("95% CI:",
      round(confidence_interval[0], 2),
      "to",
      round(confidence_interval[1], 2))

# The 95% confidence interval gives a range of reasonable values
# for the population mean Save% . It shows the uncertainty for
# the sample mean.


# One-sample t-test
t_stat, p_value = stats.ttest_1samp(sample1, 70)

# Using one-sample t-test   because the sample mean
# Save% is being compared with one specific value, 70% is a meaningful benchmark for goal keepers to be evaluated.


print("t-statistic:", round(t_stat, 3))
print("p-value:", round(p_value, 5))


# The p-value is compared with 0.05. If it is below 0.05,
# there is enough evidence to reject the null hypothesis.

if p_value < 0.05:
    print("Decision: Reject H0")
else:
    print("Decision: Fail to reject H0")

print()



# TASK 1 — SAVE FIGURE

# The histogram shows the distribution of Save% values in the sample. 


fig, axis = plt.subplots(figsize=(7, 4.5))

axis.hist(
    sample1,
    bins=10,
    color="#4C72B0",
    edgecolor="white"
)

axis.axvline(
    sample1.mean(),
    color="red",
    linestyle="--",
    label=f"Mean = {sample1.mean():.1f}%"
)

axis.axvline(
    70,
    color="black",
    linestyle=":",
    label="H0 = 70.0%"
)

axis.set_title("Task 1: Save% Distribution (n=50)")
axis.set_xlabel("Save%")
axis.set_ylabel("Frequency")
axis.legend()

plt.tight_layout()

# The figure is saved as a separate PNG file so it can be used for slides.

plt.savefig("figures/task1_save_pct.png", dpi=150)
plt.close()



# TASK 2 — GA90

print("=" * 60)
print("TASK 2: GA90")
print("=" * 60)


# GA90 measures goals conceded / missed per 90 minutes. It provides a
# standardised measure because goalkeepers may have played
# different amounts of time.

ga90 = df["GA90"].dropna()

# Missing GA90 values are removed because they cannot are not relevent
# in the statistical calculations.

# Sample of 50 selected
sample2 = ga90.sample(n=50, random_state=42)


# A random sample of 50 is used to make an inference about the
# wider group of goalkeepers. 50 because less than population.


print("Sample size:", len(sample2))
print("Mean GA90:", round(sample2.mean(), 3))
print("Median GA90:", round(sample2.median(), 3))
print("Standard deviation:", round(sample2.std(), 3))
print("Minimum:", round(sample2.min(), 3))
print("Maximum:", round(sample2.max(), 3))


# The descriptive statistics show the typical GA90 value and
# how much GA90 varies between the sampled goalkeepers.


# 95% confidence interval
confidence_interval = stats.t.interval(
    0.95,
    len(sample2) - 1,
    loc=sample2.mean(),
    scale=stats.sem(sample2)
)

print("95% CI:",
      round(confidence_interval[0], 3),
      "to",
      round(confidence_interval[1], 3))


# A 95% confidence interval estimates a reasonable range for the population mean GA90.



# One-sample t-test
t_stat, p_value = stats.ttest_1samp(sample2, 1.00)


# A one-sample t-test is used because the sample mean GA90 is
# being compared with one specific value 1.00 goal concededper 90 minutes.

print("t-statistic:", round(t_stat, 3))
print("p-value:", round(p_value, 5))

# The p-value is compared with the 0.05 significance level to
# choose whether there is enough evidence to reject the H0.

if p_value < 0.05:
    print("Decision: Reject H0")
else:
    print("Decision: Fail to reject H0")

print()


# TASK 2 — SAVE FIGURE


# The histogram shows how GA90 is distributed across the sample.
# The sample mean and hypothesised value are included for ease of visualisation
fig, axis = plt.subplots(figsize=(7, 4.5))

axis.hist(
    sample2,
    bins=10,
    color="#DD8452",
    edgecolor="white"
)

axis.axvline(
    sample2.mean(),
    color="red",
    linestyle="--",
    label=f"Mean = {sample2.mean():.2f}"
)

axis.axvline(
    1.00,
    color="black",
    linestyle=":",
    label="H0 = 1.0"
)

axis.set_title("Task 2: GA90 Distribution (n=50)")
axis.set_xlabel("Goals Conceded per 90 min")
axis.set_ylabel("Frequency")
axis.legend()

plt.tight_layout()
plt.savefig("figures/task2_ga90.png", dpi=150)
plt.close()


# TASK 3 — SAVES PER 90


print("=" * 60)
print("TASK 3: SAVES PER 90")
print("=" * 60)


# Saves per 90 was selected to measure goalkeeper workload converting saves to a per-90-minute rate makes the comparison
# better because goalkeepers played different amounts of time.

saves90 = df["Saves_per90"].dropna()


# Any missing calculated values are removed because they are not
# included in the statistical analysis.

# Random sample of 50
sample3 = saves90.sample(n=50, random_state=42)


# A random sample of 50 is used so the analsis is based on a
# consistent sample of goalkeepers rather than selecting players
# manually.

print("Sample size:", len(sample3))
print("Mean Saves/90:", round(sample3.mean(), 3))
print("Median Saves/90:", round(sample3.median(), 3))
print("Standard deviation:", round(sample3.std(), 3))
print("Minimum:", round(sample3.min(), 3))
print("Maximum:", round(sample3.max(), 3))


#The descriptive statistics show the typical number of saves
# per 90 minutes and how much goalkeeper workload differs.


# 95% confidence interval
confidence_interval = stats.t.interval(
    0.95,
    len(sample3) - 1,
    loc=sample3.mean(),
    scale=stats.sem(sample3)
)

print("95% CI:",
      round(confidence_interval[0], 3),
      "to",
      round(confidence_interval[1], 3))

# The confidence interval estimates a range for the
# population mean number of saves per 90 minutes.


# Doing one-sample t-test
t_stat, p_value = stats.ttest_1samp(sample3, 3.00)


# A one-sample t-test is used because the sample mean is being
# compared with a specific value to 3.00 saves per 90 minutes.

print("t-statistic:", round(t_stat, 3))
print("p-value:", round(p_value, 5))

# The p-value is compared with 0.05 to determine whether there
# is enough statistical evidence t reject the null hypothesis.

if p_value < 0.05:
    print("Decision: Reject H0")
else:
    print("Decision: Fail to reject H0")

print()



# TASK 3 — SAVE FIGURE
# Creating histogram shows the distribution of goalkeeper workload.
# The sample mean and hypothesised value are included to make
# the statistical comparison easier to see.

fig, axis = plt.subplots(figsize=(7, 4.5))

axis.hist(
    sample3,
    bins=10,
    color="#55A868",
    edgecolor="white"
)

axis.axvline(
    sample3.mean(),
    color="red",
    linestyle="--",
    label=f"Mean = {sample3.mean():.2f}"
)

axis.axvline(
    3.00,
    color="black",
    linestyle=":",
    label="H0 = 3.0"
)

axis.set_title("Task 3: Saves/90 Distribution (n=50)")
axis.set_xlabel("Saves per 90 min")
axis.set_ylabel("Frequency")
axis.legend()

plt.tight_layout()
plt.savefig("figures/task3_saves_per90.png", dpi=150)
plt.close()


# TASK 4 — SAVE% BY PLAYING TIME

print("=" * 60)
print("TASK 4: SAVE% BY PLAYING TIME")
print("=" * 60)


# Task 4 investigates whether goalkeeper playing time is associated
# with differences in Save%. The goalkeepers are divided into two
# groups based on whether they played more than 180 minutes or
# 180 minutes and less.

# Remove goalkeepers wtih missing Save%.
valid = df[df["Save%"].notna()]


# Creating the two playing-time groups.
high_minutes = valid[valid["Min"] > 180]["Save%"]
low_minutes = valid[valid["Min"] <= 180]["Save%"]


# The two groups are created so that the mean Save% of goalkeepers
# with lower and higher  playing times can be compared.


# Taking the required samples.
sample_high = high_minutes.sample(
    n=35,
    random_state=42
)

sample_low = low_minutes.sample(
    n=15,
    random_state=42
)

# Random samples of 35 and 15 goalkeepers are taken from the two groups

print(">180 minutes")
print("Sample size:", len(sample_high))
print("Mean Save%:", round(sample_high.mean(), 2))
print("Standard deviation:", round(sample_high.std(), 2))

print()

print("<=180 minutes")
print("Sample size:", len(sample_low))
print("Mean Save%:", round(sample_low.mean(), 2))
print("Standard deviation:", round(sample_low.std(), 2))

# Calculating confidence intervals.

print()
ci_high = stats.t.interval(
    0.95,
    len(sample_high) - 1,
    loc=sample_high.mean(),
    scale=stats.sem(sample_high)
)

ci_low = stats.t.interval(
    0.95,
    len(sample_low) - 1,
    loc=sample_low.mean(),
    scale=stats.sem(sample_low)
)

print("95% CI (>180 min):",
      round(ci_high[0], 2), "to", round(ci_high[1], 2))

print("95% CI (<=180 min):",
      round(ci_low[0], 2), "to", round(ci_low[1], 2))

print()
# The means and standard deviations are calculated separately
# because the two playing-time groups may have different levels
# of performance and variation so Welch method was used.


# Welch two-sample t-test
t_stat, p_value = stats.ttest_ind(
    sample_high,
    sample_low,
    equal_var=False
)
# Welch's two-sample t-test is used to compare means
# of two independent groups without assuming that their variances
# are equal.

print("Welch t-statistic:", round(t_stat, 3))
print("p-value:", round(p_value, 5))

# The p-value is compared to 0.05 to determine whether three is
# enough evidence to conclude that the two groups have different
# mean Save% values.

if p_value < 0.05:
    print("Decision: Reject H0")
else:
    print("Decision: Fail to reject H0")

print()


# TASK 4 — SAVE FIGURE
# The two histograms allow the Save% distrbutions of the two
# playingtime groups to be compared. Different colours distinguish groups
# to see.

fig, axis = plt.subplots(figsize=(7, 4.5))

axis.hist(
    sample_high,
    bins=10,
    alpha=0.7,
    color="#4C72B0",
    edgecolor="white",
    label="> 180 min"
)

axis.hist(
    sample_low,
    bins=10,
    alpha=0.7,
    color="#DD8452",
    edgecolor="white",
    label="<= 180 min"
)

axis.set_title("Task 4: Save% by Playing-Time Group")
axis.set_xlabel("Save%")
axis.set_ylabel("Frequency")
axis.legend()

plt.tight_layout()
plt.savefig("figures/task4_group_comparison.png", dpi=150)
plt.close()



# Anlysis finished

print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

print("Four figures have been saved in the 'figures' folder:")
print("1. task1_save_pct.png")
print("2. task2_ga90.png")
print("3. task3_saves_per90.png")
print("4. task4_group_comparison.png")


