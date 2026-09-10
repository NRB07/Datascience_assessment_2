# FIFA World Cup 2026 – Defending Analysis

## Overview

This task analyses defensive performance using FIFA World Cup 2026 player statistics.

The main analytic question is:

**Among eligible players in the FIFA World Cup 2026, what was the average number of tackles won plus interceptions per 90 minutes, and was there a statistically significant difference between defenders and midfielders?**

## Data Source

The dataset was obtained from **FBref – FIFA World Cup 2026 Defensive Actions statistics**.

The original dataset contained **499 player records**.

The main variables used were:

- Player
- Position (Pos)
- Squad
- Age
- 90s played
- Tackles Won (TklW)
- Interceptions (Int)

## Data Preparation

The following steps were performed before the analysis:

1. Selected the variables required for the defensive analysis.
2. Checked the dataset for missing values and duplicate records.
3. Used the first listed position for players with multiple positions.
4. Selected defenders (DF) and midfielders (MF).
5. Excluded players who played less than 90 minutes.
6. After filtering, **276 eligible players** remained:
   - 130 Defenders
   - 146 Midfielders

## Performance Metric

The defensive performance metric used was:

**Tackles Won + Interceptions per 90**

The metric was calculated as:

`Defensive Actions per 90 = (TklW + Int) / 90s`

This allows players with different amounts of playing time to be compared more fairly.

## Sampling

Stratified random sampling was used to create a balanced sample.

- 40 Defenders
- 40 Midfielders
- Total sample size = 80 players
- Random state = 42

## Statistical Analysis

The analysis included:

- Descriptive statistics
- Mean and median
- Standard deviation
- 95% Confidence Interval
- Welch's Independent Two-Sample t-test

The significance level used for hypothesis testing was:

**α = 0.05**

## Results

| Result | Value |
|---|---:|
| Defender Mean | 2.375 |
| Midfielder Mean | 1.829 |
| Mean Difference | 0.546 |
| Overall Sample Mean | 2.102 |
| 95% Confidence Interval | 1.841 – 2.363 |
| Welch t-statistic | 2.128 |
| p-value | 0.0366 |

Since the **p-value (0.0366) was less than 0.05**, the null hypothesis was rejected.

The analysis found a **statistically significant difference** between defenders and midfielders, with defenders recording a higher average number of tackles won plus interceptions per 90 minutes.

## Limitations

- The metric only considers tackles won and interceptions and does not represent every aspect of defensive performance.
- Total tackles were not usable in the source data, so tackles won were used.
- Players with less than 90 minutes were excluded.
- The first listed position was used for multi-position players.
- The hypothesis test was conducted using a sample of 80 players rather than all 276 eligible players.

## Files

- `Defending_Analysis_Nirmal.ipynb` – Python notebook containing the complete analysis.
- Dataset – FIFA World Cup 2026 defensive statistics used for the analysis.
- Visualisations – Charts generated during the analysis.

## Author

**Nirmal Ranabhat**  
Group 11  
HIT140 – Assessment 2
