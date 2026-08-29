# Advanced Analytical Theory and Methods — Classification
## Comprehensive Lecture Summary

**Course:** CSCI446/946 Big Data Analytics | **Topic:** Classification (Supervised Learning)

---

## 1. Overview: What is Classification?

Classification is a **supervised learning** task: the model learns from a **labelled training set** (data where the correct answer/class is already known) and then predicts the class label for new, unseen observations.

This is fundamentally different from **Clustering** (unsupervised learning), where no labels exist and the algorithm must discover structure on its own.

**Running example used throughout the lecture:** A bank has 2,000 past customers, and for each one it is known whether they **subscribed** to a term deposit or not. Input attributes include `job`, `marital`, `education`, `housing`, `loan`, `contact`, `poutcome`, etc. The task is to predict whether a *new* customer will subscribe.

| Concept | Supervised (Classification) | Unsupervised (Clustering) |
|---|---|---|
| Labels available? | Yes | No |
| Goal | Predict a known label for new data | Discover hidden groups |
| Evaluation | Compare prediction vs. ground truth | No ground truth — evaluate structure quality |

---

## 2. K-Nearest Neighbor (KNN)

### Core idea
"Similar things live near each other." To classify a new point, look at its **k nearest neighbors** in the training set and let them **vote**.

### Algorithm
1. Choose a value of **k**.
2. Compute the distance from the new point to every point in the training set (typically **Euclidean distance**).
3. Select the **k closest points**.
4. **Majority vote**: assign the class that is most common among those k neighbors.
5. Optionally use **distance-weighted voting**: weight $w = 1/d^2$, so closer neighbors have more influence than farther ones.

### Choosing k — the bias-variance trade-off
- **k too small** (e.g. k=1): very sensitive to noise — a single outlier can flip the prediction.
- **k too large**: the neighborhood starts including points from other classes, diluting local accuracy.
- **k larger** = more computation (more distances to calculate and sort).

### Key properties
- KNN is a **"lazy learner"** — it does not build an explicit model during training; all the work happens at prediction time.
- Requires **feature scaling (Z-score standardization)** before use, since it depends entirely on distance.
- Works best with numeric, low-to-moderate dimensional data.

---

## 3. Decision Tree

### 3.1 Intuition
A decision tree mimics human decision-making: a sequence of if-else questions that lead to a final classification.

**Structure:**
- **Root node** — the first, most informative question
- **Internal node** — a test on one attribute (e.g. `Income < 45,000?`)
- **Branch** — the outcome of a test
- **Leaf node** — the final class label

Real-world applications: animal classification, medical symptom checklists, loan approval, marketing response prediction.

### 3.2 The core problem: which attribute to split on first?

The tree always splits on the attribute that yields the highest **Information Gain**, which is based on **Entropy**.

**Entropy** measures the "impurity" / unpredictability of a dataset:

$$H = -\sum_{x \in X} P(x)\log_2 P(x)$$

- A **pure** set (all one class) → entropy = 0 (no surprise).
- A perfectly **balanced** set (50/50) → entropy = 1 (maximum uncertainty, like a fair coin flip).

*Bank example:* $P(subscribed{=}yes) \approx 0.11$, $P(subscribed{=}no) \approx 0.89$. Because the split is heavily skewed toward "no", the baseline entropy $H_{subscribed}$ is relatively low — the outcome is fairly predictable even without extra information.

**Conditional Entropy** $H(Y|X)$: the remaining entropy of Y *after* knowing attribute X. Computed as the weighted average of the entropy within each subgroup defined by X:

$$H_{Y|X} = \sum_{x} P(x) \cdot H(Y|X=x)$$

*Example:* For attribute `contact` (cellular / telephone / unknown): $H_{subscribed|contact} = 0.4661$.

**Information Gain** = reduction in entropy achieved by knowing the attribute:

$$InfoGain_A = H_Y - H_{Y|A}$$

*Example:* $InfoGain_{contact} = 0.4862 - 0.4661 = 0.0201$

**Bank dataset information gain ranking (from the lecture):**

| Attribute | Information Gain |
|---|---|
| poutcome | 0.0289 |
| contact | 0.0201 |
| housing | 0.0133 |
| job | 0.0101 |
| education | 0.0034 |

→ `poutcome` (outcome of the previous marketing campaign) has the highest gain and is selected as the **root split** — knowing whether a customer responded positively before reduces uncertainty about this campaign the most.

### 3.3 General algorithm (ID3-style)
Recursively, at each node:
1. Compute information gain for every remaining attribute.
2. Choose the attribute with the highest gain and split on it.
3. Repeat for each resulting branch.
4. Stop when a node is sufficiently pure, gain becomes negligible, or another stopping criterion (e.g. max depth) is reached.

### 3.4 Overfitting problem
Decision trees use a **greedy algorithm** — at each step they pick the locally best option without considering the global optimum. This easily leads to **overfitting**: overly deep trees with leaves containing very few samples, which memorize noise rather than general patterns.

**Mitigation:** **Random Forest** — an ensemble of many decision trees, each trained on a random subset of data/attributes, with predictions combined by voting. This reduces variance and the risk of being stuck with one bad greedy choice.

### 3.5 Strengths and weaknesses

✅ Computationally cheap, easy to apply, produces **human-readable decision rules** (the biggest advantage over Naïve Bayes or Neural Networks), handles both numerical and categorical data, captures non-linear relationships naturally.

❌ Performs poorly with many **irrelevant variables** — feature selection is often needed beforehand. Prone to overfitting due to its greedy nature.

---

## 4. Naïve Bayes Classifier

### 4.1 Foundation: Bayes' Theorem

$$P(C|A) = \frac{P(A|C) \cdot P(C)}{P(A)} = \frac{\text{likelihood} \times \text{prior}}{\text{evidence}}$$

- $C$ — the class label to predict
- $A = \{a_1, ..., a_n\}$ — the observed attributes (evidence)
- **Posterior** $P(C|A)$ — the updated probability of class C *after* observing the evidence

### 4.2 Worked examples from the lecture

**Example 1 — John's flight upgrade:**
- $P(E)=0.40$ (checks in early), $P(U|E)=0.75$, $P(U|\bar E)=0.35$
- Given he did **not** get upgraded, find $P(\bar E|\bar U)$ (probability he did not check in early).
- $P(\bar U) = (0.25)(0.40) + (0.65)(0.60) = 0.49$
- $P(\bar E|\bar U) = \frac{0.65 \times 0.60}{0.49} \approx 0.796$ (≈79.6%)

**Example 2 — Mary's medical test:**
- $P(C)=0.01$ (disease prevalence), $P(A|C)=0.95$ (sensitivity), $P(A|\bar C)=0.06$ (false positive rate)
- $P(A) = (0.95)(0.01) + (0.06)(0.99) = 0.0689$
- $P(C|A) = \frac{0.0095}{0.0689} \approx 0.138$ (≈13.8%)

**Key insight (base rate fallacy):** even with a highly accurate test (95% sensitivity), if the underlying condition is rare, the posterior probability of truly having it remains low — because the sheer number of false positives from the large healthy population outweighs the true positives from the small affected population. **The prior matters as much as the likelihood.**

### 4.3 The "Naïve" assumption

Naïve Bayes assumes **conditional independence**: attributes are independent of one another *given* the class. This simplifies the joint probability into a product of individual probabilities:

$$P(a_1,...,a_n|c) = \prod_{j} P(a_j|c)$$

*Bank example:* $P(yes|A) \approx 0.00023 > P(no|A) \approx 0.00017$ → predict **yes**. (These are unnormalized proportional values, sufficient for comparing classes.)

### 4.4 The rare-event problem & Laplace Smoothing

If an attribute value **never appears** in the training data for a given class, $P(a_j|c_i) = 0$, which collapses the entire product to zero — even if all other evidence strongly favors that class. This is a serious flaw.

**Solution — Laplace smoothing:** add 1 to every count to avoid zero probabilities:

$$P'(single|yes) = \frac{(20+1)}{(20+1)+(70+1)+(10+1)}$$

### 4.5 Strengths and weaknesses

✅ Simple, efficient with **high-dimensional data** (e.g. text classification, spam detection), robust to sparse data thanks to smoothing.

❌ Sensitive to **correlated attributes** — because independence is assumed, correlated evidence gets "double-counted," biasing the result. Probability estimates themselves are often not well-calibrated (though the predicted class is usually still reasonably accurate).

---

## 5. Model Diagnostics — Evaluating a Classifier

### Confusion Matrix

| | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actual Positive** | TP | FN |
| **Actual Negative** | FP | TN |

*Bank example:* out of 100 customers (11 actually subscribed, 89 did not), the model correctly predicted 3 TP + 87 TN.

### Key metrics

- **Accuracy** = $(TP+TN)/(TP+TN+FP+FN)$ — overall correctness. ⚠️ Misleading with imbalanced data: a model that always predicts "no" would still score 89% accuracy while being useless.
- **Precision** = $TP/(TP+FP)$ — of all predicted positives, how many were correct.
- **Recall (TPR)** = $TP/(TP+FN)$ — of all actual positives, how many were captured.
- **FPR** = $FP/(FP+TN)$, **FNR** = $FN/(TP+FN)$

### Choosing a model — decision guide from the lecture

| Situation | Recommended model(s) |
|---|---|
| Need probability output, not just a label | Logistic regression, Decision tree |
| Need to understand each variable's influence | Logistic regression, Decision tree |
| High-dimensional data | Naïve Bayes |
| Input variables are correlated | Logistic regression, Decision tree |
| Categorical variables with many levels | Decision tree, Naïve Bayes |
| Non-linear / discontinuous relationships | Decision tree |

---

## 6. Additional Classification Models (overview)

- **Random Forest** — ensemble of decision trees; addresses overfitting of a single tree.
- **Support Vector Machine (SVM)** — max-margin linear classifier; kernel trick handles non-linearly separable data.
- **Neural Networks** — Multi-layer Perceptron and deeper architectures for complex, non-linear patterns.

---

## 7. Synthesis — Connecting the Dots

| | KNN | Decision Tree | Naïve Bayes |
|---|---|---|---|
| Foundation | Distance | Entropy / Information Gain | Bayes' Theorem |
| "Learns" a model? | No (lazy) | Yes (tree structure) | Yes (probability tables) |
| Interpretable? | Low | **High** | Low |
| Needs feature scaling? | **Yes** | No | No |
| Handles correlated attributes? | N/A (uses raw distance) | Good | **Weak point** |
| Best suited for | Low-dim, non-linear boundaries | Rule-based, explainable decisions | High-dimensional / text data |
| Optimization style | None (lazy) | Greedy recursive | Closed-form (direct computation) |
| Key risk | Sensitive to irrelevant features & noisy k | Overfitting (mitigated by Random Forest) | Independence assumption violated |

**Core takeaway:** All classifiers ultimately answer the same question — *"given what I observe, which class is most likely?"* — but they differ in how they measure "likely" (geometric closeness vs. information-theoretic gain vs. probabilistic evidence) and in the trade-off they make between accuracy, interpretability, and computational simplicity.
