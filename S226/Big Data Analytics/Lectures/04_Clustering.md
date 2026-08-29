# Advanced Analytical Theory and Methods — Clustering
## Comprehensive Lecture Summary

**Course:** CSCI446/946 Big Data Analytics | **Topic:** Clustering (Unsupervised Learning)

---

## 1. Overview: What is Clustering?

Clustering is an **unsupervised learning** task: there are **no labels**. The algorithm's job is to discover natural groupings (clusters) in the data purely from the similarity/distance between observations.

This contrasts sharply with **Classification**, where labelled data exists and the goal is prediction. Because there is no ground truth in clustering, evaluation must rely on **internal structure quality** (e.g. compactness) rather than comparing predictions to known answers.

| Concept | Clustering (Unsupervised) | Classification (Supervised) |
|---|---|---|
| Labels available? | No | Yes |
| Goal | Discover hidden groups | Predict a known label |
| Evaluation | Internal structure (WSS, visual/domain checks) | Confusion matrix, Accuracy, Precision, Recall |

**Why feature scaling matters:** All clustering methods below rely on **distance**. If one attribute has a much larger numeric range than another (e.g. income in dollars vs. age in years), it will dominate the distance calculation and overshadow other attributes — even if both are equally important conceptually. **Z-score standardization** is therefore a required preprocessing step:

$$z = \frac{x - \mu}{\sigma}$$

---

## 2. K-Means Clustering

### 2.1 Core idea
Partition the dataset into **k** groups such that points within a group are as similar as possible (minimizing within-cluster distance), where **k must be specified in advance**.

### 2.2 The Four-Step Algorithm
1. **Choose k** — the number of clusters.
2. **Initialize** k centroids (often randomly).
3. **Assignment step** — assign each data point to its nearest centroid (by Euclidean distance).
4. **Update step** — recompute each centroid as the **mean** of all points assigned to it.
5. Repeat steps 3–4 until centroids stop changing (**convergence**).

### 2.3 Choosing k — The Elbow Method
Plot **Within-cluster Sum of Squares (WSS)** against different values of k. WSS always decreases as k increases, but the rate of decrease slows down after a certain point — this "elbow" indicates a good trade-off between cluster compactness and simplicity. Beyond the elbow, adding more clusters gives diminishing returns.

### 2.4 Important practical notes
- **Sensitive to initialization**: different random starting centroids can lead to different final clusters (the algorithm only guarantees convergence to a **local optimum**, not a global one). In practice, the algorithm is run multiple times with different random starts (e.g. R's `nstart=25`), keeping the best result.
- **Assumes roughly spherical, similarly-sized clusters** — struggles with irregular shapes or very different cluster densities/sizes.
- Fast and scalable — well suited for large datasets.

### 2.5 Strengths and weaknesses

✅ Simple, fast, scalable to large data, easy to interpret via centroids.

❌ Must specify k in advance; sensitive to outliers (they pull centroids); assumes spherical clusters; results can vary with initialization.

---

## 3. Hierarchical Clustering

### 3.1 Core idea
Unlike K-means, Hierarchical Clustering does **not require k in advance**. Instead, it builds a complete tree of nested clusters (a **dendrogram**), and the user decides afterward, by cutting the tree at a chosen height, how many clusters to use.

### 3.2 Agglomerative approach (bottom-up)
1. Start with every point as its own cluster.
2. Repeatedly **merge the two closest clusters** into one.
3. Continue until only a single cluster remains.
4. The result is a dendrogram showing the entire merge history.

This is a **greedy, one-directional process**: once two clusters are merged, that decision can **never be undone**, unlike K-means, which can reassign points across iterations.

### 3.3 Linkage methods — how to measure distance *between clusters*

Once clusters contain more than one point, "distance between clusters" must be redefined. Four common linkage methods:

| Method | Distance definition | Also known as | Characteristic |
|---|---|---|---|
| **Single** | Minimum distance between any pair of points across the two clusters | Nearest Point Algorithm | Prone to "chaining" — can create long, straggly clusters |
| **Complete** | Maximum distance between any pair of points across the two clusters | Farthest Point Algorithm | Produces tighter, more compact clusters |
| **Average** | Mean distance across all pairs of points | UPGMA | Balanced compromise between single and complete |
| **Centroid** | Distance between the two clusters' centroids | UPGMC | Easy to interpret via a representative "center" |

### 3.4 Strengths and weaknesses

✅ No need to pre-specify k; produces a rich, multi-level view of cluster structure; deterministic (no randomness, so results are reproducible).

❌ Computationally expensive (commonly $O(n^2 \log n)$ or worse) — impractical for very large datasets; sensitive to outliers, especially with single linkage; merge decisions are irreversible.

---

## 4. DBSCAN (Density-Based Spatial Clustering)

### 4.1 Core idea
Instead of measuring distance to a centroid, DBSCAN groups points based on **density** — regions of high point density form clusters, while points in low-density regions are treated as **noise/outliers**.

### 4.2 Key parameters
- **Eps (ε)** — the radius defining a point's neighborhood.
- **MinPts** — the minimum number of points required within that radius for a point to be considered a "core point."

Points are classified as:
- **Core point** — has at least MinPts neighbors within Eps.
- **Border point** — within Eps of a core point but doesn't itself meet MinPts.
- **Noise point** — neither a core point nor within reach of one.

### 4.3 Strengths and weaknesses

✅ Discovers **arbitrarily shaped clusters** (not just spherical); naturally identifies outliers/noise; does not require k to be specified.

❌ Struggles when clusters have very different densities (fixed global Eps/MinPts can't fit all regions well); choosing good Eps/MinPts values can be non-trivial.

---

## 5. Self-Organizing Map (SOM)

### 5.1 Core idea
A SOM is a type of **neural network** that performs clustering *and* dimensionality reduction simultaneously, mapping high-dimensional data onto a 2D grid of neurons while **preserving topology** — similar data points end up mapped to nearby neurons on the grid.

### 5.2 Training algorithm
For each input vector:
1. **Competitive step** — find the **Best Matching Unit (BMU)**: the neuron whose weight vector is closest to the input.
2. **Cooperative step** — update the BMU's weights *and* those of its **neighboring neurons on the grid**, with the amount of update decreasing with distance from the BMU (typically via a Gaussian neighborhood function) and shrinking over training time.

$$\Delta w_j = \eta(t) \cdot h_{j,BMU}(t) \cdot (x - w_j)$$

### 5.3 What makes SOM different
Unlike K-means, SOM's representative units (neurons) are **spatially connected** to each other via the grid — nearby neurons tend to represent similar data. This gives SOM a unique advantage: it produces a **visualizable 2D map** where clusters and their relationships to one another can be seen directly, which flat clustering methods (K-means, DBSCAN) cannot provide.

### 5.4 Strengths and weaknesses

✅ Excellent for visualizing high-dimensional data; preserves neighborhood relationships between clusters; useful for exploratory analysis and presentations.

❌ More complex to tune (learning rate, grid size, neighborhood radius schedule); slower than K-means; less commonly used purely for "hard" partitioning tasks.

---

## 6. Comparing the Four Methods

| Criterion | K-Means | Hierarchical | DBSCAN | SOM |
|---|---|---|---|---|
| Requires k upfront? | **Yes** | No | No | No (grid size instead) |
| Optimization style | Iterative (can reassign) | Greedy agglomerative (irreversible) | Density traversal | Iterative, competitive + cooperative |
| Cluster shape assumption | Spherical | Depends on linkage | **Arbitrary shape** | Grid-constrained regions |
| Handles noise/outliers? | Poorly (pulls centroids) | Poorly (esp. single linkage) | **Well** (explicit noise label) | Moderate |
| Scalability | High | Low ($O(n^2)$+) | Moderate | Moderate |
| Output | Flat partition | Full dendrogram (nested) | Flat partition + noise | 2D visual map |
| Best for | Large data, known k | Exploring nested structure | Irregular shapes, noisy data | Visualization, exploratory analysis |

---

## 7. Model Evaluation in Clustering — Why It's Fundamentally Different

Because clustering has no ground-truth labels, it **cannot** be evaluated with a confusion matrix, accuracy, precision, or recall the way classification can. Instead, evaluation relies on:

- **Within-cluster Sum of Squares (WSS) / Elbow method** — measures cluster compactness, used to select k for K-means.
- **Visual inspection / domain expert review** — checking whether resulting clusters make sense in a business or scientific context (e.g., do the customer segments correspond to meaningfully different profiles?).

This reflects the deeper philosophical distinction between the two paradigms: Classification is **predictive** (there is a correct answer to check against), while Clustering is **exploratory** (the goal is to reveal structure, not to match a known answer).

---

## 8. Synthesis — Connecting the Dots

All four clustering methods answer the same underlying question — *"which points belong together?"* — but differ in:

- **What "belonging together" means**: proximity to a centroid (K-means), nested proximity (Hierarchical), local density (DBSCAN), or topological similarity on a learned map (SOM).
- **Whether k must be chosen in advance**: K-means requires it upfront; Hierarchical, DBSCAN, and SOM let structure emerge and can be interpreted afterward.
- **Robustness to irregular shapes and noise**: DBSCAN excels here; K-means and (to a lesser extent) Hierarchical assume more regular, well-separated clusters.
- **Purpose beyond partitioning**: SOM uniquely adds a visualization/dimensionality-reduction layer that the other three do not provide.

**Core takeaway:** Clustering method choice should be driven by (1) whether the number of groups is known in advance, (2) the expected shape/density of natural groups in the data, (3) dataset size, and (4) whether visualization of relationships between groups is a goal in itself.
