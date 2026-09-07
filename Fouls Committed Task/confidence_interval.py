import pandas as pd
import scipy.stats as st

sample = pd.read_csv("sample_output.csv")

x = sample["Fls_per90"]
n = len(x)
mean = x.mean()
sem = st.sem(x)  # standard error of the mean

ci_low, ci_high = st.t.interval(0.95, df=n - 1, loc=mean, scale=sem)

print(f"Sample size: {n}")
print(f"Sample mean: {mean:.2f}")
print(f"95% Confidence Interval: ({ci_low:.2f}, {ci_high:.2f})")