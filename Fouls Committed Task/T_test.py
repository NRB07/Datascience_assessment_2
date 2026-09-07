import pandas as pd
import scipy.stats as st

sample = pd.read_csv("sample_output.csv")

knockout = sample.loc[sample["Stage"] == "Reached Knockouts", "Fls_per90"]
group_exit = sample.loc[sample["Stage"] == "Group Stage Exit", "Fls_per90"]

# Check equal-variance assumption first
levene_stat, levene_p = st.levene(knockout, group_exit)
equal_var = levene_p > 0.05

# Two-sample t-test
t_stat, p_val = st.ttest_ind(knockout, group_exit, equal_var=equal_var)

print(f"Reached Knockouts mean: {knockout.mean():.2f} (n={len(knockout)})")
print(f"Group Stage Exit mean: {group_exit.mean():.2f} (n={len(group_exit)})")
print(f"Levene's test p-value: {levene_p:.4f} -> {'equal' if equal_var else 'unequal'} variances assumed")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_val:.4f}")

alpha = 0.05
if p_val < alpha:
    print(f"Result: p < {alpha}, reject H0 - significant difference between the two groups.")
else:
    print(f"Result: p >= {alpha}, fail to reject H0 - no significant difference between the two groups.")