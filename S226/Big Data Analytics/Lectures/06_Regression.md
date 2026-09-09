# Regression

## 1. Problem Setup: Classification vs Regression

Predictive modelling problems fall into two broad types:

- **Classification** — predicting a discrete class label (e.g. spam / not spam).
- **Regression** — predicting a continuous quantity (e.g. house price, demand).

Regression analysis is used to explain the influence that a set of input variables has on the outcome of another variable of interest.

## 2. Linear Regression

### 2.1 Motivation and Model Formulation

We want a function that maps input variables to a continuous outcome:

```
y ≈ f(x1, x2, ..., xp)
```

Real-world outcomes are never perfectly deterministic — unobserved factors always introduce noise. This is made explicit with a random error term:

```
y = f(x1, ..., xp) + ε
```

Linear regression chooses the simplest useful form for `f`: a linear combination of the coefficients (not necessarily of the raw inputs — transformed inputs, e.g. `x²`, are still allowed):

```
y = β0 + β1*x1 + β2*x2 + ... + βp*xp + ε
```

Where:
- `y` — outcome variable
- `x_j` — input variables (j = 1, ..., p−1)
- `β0` — value of `y` when every `x_j = 0` (intercept)
- `β_j` — change in `y` per one-unit change in `x_j`, holding other inputs fixed
- `ε` — random error term (the model is non-deterministic; it produces an *expected value* of the outcome, not a guaranteed one)

### 2.2 Estimating the Coefficients: Ordinary Least Squares (OLS)

Given observed data, we need a criterion to pick the "best" coefficients. OLS minimizes the total squared distance between predicted and observed values:

```
min Σ (yi − (β0 + β1*xi))²
```

Squaring prevents positive and negative errors from cancelling out, and penalizes larger errors more heavily. OLS itself makes **no assumptions about the distribution of the error term** — it is purely a geometric optimization (minimizing distance from data points to the fitted line/hyperplane).

### 2.3 Additional Assumptions for Statistical Inference

To go beyond just fitting a line — to test whether coefficients are meaningful — linear regression adds assumptions on top of OLS:

```
ε ~ N(0, σ²), and the εs are independent of each other
```

i.e. errors are normally distributed, mean zero, constant variance (homoscedasticity), and independent. These assumptions are what make p-values, confidence intervals, and hypothesis tests valid.

### 2.4 Worked Example (R)

```r
income_input <- as.data.frame(read.csv("c:/data/income.csv"))
results <- lm(Income ~ Age + Education + Gender, income_input)
summary(results)
```

Model: `Income = β0 + β1·Age + β2·Education + β3·Gender + ε`

Reading the coefficient table:
- **Estimate** — the OLS-fitted β_j.
- **Std. Error** — how much the estimate would vary across different samples.
- **t value** = Estimate / Std. Error.
- **Pr(>|t|)** (p-value) — under H0: β_j = 0 (the variable has no effect), the probability of observing a t value this extreme by chance alone. A small p-value is evidence against H0.

In the example, `Age` and `Education` are highly significant (p < 2e-16); `Gender` is not (p = 0.134) — meaning the data does not provide strong evidence that Gender affects Income in this model. A non-significant coefficient could be dropped, but statistical evidence should be combined with domain knowledge before deciding.

### 2.5 Handling Categorical Variables Correctly

**Incorrect approach:** assigning arbitrary numeric codes to categories (e.g. alphabetical ordering) implies a false ordering and equal spacing between categories that doesn't exist.

**Correct approach:** for a categorical variable with `m` possible values, add `m − 1` binary (dummy) variables to the model.

Example — `Region` ∈ {North, Central, South}:
- `is_Central` = 1 if Central, else 0
- `is_South` = 1 if South, else 0
- When both are 0, the observation is implicitly `North` (the baseline/reference category)

```
y = β0 + β1·is_Central + β2·is_South + ...
```

- `β0` = expected `y` for the baseline category (North)
- `β1` = difference between Central and North
- `β2` = difference between South and North

**Why m − 1, not m?** If all `m` dummies were included, they would sum to 1 for every observation (`is_North + is_Central + is_South = 1`), making one variable perfectly predictable from the others. This creates perfect multicollinearity (the "dummy variable trap") and makes the design matrix singular — OLS cannot produce a unique solution. Dropping one category removes the redundancy.

### 2.6 Diagnostics — Validating a Fitted Model

Because all the statistical inference in §2.3–2.4 depends on the assumptions holding, they must be checked using the residuals (`residual_i = y_i − ŷ_i`, an observable proxy for the unobservable ε).

**a) Evaluating the linearity assumption**
- Plot the outcome variable against each input variable (or residuals against fitted values).
- If the relationship is not linear:
  - Transform the outcome or input variables (e.g. `log(y)`, since `y = a·e^(bx)` becomes linear after taking logs: `ln(y) = ln(a) + bx`).
  - Add extra input variables, e.g. `age²` (polynomial regression). This is still linear regression because it remains linear *in the coefficients* — `age` and `age²` are simply treated as two separate input variables. A negative coefficient on the squared term produces an inverted-U shape (e.g. income rising then falling with age); a positive coefficient produces a U shape.

**b) Evaluating residuals (residuals vs. fitted / vs. x)**
- Good model: residuals scatter randomly around zero with no pattern and constant spread.
- A curved pattern → linearity is violated (missing non-linear structure).
- A funnel/cone shape (spread increasing or decreasing) → heteroscedasticity (non-constant variance), which invalidates the p-values and confidence intervals even though OLS point estimates may still be reasonable.

**c) Evaluating the normality assumption (QQ-plot)**
```r
qqnorm(results2$residuals, ylab="Residuals", main="")
qqline(results2$residuals)
```
- Compares the quantiles of the residuals against the theoretical quantiles of a normal distribution.
- Points lying close to the 45° reference line → residuals are approximately normal.
- Systematic deviation, especially in the tails → heavier tails / skew than a normal distribution, meaning statistical inference (p-values, CIs) is less trustworthy.

**d) Other considerations**
- Consider all candidate input variables early in the analysis.
- Be careful when adding more variables: R² can increase (or stay the same) even from adding a useless variable — use **Adjusted R²** instead for fair comparison across models with different numbers of predictors.
- Linear regression is sensitive to outliers (points markedly different from the majority) since squared errors penalize them heavily.
- Sanity-check the sign and magnitude of estimated coefficients against domain knowledge.

## 3. Logistic Regression

### 3.1 Why a Different Model Is Needed

Linear regression assumes a continuous outcome. When the outcome is categorical (e.g. churn/no churn), directly applying `y = β0 + β1x + ε` fails for two reasons:
1. `β0 + β1x` can range over all of `(−∞, ∞)`, but a probability must lie in `[0, 1]`.
2. The `ε ~ N(0, σ²)` assumption no longer makes sense for a binary outcome.

### 3.2 The Logistic (Sigmoid) Function

To constrain the output to `[0, 1]`, logistic regression models the *probability* of the outcome through the sigmoid function:

```
P(y=1|x) = 1 / (1 + e^(−z)),  where z = β0 + β1x1 + ... + βp*xp
```

As `z → −∞`, `P → 0`; as `z → +∞`, `P → 1` — producing the characteristic S-shaped curve.

### 3.3 Log-Odds (Logit) Formulation

Since `P` itself is bounded and can't be modelled directly as a linear function, we transform it via the **odds** (`P/(1−P)`, ranging over `[0, ∞)`) and then the **log-odds** (logit), ranging over all of `(−∞, ∞)`:

```
ln(P / (1 − P)) = β0 + β1x1 + β2x2 + ... + βp*xp
```

This restores a linear form on the transformed scale, while the sigmoid function converts it back to a valid probability.

### 3.4 Parameter Estimation: Maximum Likelihood Estimation (MLE)

Because the relationship between `P` and `z` is non-linear (through the sigmoid), OLS's closed-form solution no longer applies. Instead, **Maximum Likelihood Estimation** is used: it finds the parameter values that maximize the probability of observing the given dataset (the *likelihood*). This requires iterative numerical optimization rather than a direct formula.

Example: `y = 3.50 − 0.16·Age + 0.38·Churned_contacts` (log-odds scale).

### 3.5 Use Cases

- Medical: probability of a patient's response to treatment
- Finance: probability an applicant defaults on a loan
- Marketing: probability of customer churn
- Engineering: probability of mechanical part failure

### 3.6 Classification Threshold

The fitted probability `P(y=1|x)` must be converted into a class decision using a threshold — commonly 0.5 (`P ≥ 0.5 → class 1`). The threshold can be adjusted depending on the relative cost of false positives vs. false negatives (e.g. lowered in medical screening to avoid missing positive cases).

### 3.7 Evaluating a Classifier: Confusion-Matrix Terms

- **True Positive (TP)** — predicted C, actually C
- **True Negative (TN)** — predicted ¬C, actually ¬C
- **False Positive (FP)** — predicted C, actually ¬C
- **False Negative (FN)** — predicted ¬C, actually C

```
Accuracy (ACC) = (TP + TN) / (TP + TN + FP + FN)
False Positive Rate (FPR) = FP / (FP + TN)
True Positive Rate (TPR) = TP / (TP + FN)
```

### 3.8 ROC Curve and AUC

**Purpose:** evaluate a classifier's discriminative ability independent of any single threshold choice, since TPR and FPR both change as the threshold changes (lowering the threshold increases TPR but also increases FPR).

**Construction:** sweep the threshold from 0 to 1; at each threshold compute (FPR, TPR); plot FPR (x-axis) vs TPR (y-axis).

**Reading the curve:**
- Curve bulging toward the top-left corner (high TPR, low FPR) → better model.
- The 45° diagonal represents performance equivalent to random guessing.

**AUC (Area Under the Curve):** summarizes the whole curve as a single number.
- AUC = 1 → perfect classifier
- AUC = 0.5 → no better than random guessing
- Example from the course material: AUC = 0.8877 (good discriminative ability)

**Practical use:** beyond overall model comparison, the ROC curve helps choose an operating threshold that matches the real-world cost asymmetry of a problem (e.g. a lower threshold to avoid missing disease cases; a higher threshold to avoid flagging important emails as spam).

## 4. Choosing Between Linear and Logistic Regression

- **Linear regression** — input variables continuous or discrete; outcome variable continuous.
- **Logistic regression** — better choice when the outcome variable is categorical.
- Both assume a linear additive function of the input variables.

## 5. Reasons to Choose and Cautions

### 5.1 Correlation Does Not Imply Causation

A statistically significant, positive coefficient only shows a *statistical association* between `x` and `y` — it does not prove that `x` directly *causes* `y`. A confounding variable can drive both simultaneously and create a spurious correlation (classic example: ice-cream sales and drowning incidents both rise in summer — the confounder is temperature/season, not a causal link between the two). Establishing true causation typically requires randomized controlled experiments or dedicated causal-inference methods, not standard regression alone.

### 5.2 Generalization Issue

A fitted model reflects the range of the data it was trained on. Applying it to data that falls **outside** that range (extrapolation) — e.g. predicting income for an age far beyond the training data's range, or applying a model trained in one context (city, market) to a very different one — can produce unreliable predictions, since there is no guarantee the learned relationship continues to hold outside the observed range.

### 5.3 Multicollinearity Issue

Occurs when two or more input variables are strongly correlated with each other (e.g. house floor area and number of bedrooms). Consequences:
- Coefficient standard errors become inflated, making estimates unstable (small data changes can shift coefficients substantially, even flipping their sign).
- Inflated standard errors reduce t-values and increase p-values, potentially making an important variable appear statistically insignificant.
- Overall prediction accuracy is often still fine, but interpreting individual coefficients becomes unreliable.

**Remedies: Ridge Regression and Lasso Regression** — both add a regularization penalty to the OLS objective:

```
Ridge:  min Σ(yi − ŷi)² + λ Σ βj²
Lasso:  min Σ(yi − ŷi)² + λ Σ |βj|
```

Both shrink coefficient magnitudes to stabilize estimates under multicollinearity. Ridge shrinks coefficients toward (but rarely to) zero, keeping all variables in the model. Lasso can shrink coefficients to *exactly* zero, effectively performing automatic feature selection. `λ` is a tuning hyperparameter controlling the strength of the penalty.

## 6. Summary

- Linear regression and logistic regression both model observed data to predict future outcomes — for continuous and categorical outcomes respectively.
- Care must be taken in performing and interpreting a regression analysis:
  - Determine the best input variables and their relationship to the outcome.
  - Understand and validate the underlying assumptions (linearity, residual behaviour, normality).
  - Transform variables when necessary.
  - Remember that association is not causation, be cautious about generalizing beyond the training data, and address multicollinearity when present.

---
*Source: "Data Science and Big Data Analytics: Discovering, Analyzing, Visualizing and Presenting Data" (course lecture material), plus discussion notes.*
