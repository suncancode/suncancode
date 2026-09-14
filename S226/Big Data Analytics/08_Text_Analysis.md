# Text Analysis 

---

## 1. Why Text Analysis Is Hard

To a computer, text is nothing but a sequence of bytes: `"Hello"` → `[72, 101, 108, 108, 111]` → binary. The computer has:

- no understanding of **syntax** (sentence structure/grammar),
- no understanding of **semantics** (meaning),
- no understanding of **pragmatics** (meaning-in-context — "break it down" can mean demolishing a building or explaining a business idea, depending on context).

Three additional sources of ambiguity make this worse: **homonyms** (same spelling, different meaning — "bark" of a dog vs. of a tree; "Amazon" the river/company/rainforest), **acronyms** (CGI = Common Gateway Interface or Computer Graphics Interface?), and the fact that most text is **unstructured** — no fixed schema, no consistency, no explicit semantics, unlike structured data in a database.

Consequence: in raw form, there is **no natural similarity metric** between two pieces of text, so clustering or classification simply cannot be applied directly. This is the single problem every technique in this lecture exists to solve: **transform unstructured text into a structured, numeric representation** on which the usual machine-learning machinery (from earlier weeks) can then operate.

---

## 2. The General Text Analysis Pipeline

```
1. Collect Raw Text → 2. Represent Text → 3. TFIDF → 4. Topic Modeling → 5. Sentiment Analysis → 6. Gain Insights
```

Motivating example from the slides: a company wants to monitor social media to see whether people are mentioning its products, and whether the sentiment is positive or negative. Every step of the pipeline above exists to answer that one business question systematically.

### Step 1 — Collecting Raw Text
Gathered via public APIs, web scrapers/crawlers. Expect unstructured or semi-structured data, and be mindful of data-ownership rights when scraping.

---

## 3. Representing Text

### 3.1 Tokenization
Splitting raw text into individual word tokens. This sounds trivial but is not:

- "day" vs. "day." — does the period belong to the token?
- "we'll", "state-of-the-art" — do apostrophes/hyphens split the token or not?
- "résumé" vs. "resume" (diacritics), "Back of Bourke" (a multi-word proper noun)
- **There is no one-size-fits-all tokenization scheme.**

(Contemporary note: GPT models use byte-level Byte Pair Encoding — BPE — with a fixed ~50k-token vocabulary, which handles arbitrary input, including code, emoji, and rare characters, by breaking text into subword units. This is one modern answer to exactly this "no universal scheme" problem.)

### 3.2 Text Normalization

1. **Case folding** — lowercasing everything. Done naively, this destroys distinctions like "US" (the country) vs. "us" (the pronoun), or "WHO" (World Health Organization) vs. "who". A lookup table of words that should *not* be folded is often needed.
2. **Stop-word removal** — dropping words unlikely to carry semantic weight ("the, a, of, and, to, …").
3. **Stemming vs. Lemmatization** — a frequently-confused pair:

| | Stemming | Lemmatization |
|---|---|---|
| Method | Chops word endings using crude rules | Uses a dictionary + grammar rules to find the true base form |
| Speed | Fast | Slower |
| Accuracy | Rough — can produce non-words | Accurate — always produces a real word |
| Example | walking, walks, walked → **walk** (fine) | geese, goose, gander, ganders → **goose** (requires knowing "geese" is the irregular plural of "goose" — a rule-based stemmer cannot infer this) |
| Common tool | Porter Stemmer | WordNet Lemmatizer |

Modern note: embeddings/LLMs handle word-form variation internally at the representation level, so many modern pipelines skip stemming/lemmatization as a separate step entirely.

### 3.3 Bag-of-Words (BoW)

Represents a document as a set/vector of the terms it contains, discarding order, context, and inference entirely — "a dog bites a man" and "a man bites a dog" produce the **identical** BoW vector. Naïve, but still a reasonable teaching tool and baseline, even though embeddings and LLMs have largely superseded it for state-of-the-art work.

Slide example — three documents: *"the quick brown fox."*, *"the best of times."*, *"my quick study of lexicography helped."* Shared dictionary: `{the, brown, fox, quick, times, of, best, my, study, lexicography, helped}`. Document 1's vector is `(1,1,1,1,0,0,0,0,0,0,0)` — a 1 at each position corresponding to a word it contains.

---

## 4. From Information Content to TF-IDF

**Information Content (IC)** of a term: `IC(x) = −log P(x)`. Rarer terms (low P) get higher IC — i.e., they carry more information.

Problem with IC: it depends on a **fixed corpus/metadata that does not change over time**, which fails for dynamic data (social media, breaking news) for two reasons — (1) the reference corpus itself is static, and (2) it limits recognizable knowledge to whatever the corpus already covers; brand-new topics/concepts go unrecognized.

→ We need a measure that **adapts to whatever document set is currently being analyzed**, and updates automatically when that set changes. That measure is **TF-IDF**.

### Term Frequency (TF)
Number of times term *t* appears in document *d* (with variants: raw count, log-normalized `1 + log(TF)`, or divided by document length to avoid favoring long documents).

**Zipf's Law**: the *i*-th most common word occurs with frequency roughly proportional to 1/*i* relative to the most frequent word — natural language is highly imbalanced: a handful of words dominate, most words are rare.

**The problem with TF alone**: a term's importance is judged only within one document. But what if that term appears frequently in *every* document? Then it isn't actually distinctive. We need a broader, corpus-level view.

### Document Frequency (DF) and Inverse Document Frequency (IDF)

`DF(t)` = number of documents in the corpus containing term *t*.
`IDF(t) = log(N / DF(t))`, where N is the total number of documents.

- A **rare** term (low DF) gets a **high** IDF.
- A term that is **common across the whole corpus** (DF close to N) gets a **low** IDF, approaching 0 as DF → N (a term appearing in nearly every document is nearly useless for distinguishing documents).

### TF-IDF

```
TFIDF(t, d) = TF(t, d) × IDF(t)
```

A term scores high when it is **frequent within this specific document** (high TF) **but rare across the corpus as a whole** (high IDF) — precisely the signature of a term that genuinely characterizes this document. This is what fixes TF's blind spot and beats static IC on adaptability, since it recomputes automatically as the underlying document collection changes.

---

## 5. Topic Modeling — How Words Actually Get Grouped Into Topics

This is the part of the lecture that deserves the most careful unpacking, because "grouping words by topic" is *not* simple frequency counting or thresholding. It is the result of an **iterative, self-reinforcing statistical process** driven by co-occurrence patterns across documents, constrained by a number of topics (K) that you choose in advance.

### 5.1 Why go beyond TF-IDF at all?

A TF-IDF vector represents a document as a score for *every individual word* in the vocabulary — extremely high-dimensional, and it captures **no relationship between documents or between words**: two documents about the exact same theme, using different vocabulary, look completely unrelated under TF-IDF. Topic modeling fixes this by representing a document not as thousands of word-scores, but as a **short mixture of K themes** — a genuine dimensionality reduction that preserves cross-document structure.

A **topic** is defined formally as a **probability distribution over the entire fixed vocabulary**. Different topics are different distributions over the *same* vocabulary — so a word like "market" might have high probability under a "finance" topic and low (but non-zero) probability under a "sports" topic; it is never excluded from any topic, just weighted differently.

### 5.2 The generative story behind LDA (Latent Dirichlet Allocation)

LDA assumes each document was "cooked" by an imaginary generative recipe:

1. Choose the document length *N*.
2. Choose a distribution over the *K* topics for this document (e.g., "60% Topic A, 40% Topic B").
3. For each of the *N* word slots in the document:
   a. Draw a topic according to the document's topic distribution from step 2.
   b. Draw an actual word according to *that topic's* word distribution.

In reality, we only ever observe the finished documents — the topic mixtures, the per-word topic assignments, and even the topics themselves (as word distributions) are all **hidden (latent)** variables. LDA's job is to run this story **backward**: given only the observed words, infer the most plausible hidden topics, per-document topic proportions, and per-word topic assignments that could have generated this data.

Three fixed assumptions: (1) the vocabulary is fixed, (2) the number of topics K is fixed and chosen by you in advance (exactly like choosing K in K-means — a striking parallel to Clustering), (3) each topic is a distribution over the vocabulary and each document is a distribution over topics.

### 5.3 The actual mechanism: Collapsed Gibbs Sampling, step by step

This is the algorithm that performs the inference, and it is the real answer to "how does frequency + K produce topic groupings":

1. Choose the number of topics *K*.
2. **Randomly** assign every word token in every document to one of the *K* topics. (At this point the assignment is pure noise — no structure yet.)
3. For each word token *w* in each document *d*, repeatedly:
   - Temporarily remove *w*'s current topic assignment from all counts.
   - Count how many **other** words in document *d* are currently assigned to each topic → this is the *document–topic count*, `n_{d,t}`.
   - Count how many times word *w* specifically is currently assigned to each topic **across the entire corpus** → this is the *topic–word count*, `n_{t,w}`.
   - Combine these two counts (with Dirichlet smoothing constants α, β) into a probability that *w* belongs to each topic *t*:
     ```
     P(t | w, d) ∝ (n_{d,t} + α) × (n_{t,w} + β) / (n_t + V·β)
     ```
     where `n_t` is the total number of word tokens currently assigned to topic *t* across the corpus, and *V* is the vocabulary size.
   - **Resample** a new topic for *w* according to this probability distribution.
4. Repeat step 3 for many iterations (sweeping through every word in every document each time) until the assignments stabilize (converge).
5. Use the final, stabilized assignments to read off: the topic-proportion vector for every document, and the word-distribution for every topic.

**Why this converges to meaningful groups — the co-occurrence feedback loop.** The formula above has an intuitive reading: word *w* is pulled toward topic *t* when (a) topic *t* is **already prominent in this same document** (high `n_{d,t}` — "what else is this document about?"), **and** (b) topic *t* **already carries a lot of weight for this exact word elsewhere in the corpus** (high `n_{t,w}` — "does this topic like this word, based on the rest of the corpus?"). Neither signal alone is enough; it's their product that matters.

**Worked toy example.** Vocabulary `{ball, goal, score, stock, market, invest}`, K = 2, three documents:

```
D1: ball goal score ball          (a "sports" document)
D2: stock market invest stock     (a "finance" document)
D3: ball score stock market       (a mixed document)
```

Suppose the random initialization happens to give: D1 → `ball(T1) goal(T2) score(T1) ball(T2)`; D2 → `stock(T1) market(T2) invest(T1) stock(T2)`; D3 → `ball(T2) score(T1) stock(T1) market(T2)`. Right now T1 and T2 are meaningless — each contains a random mix of sports and finance words.

Now resample the first "ball" token in D1 (currently T1). Removing it first, the relevant counts are:

- Document D1 (excluding this token): `n_{D1,T1}=1` (score), `n_{D1,T2}=2` (goal, ball)
- Topic-word counts (excluding this token): `n_{T1,ball}=0`, `n_{T2,ball}=2`; corpus-wide topic totals (with V=6, using α=β=0.1 for illustration): `n_{T1}≈5`, `n_{T2}≈6`

```
P(T1) ∝ (1+0.1) × (0+0.1)/(5+0.6)  ≈ 0.0196
P(T2) ∝ (2+0.1) × (2+0.1)/(6+0.6)  ≈ 0.668
```

Normalized, this token has roughly a **97% chance** of being resampled into T2. Why? Because D1 already leans toward T2 based on its *other* words (goal, ball), and T2 already "likes" the word *ball* based on its occurrences elsewhere in the corpus. Both signals point the same direction, so the token gets pulled along.

Run this resampling for every word, over many iterations, and the effect compounds: whenever a sports word appears, the *other* sports words co-occurring with it in the same documents reinforce the same topic assignment; whenever a finance word appears, the other finance words co-occurring with it reinforce a different topic. Because "ball", "goal", "score" keep showing up together (in D1 and D3), and "stock", "market", "invest" keep showing up together (in D2 and D3), the two groups pull apart into two increasingly coherent topics — purely as an emergent consequence of **co-occurrence across documents**, not because anyone told the algorithm what "sports" or "finance" means, and not because of raw frequency alone.

This is precisely why **frequency by itself is not the grouping signal** — a word that is frequent overall but spread roughly evenly across all documents (a classic stop word, if not already removed in preprocessing) will end up with roughly uniform counts across all K topics and will not get pulled strongly toward any one of them. What actually drives the grouping is **which words tend to co-occur inside the same documents, repeated consistently enough across many documents** that the counts accumulate a clear signal. This is also exactly why stop-word removal (Section 3.2) matters so much before running LDA — leaving stop words in adds noise that dilutes every topic's word distribution.

### 5.4 The role of K, and of α/β

- **K too small**: distinct, unrelated co-occurrence groups get forced to merge into one topic, blending vocabularies that don't actually belong together (e.g., forcing sports and finance into a single topic if K=1).
- **K too large**: a single coherent theme gets artificially split into multiple overlapping, less-interpretable micro-topics, or the model manufactures near-duplicate topics to "use up" the extra capacity. There is no single mathematically "correct" K — it is chosen using judgment, domain knowledge, or model-selection heuristics (e.g., topic coherence scores, perplexity on held-out data), the same kind of trade-off as choosing K in K-means.
- **α** controls how many topics a document is expected to mix — higher α → each document's topic distribution is assumed spread across more topics (less peaked).
- **β** controls how many words each topic is expected to concentrate on — higher β → each topic's word distribution is assumed spread across more words (less sharply defined).

---

## 6. It's "Just Descriptive" — So What Can You Actually Do With Topics?

This is the natural follow-up question, and it parallels exactly the concern you raised earlier about Clustering: if there's no ground truth and nothing is being "predicted," what is the output actually *for*? The honest answer is that descriptive/unsupervised methods are rarely the final step of an analysis — they are a **compression, exploration, and feature-engineering stage** that feeds something else useful. Concretely:

1. **Dimensionality reduction for downstream tasks.** A document's TF-IDF vector has one dimension per vocabulary word (often tens of thousands); its topic-proportion vector has only *K* dimensions (e.g., 10–50). This compressed representation can be clustered, visualized (e.g., projected to 2D to see how documents relate to each other), or compared for similarity far more efficiently and meaningfully than raw word vectors — two documents using entirely different vocabulary but the same underlying theme will now look similar, which they never would under TF-IDF.

2. **Feeding a supervised model downstream — bridging descriptive into predictive.** Nothing stops you from taking each document's *K*-dimensional topic-proportion vector and using it as the **input features** to a classifier or regression model afterward (e.g., predicting whether a support ticket will escalate, using its topic mixture as a compact feature set instead of raw TF-IDF). LDA itself makes no validated prediction — but its output becomes the *input* to a later stage that can be validated in the usual supervised way. This is the same relationship PCA has to a downstream classifier: an unsupervised compression step in front of a supervised model.

3. **Corpus-scale sense-making that no human could do by reading.** With thousands or millions of documents (customer reviews, support tickets, research papers, social posts), topics give a human-readable summary of what themes actually exist — e.g., discovering that "battery life," "shipping delays," and "customer service" are the three dominant recurring themes in negative reviews. This directly informs business decisions (which team should act, what to prioritize) without needing to predict anything about any single new document.

4. **Organizing and browsing an unlabeled archive.** Tagging each document with its dominant topic(s) enables filtering/browsing a large collection by theme (e.g., a digital library auto-sorting papers by inferred subject), or improving retrieval by matching on topic similarity rather than exact keyword overlap.

5. **Monitoring trends over time.** Running the same topic model over a time-sliced corpus (e.g., weekly social media mentions) reveals how the *proportion* of each theme shifts week over week — an early-warning signal for emerging issues, exactly matching the motivating business scenario from Section 2 (monitoring what's being said about a product, and whether it's shifting).

The general pattern — and it's the same pattern behind Clustering and Association Rules, so it's worth stating explicitly: **unsupervised/descriptive output has no external "correct answer" to be scored against, but it is not a dead end.** It becomes the basis for human decisions, for visualization, or for the *input features* of a later supervised stage whose predictions genuinely can be validated. "Descriptive" describes what the *method itself* does (summarize existing structure), not a ceiling on what the *pipeline as a whole* can accomplish with that summary.

---

## 7. Sentiment Analysis (Supervised, for Contrast)

Uses statistics + NLP to mine subjective opinions from text, at the document, sentence, phrase, or short-text level.

**Traditional approach**: reuses the exact Classification algorithms from earlier weeks — Naïve Bayes, Maximum Entropy, SVM — on BoW features.

**Slide example (Movie Review Corpus, 2000 reviews, 1000 positive/1000 negative, manually labeled)**:
1. Use NLTK.
2. Split 1600 train / 400 test — the same train/test structure from the Classification lecture.
3. Represent with BoW features.
4. Naïve Bayes trained on the training set achieves **73.5% accuracy** on the test set, and can surface the "most informative features" (which words most strongly drive the positive/negative prediction).

**Limitations of the traditional approach**: a classifier trained on one domain doesn't transfer well to another (word meaning varies by domain — "sharp" is praise for a knife or an image, but a complaint about taste); an absolute sentiment score is meaningless without a baseline for comparison; and getting enough *labeled* data at scale is hard (mitigated with emoticon-as-label heuristics, or crowdsourced labeling via Amazon Mechanical Turk).

**Modern note**: in the LLM era, sentiment analysis has shifted from lexicon/feature-based classifiers to prompting, fine-tuning, and few-shot learning with pretrained language models — simpler, more context-robust, and considerably more powerful, and is now the mainstream approach in place of the BoW+Naïve Bayes pipeline above.

### Topic Modeling vs. Sentiment Analysis — the key branch point of the whole lecture

| | Topic Modeling (LDA) | Sentiment Analysis |
|---|---|---|
| Learning type | **Unsupervised** — no "correct topic" label exists at train time | **Supervised** — requires pre-labeled positive/negative examples |
| Goal | Descriptive — summarize latent thematic structure | Predictive — classify new text into a discrete sentiment label |
| Same family as | Clustering, Association Rules | Classification (Naïve Bayes, Logistic Regression) |

---

## 8. Gaining Insights

- **Word cloud**: word-frequency visualized by font size — fast, but crude (doesn't distinguish "genuinely distinctive" from "just common").
- **TF-IDF highlighting**: highlighting the highest-TF-IDF words within each individual review immediately surfaces what's distinctive about *that* review ("minor bugs," "mint condition," "buttons did not work" — each one tells its own specific story instead of a generic word list).
- **Circular graph / LDA topic visualization**: disc size represents a word's weight within a topic — lets you "read" a topic's meaning at a glance without reading every underlying document.

---

## 9. Word Embeddings

**The problem with one-hot encoding** (which is what BoW reduces to at the single-word level): each word is a vector with a single 1 and the rest 0s, so there is **no notion of "closeness"** between related words — "cat" and "kitten" are just as far apart as "cat" and "car." This fails to capture generalization across related words.

**Word embeddings** solve this by learning a **dense**, low-dimensional vector for each word (learned automatically from data), such that semantically related words end up close together in that space.

**A remarkable property — vector arithmetic encodes relationships.** The vector difference B − A appears to encode a specific *type* of relationship — famously, "Athens is to Greece as Oslo is to [what]?" → D = C + (B − A), where (B − A) is the learned "capital-of" relationship vector, added to C (Oslo) to approximate D (Norway).

**Why embeddings became popular**: they are a strong general-purpose representation for downstream tasks (question answering, translation, summarization); pre-trained vectors (Word2Vec, GloVe, FastText) are available off the shelf, or you can train your own on a domain-specific corpus for a specific task.

---

## 10. Latest Developments — From Word Embeddings to LLMs

**From word embeddings to contextual embeddings.** Word2Vec/GloVe/FastText give each word **one fixed vector** regardless of context — but "bank" in "the bank of the river" and "bank" in "apply for a loan from the bank" arguably shouldn't share a representation. **Contextual embeddings** (BERT, Sentence-BERT) represent a word according to its **surrounding context**, so the same word can take different vectors in different sentences — directly resolving the homonym problem raised in Section 1.

Evolution of text representation: **BoW/TF-IDF → Word Embeddings → Contextual Embeddings.**

**From task-specific models to general-purpose LLMs.** Traditional pipeline: Text → Features (TF-IDF/BoW) → a model built for **exactly one task** → Prediction (TF-IDF + classifier for document classification, LDA for topic discovery, BoW + Naïve Bayes for sentiment — literally the three techniques covered in this lecture). LLMs change the shape of the pipeline entirely: Text + Instruction → a pretrained LLM (Transformer architecture, trained on massive text collections) → **many different tasks from one model** (classification, sentiment, information extraction, question answering, summarization, translation, text generation), supporting zero-shot and few-shot learning without task-specific retraining.

**Beyond LLMs — Search, RAG, and AI Agents.**
1. **Semantic Search**: traditional search matches keywords; modern semantic search embeds the query and retrieves documents that are close *in meaning*, not just in wording.
2. **Retrieval-Augmented Generation (RAG)**: Question → retrieve relevant information → feed to an LLM → Answer. Combines information retrieval with LLMs, letting the model draw on external or organization-specific knowledge — important for analyzing large internal document collections.
3. **AI Agents**: an LLM becomes a component in a system that can Understand → Search → Use Tools → Reason → Act, interacting with databases, search engines, APIs, and other software.

---

## 11. Summary — The Evolution of Text Analytics

```
Traditional:  Raw Text → Preprocessing → BoW/TF-IDF → Statistical/ML models → Topic Modeling / Classification / Sentiment Analysis
Modern:       Word Embeddings → Contextual Embeddings → Transformers/LLMs → Semantic Search / RAG / AI Agents
```

The underlying goal never changes across generations of technology: turning unstructured text into useful information, knowledge, and insight — only the tools available to do it keep getting more powerful.

**Tying it back to earlier weeks** (this is the same supervised/unsupervised split you worked out for Clustering and Regression):

- Topic Modeling (LDA) = unsupervised + descriptive → same family as Clustering (you pick K in advance, exactly as in K-means) and Association Rules (discovers latent structure with no ground truth to score against) — but as Section 6 shows, its output routinely becomes the *input* to a later, validatable, supervised stage.
- Sentiment Analysis = supervised + predictive → same family as Classification (and Logistic Regression is a classic alternative to Naïve Bayes here) — requires labeled training data, evaluated with accuracy/confusion-matrix exactly as in the Classification lecture.
