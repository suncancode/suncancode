"""
Task 3: Statistical evaluation
"""

import pandas as pd
from scipy import stats

# NOTE: Update this path to match where you saved yearly_sales.csv
FILE_PATH = r"D:\sun\WOLLONGONG\suncancode\S226\Big Data Analytics\Labs\Lab3\yearly_sales.csv"

sales = pd.read_csv(FILE_PATH, index_col=0)

# ---------------------------------------------------------
# Code 6: t-test (Male vs Female sales_total)
# ---------------------------------------------------------
ms = sales[sales["gender"] == "M"]["sales_total"]
fs = sales[sales["gender"] == "F"]["sales_total"]

t, p = stats.ttest_ind(ms, fs, equal_var=True)
print('t-test: t=', t.item(), 'p=', p.item())

# ---------------------------------------------------------
# Code 7: t critical value for a two-sided test at alpha=0.05
# ---------------------------------------------------------
n1 = ms.shape[0]
n2 = fs.shape[0]
df = n1 + n2 - 2
t005 = stats.t.ppf(q=1 - 0.05 / 2, df=df)
print('when p = 0.05, t=', t005)

# ---------------------------------------------------------
# Code 8: Welch's t-test (does not assume equal variance)
# ---------------------------------------------------------
t_welch, p_welch = stats.ttest_ind(ms, fs, equal_var=False)
print('Welchs t-test: t=', t_welch.item(), 'p=', p_welch.item())

# ---------------------------------------------------------
# Code 9: Wilcoxon Rank-Sum test (non-parametric, no normality assumption)
# ---------------------------------------------------------
_, t_wilcoxon = stats.ranksums(ms, fs)
print('Wilcoxon rank-sum test: t=', t_wilcoxon.item())

# Extra: also report p-value for the Wilcoxon test explicitly
res_wilcoxon = stats.ranksums(ms, fs)
print('Wilcoxon rank-sum test: statistic=', res_wilcoxon.statistic, 'p=', res_wilcoxon.pvalue)

# ---------------------------------------------------------
# Code 10: ANOVA test among Low / Medium / High order groups
# ---------------------------------------------------------
sales["order_group"] = pd.cut(
    sales["num_of_orders"],
    bins=[0, 1, 3, float("inf")],
    labels=["Low", "Medium", "High"]
)

low = sales[sales["order_group"] == "Low"]["sales_total"]
medium = sales[sales["order_group"] == "Medium"]["sales_total"]
high = sales[sales["order_group"] == "High"]["sales_total"]

# How many customers fall into each group? (useful context for interpreting the result)
print('group sizes -> Low:', low.shape[0], 'Medium:', medium.shape[0], 'High:', high.shape[0])

# One-way ANOVA: tests whether the means of the 3 groups are all equal
f_stat, p_anova = stats.f_oneway(low, medium, high)
print('ANOVA: F=', f_stat, 'p=', p_anova)

# Extra: if ANOVA is significant, Tukey's HSD tells us WHICH pairs of groups differ
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey_result = pairwise_tukeyhsd(
    endog=sales["sales_total"],
    groups=sales["order_group"],
    alpha=0.05
)
print(tukey_result)
