# Lecture 3 — Data Visualization and Hypothesis Testing

---

## 0. The Big Picture — Where This Lecture Fits

Lecture 1 explained *why* Big Data matters and *what* makes it different. Lecture 2 explained *how* to process huge datasets at scale (MapReduce/Hadoop). This lecture answers the next natural question: **once you can access the data, how do you actually make sense of it — and how do you know whether what you're seeing is real or just noise?**

This lecture covers **three connected topics**, in increasing order of rigor:

```
1. Descriptive Statistics
   → quick numerical summaries (mean, std, min/max, quartiles)
        │
        ▼
2. Exploratory Data Analysis (EDA)
   → visualize the data BEFORE modelling, to catch patterns,
     relationships, and problems that summary numbers alone hide
        │
        ▼
3. Statistical Methods for Evaluation (Hypothesis Testing)
   → move beyond "eyeballing" a chart to a RIGOROUS, quantifiable
     test of whether an observed difference/pattern is statistically
     significant or could just be due to random chance
```

A central message of this lecture is: **statistics is not a one-off step — it runs through the entire Data Analytics Lifecycle.** It shows up during initial data exploration and preparation, during model building/planning (choosing the best input variables, assessing predictability), during evaluation of final models (is this model actually better than a guess, or better than a competing model?), and again after deployment (did the change we made actually have the desired real-world effect?).

---

## 1. Descriptive Statistics

- The starting point of almost any analysis is calling something like `.describe()` on your dataset, which returns: **count, mean, standard deviation (std), min, quartiles (25%/50%/75%), and max**.
- **Critical warning from the lecture: do not simply depend on these summary numbers.** Two datasets can have *nearly identical* descriptive statistics while looking completely different when actually visualized — meaning summary statistics alone can hide important structure, relationships, and even errors in your data.

> **Why this matters:** This single warning is the entire justification for the next section (EDA). If summary statistics told the full story, you wouldn't need to plot anything. The fact that they don't is why visualization is treated as a mandatory, not optional, step of analysis.

A well-known illustration of this exact point (referenced conceptually by the "four datasets, nearly identical statistics, but very different reality" example in the slides) is **Anscombe's Quartet** — four small datasets that share almost the same mean, variance, correlation, and regression line, yet look completely different when plotted (one is linear, one is curved, one has a clear outlier, one is nearly constant with one extreme point). It's a classic teaching example precisely because it proves that relying on numbers alone can be dangerously misleading.

---

## 2. Exploratory Data Analysis (EDA)

### 2.1 Why EDA matters

- The success of a data analysis project requires a **deep understanding of the data** — this requires a "toolbox" of basic statistical measures, graph/plot creation skills, and the ability to identify relationships and patterns.
- **Linear relationships and distributions are more difficult to detect from descriptive statistics alone** than from a well-chosen visualization.
- EDA helps **detect patterns and anomalies** in data through visualization, giving a **succinct, holistic view** that numbers cannot.
- Visualization is described as an important facet specifically at the **initial data exploration** stage — i.e., it's a *diagnostic* tool used early, not just a way to present final results.

### 2.2 Visualization Before Analysis

The core principle here: **look at your data visually before you start modelling it.** This catches problems (and reveals structure) that would otherwise bias or break your downstream analysis. Popular languages for this are **Python and R**, valued for their popularity and versatility (rich plotting ecosystems: `matplotlib`/`seaborn` in Python, `ggplot2`/base graphics in R).

### 2.3 Detecting "Dirty Data" via Visualization

- Visualization is one of the most effective ways to **detect dirty (i.e., erroneous, inconsistent, or implausible) data**.
- Method: look for **anomalies** in a plot (e.g., an unexpected spike, a value outside a plausible range), then **verify with domain knowledge** whether it's a real phenomenon or a data error, and **clean the data appropriately** if it is an error.
- **Example — Age Distribution histogram:** `hist(age, breaks=100, main="Age Distribution of Account Holders", xlab="Age", ylab="Frequency", col="gray")`. If this histogram showed, say, ages above 120 or negative ages, that would be an obvious red flag of dirty data that a `.describe()` table alone might not make as visually obvious.
- **Example — Mortgage Age histogram:** `hist(mortgage, breaks=10, xlab="Mortgage Age", col="gray", main="Portfolio Distribution, Years Since Origination")`. The lecture poses this as a "spot the dirty data" exercise — the key skill being trained here is pattern recognition: does the shape of the distribution make real-world sense for the domain (e.g., an implausible spike at a suspicious "round number" year might indicate default/placeholder values rather than real data)?

### 2.4 Visualizing a Single Variable

Several standard chart types for exploring one variable at a time:

| Chart | Purpose | Example (from lecture) |
|---|---|---|
| **Dotchart** | Shows individual values along a single axis, good for a moderate number of labeled items | `dotchart(mtcars$mpg, labels=row.names(mtcars), main="Miles Per Gallon (MPG) of Car Models")` |
| **Barplot** | Shows counts/frequencies of categorical values | `barplot(table(mtcars$cyl), main="Distribution of Car Cylinder Counts")` |
| **Histogram** | Shows the distribution (shape, spread, skew) of a continuous variable | `hist(income, breaks=500, xlab="Income", main="Histogram of Income")` |
| **Density plot** | A smoothed version of a histogram, useful when the raw histogram is noisy or the variable is highly skewed | `plot(density(log10(income), adjust=0.5), main="Distribution of Income (log10 scale)")` |

**Log transformation:** When a variable like income is heavily right-skewed (a few very large values dominate the visual range), plotting on a **log10 scale** compresses the range and reveals the underlying shape of the distribution far more clearly. A `rug()` plot (small tick marks along the axis showing individual data points) can be added underneath a density plot to show the raw data alongside the smoothed curve.

**Unimodal vs. multimodal:** Density plots are especially useful for answering the question "does this variable have one peak (unimodal) or multiple peaks (multimodal)?" — the lecture example plots diamond price density curves split (colored) by diamond `cut` category, both on the raw price scale and on a `log10(price)` scale, to see how the shape and modality differ once skew is removed.

### 2.5 Examining Multiple Variables

Moving from one variable to relationships *between* variables:

**a) Scatterplot with fitted trend lines**
```r
x <- runif(75, 0, 10); x <- sort(x)
y <- 200 + x^3 - 10*x^2 + x + rnorm(75, 0, 20)
lr <- lm(y ~ x)          # linear regression fit
poly <- loess(y ~ x)     # LOESS: local, nonlinear smoothing fit
fit <- predict(poly)
plot(x, y)
points(x, lr$coefficients[1] + lr$coefficients[2]*x, type="l", col=2)  # linear fit line
points(x, fit, type="l", col=4)                                        # LOESS fit line
```
This example is deliberately chosen because the true underlying relationship is **cubic** (`x^3` term), not linear. Plotting *both* a straight linear regression line and a flexible LOESS (locally weighted smoothing) line on the same scatterplot lets you visually compare: does a simple straight line capture the trend well, or is the relationship clearly curved/nonlinear? This is a key EDA skill — checking whether a linear model assumption is even reasonable before you commit to one.

**b) Dotchart with color as an extra dimension**
Using the `mtcars` dataset, cars are grouped and colored by number of cylinders (4 = red, 6 = blue, 8 = dark green) while plotting MPG. This illustrates using **color as an additional visual dimension** to encode a third categorical variable on top of a 2D plot — a very common EDA trick when you have more than two variables to compare at once.

**c) Grouped/side-by-side barplot**
```r
counts <- table(mtcars$gear, mtcars$cyl)
barplot(counts, main="Distribution of Car Cylinder Counts and Gears",
        xlab="Number of Cylinders", ylab="Counts",
        legend=rownames(counts), beside=TRUE)
```
This cross-tabulates two categorical variables (number of gears × number of cylinders) and plots them side by side (`beside=TRUE`), letting you compare counts across combinations of two categories at once — useful for spotting interaction patterns between categorical variables.

**d) Box-and-whisker plot**
```r
ggplot(data=DF, aes(x=as.factor(Zip1), y=log10(MeanHouseholdIncome))) +
  geom_point(aes(color=factor(Zip1)), alpha=0.2, position="jitter") +
  geom_boxplot(outlier.size=0, alpha=0.1)
```
Box-and-whisker plots summarize the distribution of a continuous variable (median, quartiles, spread, outliers) **across categories** (here, income across different zip codes). The example also demonstrates two useful refinements:
- **Jittering** points (`position="jitter"`) so overlapping data points don't stack exactly on top of each other and become invisible.
- Combining a **jittered scatterplot with an overlaid boxplot** to show both individual data points *and* the summary distribution shape at once.
- The example also shows the practical step of **removing outliers** (`subset(DF, DF$MeanHouseholdIncome > 7000 & DF$MeanHouseholdIncome < 200000)`) before plotting, to avoid extreme values distorting the visual scale.

**e) Hexbin plot (for large datasets)**
When you have *so many* data points that a regular scatterplot becomes an unreadable "blob" of overlapping dots, a **hexbin plot** divides the plotting area into hexagonal bins and shades each bin by how many data points fall inside it (essentially a 2D histogram). The example also overlays a linear regression line (`abline(lm(...))`) directly on the raw scatterplot for comparison. This chart type is specifically called out as useful **for large data** — a direct nod back to the "Volume" challenge from Lecture 1: standard scatterplots don't scale visually to millions of points, but hexbin plots do.

**f) Scatterplot matrix (pairs plot)**
```r
pairs(iris[1:4], main="Fisher's Iris Dataset",
      pch=21, bg=colors[unclass(iris$Species)])
```
A scatterplot matrix plots **every pair of variables** against each other in a grid, all at once — an efficient way to quickly scan for relationships (linear, nonlinear, or none) across *many* variable pairs simultaneously, rather than manually creating one scatterplot per pair. Coloring points by a categorical variable (here, iris species) additionally reveals whether relationships differ by category/group.

### 2.6 Data Exploration vs. Data Presentation

An important distinction raised in the lecture: **the same underlying data may need to be presented differently depending on the audience.**
- **Exploration** (what this lecture mostly focuses on) is for *you*, the analyst — quick, rough, iterative plots meant to help you understand the data, not to be pretty.
- **Presentation** is for *stakeholders* — polished, focused visuals meant to communicate a specific conclusion clearly, often stripped of exploratory clutter.
This connects to the Data Analytics Lifecycle concept mentioned earlier in the course — visualization plays a role at *both* the early exploration phase and the later "communicate results" phase, but with very different goals and styles at each stage.

### 2.7 Motivating Question: Comparing Before/After — Is a Simple Mean Comparison Enough?

The lecture poses two illustrative scenarios to set up the transition into hypothesis testing:

1. A company changes a product design and wants to know if **customer satisfaction** improved.
2. A data scientist changes a machine learning **model architecture** and wants to know if **results** improved.

In both cases, a naive approach is to just compute the **mean before** and the **mean after**, and see if the new mean is larger. **The lecture explicitly warns that this is not sufficient** — just because the new mean is numerically larger does *not* automatically mean the change is meaningfully/statistically better. This is exactly the gap that hypothesis testing is designed to fill.

---

## 3. Statistical Methods for Evaluation — Hypothesis Testing

### 3.1 Why Statistics Matters Throughout the Data Analytics Lifecycle

Statistics isn't confined to one phase — it recurs across the entire lifecycle:
- **Initial data exploration and data preparation** (this is explicitly tied to **Phase 2: Data Preparation** of the Data Analytics Lifecycle — hypothesis testing is used here to assess the *plausibility* of a hypothesis using sample data, where that sample may come from a larger population or from an ongoing data-generating process).
- **Model building and planning** — choosing the best input variables, assessing predictability.
- **Evaluation of final models** — is accuracy meaningfully better than a random guess, or better than a competing model?
- **Assessment of models after deployment** — does the model/change actually produce a sound, real-world effect once it's live?

### 3.2 Why a Simple Difference of Means Isn't Enough

- Comparing two population means is one of the most common types of hypothesis test, **but a simple comparison is often not sufficient on its own.**
- Example: imagine two populations, one with mean = -3 and another with mean = 3. Can we say the difference is "significant" just because the means differ? **The answer depends on the variance** of each population. If both populations have huge spread (variance), their value ranges might overlap enormously despite different means — making the "difference" much less meaningful/reliable than it first appears.

### 3.3 What Is Hypothesis Testing?

> **Definition (Hypothesis):** A supposition or proposed explanation made on the basis of limited evidence, as a starting point for further investigation.

The general procedure:
1. **Form an assertion** (a hypothesis) and test it using data.
2. The common starting assumption is that **there is no difference/effect** — this becomes the **Null Hypothesis (H₀)**.
3. The competing claim — that there *is* a difference/effect — becomes the **Alternative Hypothesis (H₁, sometimes written Hₐ)**.
4. A hypothesis is formed **before** validation — it defines expectations up front, which is what keeps the test objective (you're not just looking at the data and making up a story afterward).
5. The outcome of a hypothesis test is always one of two decisions: **reject H₀ in favor of H₁**, or **fail to reject H₀** (note: this is *not* the same as "proving H₀ is true" — more on this nuance below).

**Worked example (conceptual):** comparing the effect of Drug A vs. Drug B on patients.
- H₀: There is no difference in effect between Drug A and Drug B.
- H₁: There is a difference (or, in a directional test, Drug A is better than Drug B).

### 3.4 Visual Intuition: Overlapping Distributions

- If you plot the distributions of two populations being compared, **the more their distributions overlap, the less significant the difference between them appears.**
- Overlap is driven by two things: **how close the means are** (closer means → more overlap) and **how large the variances are** (larger variance/spread → more overlap).
- **Decision rule (intuitive version):** if the overlap is large, we tend to *accept* (fail to reject) the null hypothesis; if the overlap is small, we tend to *reject* the null hypothesis in favor of the alternative.
- This intuition is what the **Student's t-test** formalizes into an exact, quantifiable procedure.

### 3.5 Student's t-Test

**Assumptions:**
- The two populations being compared are assumed to have **equal, but unknown, variance**.
- Each population is assumed to be **normally distributed**.
- Under the null hypothesis, both populations share the **same mean**.

**The t-statistic:**
- If the assumptions hold, the test statistic **T** follows a **t-distribution** with **(n₁ + n₂ − 2) degrees of freedom**, where n₁ and n₂ are the sample sizes of the two groups.
- **The further T is from zero, the more significant the difference** between the populations appears. If |T| is large enough, we reject the null hypothesis.

**Significance level (α):**
- α is defined as the probability of **rejecting the null hypothesis when it is actually TRUE** — this is exactly the definition of a **Type I Error** (see Section 3.9).
- Setting α = 0.05 (the most common choice) means: we are willing to accept a 5% chance of wrongly rejecting a true null hypothesis.
- **Decision procedure:** find a critical value **T\*** such that P(|T| ≥ T\*) = α. Then: **reject H₀ if |T| ≥ T\***.

**Worked example logic (from the lecture):**
- In a two-sample t-test, a 95% confidence interval (CI) gives a range of values we believe, with 95% confidence, contains the *true difference* between the two population means.
- "Two-sided test" means we're testing for a difference in **either direction** — i.e., whether the true mean difference could be less than 0 *or* greater than 0 (as opposed to testing only one specific direction).
- **Decision check:** compare |T| to T\*. In the worked example, |T| = 1.7828, and T\* = 2.048407. Since 1.7828 is **not** ≥ 2.048407, there is **insufficient evidence to reject H₀** — so H₀ is **accepted** (i.e., not rejected).

**Understanding the p-value (two-sided test):**
- The significance level α actually corresponds to the **sum of both tails** of the distribution: P(T ≤ −t) + P(T ≥ t).
- Since there are two tails, the significance level **for each individual tail is α/2**.
- The **p-value** is the probability of observing a |T| at least as extreme as what we actually got, **assuming the null hypothesis is true**.
- **Decision rule using p-value:** if p-value > α, we do **not** reject H₀ (in the lecture's worked example: p-value = 0.08547 > α = 0.05, so we fail to reject H₀ — consistent with the T vs. T\* comparison above). If p-value ≤ α, we **reject** H₀.
- α = 0.05 is described as *"very common in statistics,"* but it is a convention, not a universal law — other fields sometimes use stricter (e.g., 0.01) or looser thresholds depending on the cost of errors.

### 3.6 One-Sided vs. Two-Sided t-Tests

| | One-sided test | Two-sided test |
|---|---|---|
| **When to use** | When you only care about a difference in *one specific direction* | When you care about a difference in *either* direction |
| **Example scenario** | A pharmaceutical company claims their new drug lowers blood pressure **more than** the standard drug | A company wants to know if a new packaging design **changes** average sales (could go up or down) |
| **H₀** | μ_new ≤ μ_standard (new drug does NOT lower BP more than standard) | μ_new = μ_standard (no difference in average sales) |
| **H₁** | μ_new > μ_standard (new drug DOES lower BP more) | μ_new ≠ μ_standard (there IS a difference, direction unspecified) |
| **Why this label** | The alternative hypothesis is **directional** — it only asks about one direction of effect | The alternative hypothesis is **non-directional** — it allows for a difference in either direction |

### 3.7 Student's t-Test vs. Welch's t-Test

- In software (e.g., R's `t.test()`), you may see an argument like `var.equal = TRUE`. This exists because the **Student's t-test formally requires the two populations to have equal variance.**
- **If the equal-variance assumption is not appropriate/justified, use Welch's t-test instead.**

**Welch's t-test:**
- Used when the **equal population variance assumption is NOT justified**.
- Instead of pooling the variance across both groups (as Student's t-test does), Welch's t-test **uses each population's own sample variance separately**.
- It **still assumes** both populations are normally distributed and share the same mean under H₀ — the *only* relaxed assumption compared to Student's t-test is the equal-variance requirement.

> **Practical rule of thumb:** if you're not sure whether your two groups have equal variance, Welch's t-test is generally the safer default, since it doesn't rely on an assumption you haven't verified.

### 3.8 Wilcoxon Rank-Sum Test (a Non-Parametric Alternative)

**Motivating question:** What if the two populations being compared are **not normally distributed**? Student's t-test (and Welch's t-test) both assume normality — if that assumption fails, their results become unreliable.

- **Parametric tests** (e.g., Student's t-test) make specific assumptions about the shape/distribution of the population(s) the samples are drawn from.
- **Nonparametric tests** (e.g., Wilcoxon Rank-Sum) make **no such distributional assumption** — they should be used when the populations cannot be assumed (or transformed, e.g., via log transform) to be normal.
- The Wilcoxon Rank-Sum test checks whether **two populations are identically distributed**, using the **ranks** of the combined data rather than the raw numerical values — this avoids needing any specific assumption about the shape of the distribution.

**Step-by-step procedure (as given in the lecture's worked example):**

Suppose we have:
- Group A: `[85, 80, 78, 90, 95]`
- Group B: `[88, 82, 85, 87, 92]`

1. **Combine and rank all the data together** (as if from one group):
   - Combined: `[85, 80, 78, 90, 95, 88, 82, 85, 87, 92]`
   - Ranks: `[4.5, 2, 1, 8, 10, 7, 3, 4.5, 6, 9]`
   *(Note: tied values — the two 85's — each receive the average of the ranks they would have occupied, hence 4.5.)*
2. **Sum the ranks for each group separately:**
   - Group A ranks: `[4.5, 2, 1, 8, 10]` → **W₁ = 4.5+2+1+8+10 = 25.5**
   - Group B ranks: `[7, 3, 4.5, 6, 9]` → **W₂ = 7+3+4.5+6+9 = 29.5**
3. **Choose the test statistic:** W can be taken as either sum, depending on the test's design — for a one-sided test, the **smaller** sum is typically used.
4. **Determine significance:** compare the chosen test statistic W to a critical value from the **Wilcoxon rank-sum distribution**, or compute a **p-value** directly using statistical software (e.g., `wilcox.test()` in R).

### 3.9 Type I and Type II Errors, and Statistical Power

| Error type | Definition | Also known as | Denoted by | How to reduce it |
|---|---|---|---|---|
| **Type I error** | **Rejecting** H₀ when H₀ is actually **TRUE** | False positive | **α** | Choose an appropriately strict significance level (e.g., lower α) |
| **Type II error** | **Accepting/failing to reject** H₀ when H₀ is actually **FALSE** | False negative | **β** | Increase sample size |

- **Statistical power** = **1 − β** = the probability of *correctly* rejecting a false null hypothesis.
- Power is used to help determine the **necessary sample size** for a study — the higher the power you want, generally the larger the sample size you need.

> **Intuition:** Type I and Type II errors represent a fundamental trade-off. Making your test stricter (lower α, harder to reject H₀) reduces the risk of a false positive but increases the risk of a false negative (missing a real effect), and vice versa. There's no way to eliminate both errors simultaneously without collecting more data (increasing sample size, which boosts power).

### 3.10 ANOVA (Analysis of Variance)

**Motivating question:** What if you need to compare **more than two** populations/groups at once? Running multiple pairwise t-tests becomes unwieldy and statistically problematic (the more pairwise tests you run, the higher your cumulative chance of a false positive purely by chance).

- **ANOVA is a generalization of hypothesis testing** to more than two groups.
- ANOVA tests whether **any** of the population means differ from the others (it does **not**, by itself, tell you *which* specific groups differ — see Tukey's HSD below for that).
- **Assumption:** each population/group is assumed to be **normally distributed** and to have the **same variance**.

**The F-test statistic:**
- ANOVA computes an **F-test statistic**, derived from two components:
  - **Between-groups mean sum of squares** — how much the group means vary from the overall mean.
  - **Within-groups mean sum of squares** — how much individual observations vary within each group.
- The F-statistic essentially measures **how different the group means are relative to the natural variability *within* each group**.
- **The larger the F-statistic, the greater the likelihood** that the observed difference in means is due to something *other than chance alone* (i.e., a real effect).
- The F-test statistic follows an **F-distribution**.

**Full assumptions of ANOVA:**
- **Normality:** data in each group should be approximately normally distributed.
- **Homogeneity of variances:** variances should be equal across groups (this can be formally checked with **Levene's test**).
- **Independence:** observations must be independent of one another.

**Limitations of ANOVA:**
- **Sensitive to outliers** — extreme values can distort the F-statistic and produce misleading conclusions.
- **Assumes equal variances** — if this is violated and not addressed, results can be invalid.
- **Identifies whether a difference exists, but not which specific groups differ** — you need an additional, follow-up ("post-hoc") test to pinpoint exactly which group(s) are different from which.
- When normality and/or equal-variance assumptions fail, **nonparametric alternatives** exist (analogous in spirit to how Wilcoxon Rank-Sum serves as the nonparametric alternative to the two-sample t-test).

### 3.11 Tukey's Honest Significant Difference (HSD) — Post-Hoc Testing

Used *after* ANOVA has shown a significant difference somewhere among the groups, to find out **specifically which pairs of groups differ**.

**Assumptions:**
- Normality, equal variance, and **approximately equal sample sizes across groups** (though Tukey's HSD can still be used, with some caution, even if sample sizes are unequal).

**Procedure:**
1. **Perform the ANOVA test first** to establish whether there is a significant difference somewhere among the group means. Only proceed to Tukey's HSD if the ANOVA null hypothesis (H₀: all means are equal) is **rejected**.
2. **Calculate the HSD value**, using: the critical value from the studentized range distribution, the mean square *within* groups (taken directly from the ANOVA calculation), and the number of groups being compared.
3. **Decision rule:** for **each pair** of group means, calculate the absolute difference between them, and compare that difference to the HSD value.
   - If the absolute difference **is greater than** the HSD value → that pair of means is considered **significantly different**.
   - If not → no significant difference is concluded for that specific pair.

---

## 4. Recap: Data Analytic Methods (as summarized in the lecture)

- **Descriptive statistics** — quick numerical summaries, but insufficient on their own.
- **Exploratory Data Analysis** — visualization before analysis; visualizing single variables (dotchart, barplot, histogram, density plot) and multiple variables (scatterplot + regression/LOESS, colored dotchart, grouped barplot, box-and-whisker, hexbin, scatterplot matrix).
- **Statistical Methods for Evaluation** — Hypothesis Testing:
  - Foundations: H₀ vs. H₁, significance level α, p-value, Type I/II errors, statistical power.
  - **Two-group comparisons:** Student's t-test (equal variance, normal), Welch's t-test (unequal variance, normal), Wilcoxon Rank-Sum test (non-normal, non-parametric).
  - **Multi-group comparisons:** ANOVA (tests if *any* group differs), followed by Tukey's HSD (post-hoc test to find *which* groups differ).

---

## 5. How This Connects to the Rest of the Course

- This lecture gives you the **analytical rigor** to complement the **infrastructure** from Lecture 2 (MapReduce/Hadoop) and the **conceptual framing** from Lecture 1 (why Big Data analytics matters, and the emphasis on extracting real *Value*).
- A key theme worth carrying forward: **visualization and hypothesis testing are not "final report" activities** — they are used *throughout* the Data Analytics Lifecycle, from the earliest data preparation stages through to assessing whether a deployed model or business change actually worked.
- Practically, expect future labs/assignments to ask you to: (1) visualize a dataset to detect anomalies or relationships before modelling, and (2) formally test a claim (e.g., "does variable X differ significantly between two groups?") using the appropriate test — choosing between t-test, Welch's t-test, Wilcoxon Rank-Sum, or ANOVA/Tukey's HSD based on the number of groups and whether normality/equal-variance assumptions hold.

---

## 6. Self-Check Questions

1. Why is it dangerous to rely only on `.describe()` summary statistics without visualizing your data?
2. In which phase of the Data Analytics Lifecycle is hypothesis testing explicitly mentioned as important, and why?
3. What are H₀ and H₁, and what does it mean to "reject" vs. "fail to reject" H₀?
4. What assumptions does Student's t-test require, and what should you use instead if the equal-variance assumption doesn't hold? What if normality also fails?
5. Explain the difference between a one-sided and a two-sided t-test, with an example of each.
6. Define Type I error and Type II error. How do you reduce each one, and what is the trade-off between them?
7. Why can't you just run multiple pairwise t-tests when comparing more than two groups? What should you use instead, and what does it tell you (and *not* tell you)?
8. What is the purpose of Tukey's HSD, and when should it be applied relative to ANOVA?
9. Walk through how to compute the Wilcoxon Rank-Sum statistic for two small samples, including how tied values are handled.
