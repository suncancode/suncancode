# Lecture 2 — MapReduce Framework

---

## 0. How This Lecture Connects to the Rest of the Course

Lecture 1 established *why* we need clusters and Hadoop (Big Data breaks single-machine, traditional architectures). This lecture answers the next question: **once you have a cluster of machines, how do you actually tell it what computation to perform on a huge dataset spread across many nodes?**

MapReduce is the answer Hadoop originally used (and still supports). It is a **programming model** — a pattern for how to *write* your program — not a specific piece of software by itself. Lecture 3 (Hadoop Architecture) will then show you the actual machinery (HDFS + YARN) that Hadoop uses to physically execute a MapReduce job across the cluster. So the logical order is:
1. **This lecture (the model):** what shape must your program take (Map phase + Reduce phase) so that it *can* be automatically parallelized across a cluster?
2. **Next lecture (the mechanics):** which daemons/processes in Hadoop actually schedule, run, and coordinate the Map and Reduce tasks across the nodes?

---

## 1. MapReduce — The Programming Model

### 1.1 What is MapReduce?

**From the lecture:**
- MapReduce is the **most important processing framework in Hadoop**.
- Many high-level data processing languages are **abstractions of MapReduce** — for example, **Pig**, **Hive**, and **Spark** are heavily influenced by MapReduce concepts.
- Historically, **Hadoop version 1 supported MapReduce only** (i.e., there was no separate resource manager like YARN yet — this is expanded on in Lecture 3).
- MapReduce is also a **platform- and language-independent programming model** at the heart of most big data and NoSQL platforms.
- A **programming model** is a pattern/format in accordance with which we write our programs.
- The logic of a MapReduce application consists of a **Map phase** and a **Reduce phase**.

**Explanation:**
Calling MapReduce "platform- and language-independent" means the *idea* of Map and Reduce phases isn't tied specifically to Hadoop or to Java — it's a general pattern that has been re-implemented in many languages and many systems (this is exactly why Pig, Hive, and Spark, even though they present very different-looking interfaces to the user, were originally built on or influenced by the same underlying Map/Reduce idea).

### 1.2 Why was MapReduce created? — Limitations of earlier approaches

**From the lecture — limitations of early distributed computing and grid computing frameworks:**
- Complexity in parallel programming
- Hardware failures
- Bottlenecks in data exchange
- Scalability problems

**Explanation:**
Before MapReduce, if you wanted to process a huge amount of data across many machines, you (the programmer) had to manually handle an enormous amount of low-level plumbing:
- Deciding how to split the data across machines,
- Sending code/data to the right machines,
- Detecting and recovering from a machine crashing mid-job,
- Coordinating when machines needed to exchange intermediate results,
- Combining partial results back together.

This was extremely error-prone and required deep expertise in distributed systems just to do basic data processing. MapReduce's key insight was to **separate "what to compute" from "how to distribute and coordinate it."** The programmer only writes two simple functions (map and reduce); the underlying framework (later, Hadoop) handles all the distribution, fault tolerance, and coordination automatically. This directly addresses every one of the four limitations listed above.

### 1.3 The 2004 Google MapReduce design goals

**From the lecture:**
The 2004 Google MapReduce white paper set out the following design goals for MapReduce:
- **Automatic parallelization and distribution**
- **Fault tolerance**
- **Input/output (I/O) scheduling**
- **Status and monitoring**

**Explanation:**
- **Automatic parallelization and distribution:** the framework itself decides how to split work across many machines — the programmer doesn't write any explicit multi-threading or networking code.
- **Fault tolerance:** if a machine fails partway through a job, the framework automatically detects this and reassigns that piece of work to another healthy machine — the programmer doesn't have to write any recovery logic.
- **I/O scheduling:** the framework manages when and how data is read from and written to storage, including trying to schedule computation close to where the data physically resides (this becomes the "data locality" idea covered in Section 3 below).
- **Status and monitoring:** the framework provides visibility into how a job is progressing (e.g., how many map/reduce tasks are done, failed, or still running), so operators/users can track large jobs that might run for a long time across hundreds of machines.

This white paper (by Jeffrey Dean and Sanjay Ghemawat at Google, 2004) is historically the origin of the MapReduce idea; Hadoop is the most well-known open-source implementation inspired directly by it (along with the Google File System paper, which inspired HDFS — covered in Lecture 3).

### 1.4 The key-value pair model

**From the lecture:**
- The MapReduce model uses **key-value pairs** for processing data.
- A classic illustrative example given is **WordCount** — often called the "Hello World" of MapReduce.

**Explanation — how WordCount works (the standard example used across essentially every MapReduce course, filling in the mechanics the slide only names):**

The goal of WordCount is: given a large collection of text, count how many times each word appears.

**Map phase:**
- Input: raw lines of text, conceptually represented as key-value pairs of `(line_number, line_text)`.
- The **map function** processes each line independently and, for every word it finds, emits an intermediate key-value pair: `(word, 1)`.
- Example: for the line `"the cat sat on the mat"`, the mapper emits:
  `(the, 1), (cat, 1), (sat, 1), (on, 1), (the, 1), (mat, 1)`

**Shuffle & Sort (happens automatically between Map and Reduce — this is done by the framework, not written by the programmer):**
- All intermediate pairs with the **same key** are grouped together across the whole cluster.
- Example: all the `(the, 1)` pairs from every mapper, from every machine, are grouped into `(the, [1, 1, 1, ...])`.

**Reduce phase:**
- The **reduce function** receives a key and the full list of values associated with that key, and combines/aggregates them.
- For WordCount, reduce simply sums the list: `(the, [1,1,1]) → (the, 3)`.
- Output: a final key-value pair per word, giving its total count across the entire dataset: `(the, 3), (cat, 1), (sat, 1), (on, 1), (mat, 1)`.

This example illustrates the general MapReduce pattern:
```
Input data → [ MAP: transform each record into (key, value) pairs ]
           → [ SHUFFLE/SORT: group all values by key, automatically, across the cluster ]
           → [ REDUCE: aggregate/summarize the values for each key ]
           → Final output
```
Notice this maps cleanly onto why key-value pairs matter: they give the framework a simple, uniform way to decide *what needs to be grouped together* (everything with the same key) so that the Reduce step can be automatically parallelized too — each distinct key (or range of keys) can be processed by a different reducer, on a different machine, independently.

---

## 2. Real-World Scenario: Log Data Analysis

**From the lecture:**
- In online purchasing, users sometimes **abandon their shopping carts** before completing the purchase.
- To improve their business, companies are usually interested in finding out more about the **nature of these abandoned purchases**.
- The slide references "A MapReduce job for this analysis" (illustrated visually in the original slide).

**Explanation:**
This scenario is a realistic, business-driven use case for MapReduce, and it's worth walking through conceptually since it echoes the WordCount pattern:

- **Raw input:** massive web server / application **log files** recording user actions — page views, "add to cart" events, "checkout started" events, "purchase completed" events — each with a timestamp and (for example) a session or user ID. This is a textbook example of the log/clickstream data mentioned as an "example of Big Data" in Lecture 1 (Section 2.4).
- **Map phase (conceptually):** for each log line, a mapper could emit something like `(session_id, event_type)` or `(session_id, (event_type, timestamp))` — extracting the relevant fields from the messy raw log text.
- **Shuffle/Sort:** the framework automatically groups all events belonging to the **same session** together, regardless of which physical machine or which log file they originally came from.
- **Reduce phase (conceptually):** for each session's full sequence of events, the reducer can determine: did this session reach "add to cart" but never reach "purchase completed"? If so, it's an abandoned cart. The reducer can then aggregate these results — e.g., counting abandoned carts by product category, time of day, or geography.
- **Business value:** this kind of analysis directly ties back to the "Value" and "Viability" V's from Lecture 1 — the whole point of processing this Big Data is to extract actionable business insight (e.g., "carts are most often abandoned at the shipping-cost step," prompting a business change).

This is a good example of why MapReduce (and Big Data tooling generally) matters in practice: this analysis would be essentially impossible to run efficiently on one machine against logs from a large e-commerce site, but is a very natural fit for the Map (per-event) / group-by-key (per-session) / Reduce (per-session summarization) pattern.

---

## 3. MapReduce Implementation in Hadoop

### 3.1 What Hadoop's implementation gives you

**From the lecture:**
- Hadoop MapReduce **frees users from the low-level communication and coordination of nodes and processes**.
- It lets programmers **focus on the MapReduce implementation** (i.e., just writing the map and reduce functions) **and a few configuration parameters**, rather than distributed-systems plumbing.

**Explanation:** This is the direct payoff of the design goals in Section 1.3 — "automatic parallelization and distribution" and "fault tolerance" mean the programmer really does only need to write the map() and reduce() logic; Hadoop's underlying execution engine (detailed fully in Lecture 3's discussion of YARN) takes care of everything else: splitting the input, scheduling tasks on nodes, retrying failed tasks, performing the shuffle/sort, and collecting the final output.

### 3.2 Data locality

**From the lecture:**
- Because the data file is usually too large to be stored on a single persistent storage device of commodity hardware, **Hadoop handles the shipment of code to data fragments** — this is called **data locality**.
- This can **dramatically reduce the overhead of network transmission**.

**Explanation — this is one of the single most important ideas in the entire Hadoop philosophy:**
In a traditional computing model, you would move *data* to where the *program* is running (e.g., copy files over the network to a central server, then process them). In a Big Data cluster, the data is enormous and already spread across hundreds of machines, so moving all of it to one place would be incredibly slow and would create the exact "bottleneck in data exchange" problem noted in Section 1.2 as a limitation of earlier approaches.

MapReduce/Hadoop flips this around: instead of moving data to the code, it **moves the (small) code to wherever the data already lives**, and runs the Map task locally, on the same machine (or at least the same rack) that already stores that piece of data. Since program code is tiny compared to the data it processes, shipping code is vastly cheaper than shipping data across the network. This principle — **"move computation to the data, not data to the computation"** — is exactly why, in Lecture 3, you'll see that HDFS (storage) and YARN (computation scheduling) are designed to work closely together and are typically deployed on the *same* physical machines, rather than as separate storage-only and compute-only clusters.

### 3.3 Why Hadoop is useful for Big Data

**From the lecture — the full list given:**
- Cost-effective, fault-tolerant storage (HDFS)
- Scalability
- Data that is ingested may be interpreted at runtime (i.e., schema-on-read, as discussed for Data Lakes in Lecture 1)
- Low cost in storing unstructured and semi-structured data
- Fast transfer of data into storage
- Separation of programming logic and scheduling/management
- Multiple levels of distributed system abstractions: Hive, Pig, Spark
- Multi-language tooling:
  - **Java, Python** → MapReduce
  - **SQL** → Hive
  - **Data-flow** → Pig
  - **Scala, Python** → Spark

**Explanation — tying this list back to earlier concepts:**
- "Cost-effective, fault-tolerant storage" and "scalability" are the direct payoff of the commodity-hardware + replication design discussed for Hadoop in Lecture 1 (Section 4.2).
- "Data ingested may be interpreted at runtime" and "low cost storing unstructured/semi-structured data" are the direct payoff of Hadoop's schema-on-read philosophy — contrasted with the traditional, schema-on-write data warehouse approach also discussed in Lecture 1 (Section 3.1–3.3).
- "Separation of programming logic and scheduling/management" is exactly the benefit described in Section 3.1 above — you write map()/reduce(), Hadoop handles the rest.
- The "multiple levels of abstraction" and "multi-language tooling" rows are your first explicit preview of what's coming later in the course: Hive (SQL-like queries) and Pig (data-flow scripting) are both built as higher-level abstractions *on top of* the same underlying MapReduce concepts you learned in this lecture, and Spark is a related-but-distinct engine (mostly in-memory, generally faster) that also builds on these ideas — all of which appear in later weeks of this unit.

---

## 4. References (as given in the lecture)

- White, T. *Hadoop: The Definitive Guide — Storage and Analysis at Internet Scale*, O'Reilly, 2015. (Available through UOW library)
- Vohra, D. *Practical Hadoop Ecosystem: A Definitive Guide to Hadoop-Related Frameworks and Tools*, Apress, 2016. (Available through UOW library)
- Aven, J. *Hadoop in 24 Hours, SAMS Teach Yourself*, SAMS, 2017.
- Alapati, S. R. *Expert Hadoop Administration: Managing, Tuning, and Securing Spark, YARN and HDFS*, Addison-Wesley, 2017.
- Apache Hadoop (official site)
- Apache Hadoop, MapReduce Tutorial (official documentation)

---

## 5. Self-Check Questions (for revision)

1. What are the two phases that make up the logic of a MapReduce application?
2. Name the four limitations of earlier distributed/grid computing frameworks that MapReduce was designed to solve.
3. List the four design goals of MapReduce from Google's 2004 white paper, and explain each in one sentence.
4. Walk through the WordCount example: what key-value pairs does the Map phase emit, and what does the Reduce phase do with them?
5. What happens in the "shuffle and sort" step, and why is it necessary before the Reduce phase can run?
6. In the abandoned-shopping-cart scenario, what would a reasonable map-phase key be, and why?
7. What does "data locality" mean, and why does it dramatically reduce network overhead?
8. Explain the phrase "move computation to the data, not data to the computation."
9. What does it mean that MapReduce is a "platform- and language-independent programming model"?
10. Name three high-level tools mentioned as being "abstractions of MapReduce," and the language/interface each one uses.
11. Why does separating "programming logic" from "scheduling/management" make Hadoop easier to use than earlier distributed computing frameworks?
