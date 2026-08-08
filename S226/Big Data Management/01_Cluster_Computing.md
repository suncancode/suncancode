# Lecture 1 — Cluster Computing

---

## 0. The Big Picture — Where This Lecture Fits in the Course

Before diving into details, it helps to see the whole map of the subject, because Lecture 1 is essentially the "why" that motivates everything else you'll learn.

**The core problem the whole course solves:**
Traditional single-machine systems (a single powerful server, a single relational database) cannot store or process data once it grows past a certain size, arrives too fast, or is too irregularly structured. The subject teaches you, layer by layer, how the industry solved this problem — starting from raw hardware clusters, moving up to Hadoop, and then to higher-level tools built on top of Hadoop.

A typical progression through the subject (based on the structure visible in this unit's public teaching material) looks like this:

```
Week 1  → Foundations: Cluster Computing → MapReduce (the model) → Hadoop Architecture (HDFS + YARN)
Week 2  → HDFS Interfaces (how to actually use HDFS) → MapReduce Data Processing Model (deeper dive)
Week 3  → Writing real MapReduce applications (e.g., in Python)
Week 4  → Data Warehouse Concepts, Hive Data Structures
Week 6  → SQL for Data Warehousing
Week 9  → Pig Latin (a data-flow language on top of Hadoop)
(also covered elsewhere in the unit: HBase Data Model, Introduction to Spark)
```

So the mental model is:

1. **Hardware/infrastructure layer** — computer clusters (this lecture).
2. **Programming model layer** — MapReduce (Lecture 2): *how* you tell a cluster what computation to do.
3. **Platform layer** — Hadoop (Lecture 3): the concrete open-source system that implements storage (HDFS) + resource management (YARN) + the MapReduce engine.
4. **Higher-level tools layer** (later weeks) — Hive (SQL-like queries), Pig (data-flow scripting), HBase (NoSQL database), Spark (faster in-memory alternative to MapReduce) — all of these sit *on top of* Hadoop so that people don't have to write raw MapReduce code by hand.
5. **Data warehousing / SQL layer** (later weeks) — how Big Data techniques connect back to classic data warehousing concepts (star schemas, OLAP, SQL).

**Why this matters for how you study Lecture 1:** everything here — clusters, the 3 V's, Hadoop's philosophy of "commodity hardware + fault tolerance + move-code-to-data" — is the justification for every design decision you'll see in HDFS and YARN in Lecture 3, and for why MapReduce looks the way it does in Lecture 2. If you understand *why* Big Data broke traditional architectures, the rest of the course reads as "engineering solutions to specific problems," not a random pile of tool names.

**The outline of this lecture (from the slides):**
- Computer Cluster
- Big Data
- Traditional Data Architectures
- Meet Hadoop!
- Big Data on Database Clusters
- Big Data on Kubernetes

---

## 1. Computer Cluster

### 1.1 What is a computer cluster?

**From the lecture:**
- A computer cluster is a **collection of computers (nodes)** connected through a **high-speed local area network (LAN)** that work together to simulate a single, much more powerful computer system.
- Each node in a computer cluster is controlled by **its own operating system**.
- Each node in a computer cluster performs a **different version of the same task**.
- **Cluster vs. Grid:** in a computer *grid*, the nodes perform *different* tasks (heterogeneous work), whereas in a computer *cluster*, the nodes perform *the same kind* of task (just on different pieces of data or work).
- The architecture of a computer cluster ranges from a simple two-node system (connecting two personal computers) up to a supercomputer built with a cluster architecture.

**Explanation:**
Think of a cluster like a team of identical workers, each doing the same *type* of job (e.g., "process this chunk of the file") but each on a different piece of the overall workload — as opposed to a grid, which is more like a factory with specialized stations (accounting, printing, packaging) each doing something different. This distinction matters later: Hadoop's worker nodes are a **cluster** in this strict sense — every DataNode/NodeManager runs the *same* software and can, in principle, do the *same kind* of work as any other node.

### 1.2 Why use clusters?

**From the lecture:**
- Clusters speed up computing through:
  - **Shared-nothing (sharding) partitioning** of data, and
  - **Parallelization** of data processing across the nodes.
- Clusters provide **high availability** through **automatic replacement of a failed node with a replica node**.
- **Advantages of computer clusters:**
  - Faster processing speed
  - Larger storage capacity
  - Better data integrity
  - Greater reliability
  - Wider availability of resources
- A **Linux cluster** is a collection of connected computers that can be viewed and managed *as a single system*.

**Explanation — "shared-nothing" architecture:**
"Shared nothing" means each node has its own private CPU, memory, and disk — nodes don't compete for the same physical hardware resource, they only communicate over the network. This is the opposite of "shared everything" (e.g., multiple CPU cores sharing one big memory pool). Shared-nothing is what allows a cluster to scale almost linearly: adding a new node adds its own independent CPU/RAM/disk rather than adding contention on a shared resource.

### 1.3 A real sample cluster (as an example, from the lecture)

- **54 regular compute nodes**, each with:
  - Two 32-Core Intel 8358 processors
  - 1.6 TB of local NVMe storage
  - 512 GB of memory
- **5 GPU nodes**, each with:
  - Two 24-Core AMD EPYC 7413 processors
  - Eight A100 GPU cards
  - 960 GB of local storage
  - 512 GB of memory

**Explanation:** This example is meant to make "cluster" concrete — it isn't an abstract idea, it's literally dozens of real machines wired together, each contributing CPU cores, memory, and storage to a shared pool of computing power. Note the mix of regular compute nodes and specialized GPU nodes — real-world clusters are often heterogeneous at this level even though, within the "compute cluster" definition, nodes running the same job still do the same *kind* of task.

### 1.4 What is cluster computing?

**From the lecture:**
- **Cluster computing** is the *process* of sharing computation tasks among the multiple computers included in a computer cluster.
- **Advantages of cluster computing:** cost efficiency, processing speed, expandability, high availability of resources.
- Cluster computing is currently an attractive paradigm for processing large-scale science, engineering, and commercial applications.
- Cluster computing requires **specialized algorithms** such as:
  - Load balancing
  - Resource sharing
  - Resource scheduling
  for optimization of data processing.
- Cluster computing is an attractive **alternative** to data processing on large parallel supercomputers (i.e., you can often get supercomputer-like power from many cheap machines instead of one very expensive specialized machine).
- The **simplest configuration** of nodes for cluster computing consists of a **master node** and **slave (worker) nodes**.

**Explanation:**
- **Load balancing** = spreading work evenly across nodes so no single node becomes a bottleneck while others sit idle.
- **Resource scheduling** = deciding *when* and *where* (on which node) a task should run, given the resources currently available.
- The **master–slave** pattern introduced here is the same pattern you'll see again explicitly in Hadoop: one (or a small number of) coordinating node(s) that manage metadata/scheduling, and many worker nodes that do the actual storage/computation. This is one of the most important recurring ideas in the whole subject.

---

## 2. Big Data

### 2.1 What does "Big Data" mean, and how big is Big Data?

**From the lecture:**
- Big Data is data **so big that it cannot be stored on the persistent storage devices attached to a single computer system**.
- Big Data may also mean an **infinite amount of data** (i.e., data that is continuously and indefinitely generated, such as a never-ending stream).

**Explanation:**
This definition is deliberately *relative*, not a fixed number of gigabytes/terabytes. "Big" is defined in relation to what a single machine can handle. This is important because it directly motivates why we need *clusters* (Section 1) — if the data literally will not fit on one machine's disks, or will never stop arriving, you are forced into a distributed, multi-machine architecture no matter what.

### 2.2 Sources of Big Data

**From the lecture:** The slide poses the question "What are the sources of Big Data?" and illustrates it visually (the original is a diagram/graphic rather than a bullet list, so the visual itself isn't reproducible here).

**Explanation (general knowledge, to fill this in conceptually):** Typical sources of Big Data discussed in this space include:
- Social media platforms (posts, likes, shares)
- Mobile devices and apps (GPS/location data, usage logs)
- Internet of Things (IoT) sensors (industrial sensors, smart home devices, wearables)
- Transaction and financial systems (credit card transactions, stock trades)
- Web activity (clickstreams, search logs)
- Enterprise systems (ERP, CRM data)
- Scientific instruments (telescopes, genome sequencers, particle colliders)

These map closely onto the "Examples of Big Data" list given explicitly in the next slide (Section 2.4).

### 2.3 The "V" Characteristics of Big Data

**From the lecture — the core 3 V's:**
| V | Meaning |
|---|---|
| **Volume** | The sheer scale of data — e.g., billions of rows, millions of columns |
| **Variety** | The complexity of data types and structures (structured, semi-structured, unstructured, mixed) |
| **Velocity** | The speed at which new data is created and grows |

**From the lecture — additional V's mentioned explicitly:**
| V | Meaning |
|---|---|
| **Veracity** | The ability to represent and process uncertain and imprecise data |
| **Value** | Data is the driving force of next-generation business |
| **Viability** | The benefits we can potentially gain from data analysis |
| **Vagueness** | The meaning of the data found is often unclear, regardless of how much data is available |
| **Validity** | Rigor in analysis is essential for valid predictions, since data drives next-generation business |
| **Vane** | Data science can aid decision-making by pointing in the correct direction |

- The lecture notes, half-jokingly, that people online have proposed as many as **42 different "V" words** to describe Big Data properties — the point being that 3V (or 5V, 7V…) is a *framework for thinking*, not a rigid checklist.

**Explanation:**
The "V model" is the most widely cited way to characterize what makes data "Big Data" rather than just "a lot of data." A practical way to internalize the original 3 V's:
- **Volume** → *storage and processing scale* problem → solved by distributed storage/compute (HDFS, MapReduce, clusters).
- **Variety** → *schema/structure* problem → solved by schema-flexible storage (NoSQL, "schema-on-read" as opposed to the traditional "schema-on-write").
- **Velocity** → *throughput/latency* problem → solved by streaming systems and fast ingestion pipelines (e.g., Kafka, mentioned later in the Hadoop cluster composition).

### 2.4 Examples of Big Data

**From the lecture:**
- Clickstream data
- Call centre data
- E-mail and instant-messaging
- Sensor data
- Unstructured data
- Geographic data
- Satellite data
- Image data
- Temporal data
- …and more

**Explanation:** Notice how varied these are — some are highly structured (temporal/timestamped logs), some are completely unstructured (raw text of emails, images). This diversity is exactly what the "Variety" V is describing, and it's also exactly why traditional relational databases (which expect a fixed, predefined schema) struggle with Big Data.

---

## 3. Traditional Data Architectures

### 3.1 Strengths of traditional data architectures

**From the lecture:**
- Centralised governance of data repositories
- Lightning-fast queries performed regularly in daily business ("light-fast inquiries")
- Optimisation for **OLTP** and **OLAP**
- Security and access control
- Fault tolerance and backup

**Explanation — OLTP vs OLAP (useful background):**
- **OLTP (Online Transaction Processing):** systems optimized for many small, fast read/write transactions — e.g., processing a single retail sale, updating one bank account balance.
- **OLAP (Online Analytical Processing):** systems optimized for large, complex analytical queries over historical data — e.g., "what were total sales by region for each of the last 5 years?"
Traditional relational database and data warehouse systems were purpose-built and tuned for exactly these two well-understood workloads over decades, which is why they remain strong at them.

### 3.2 Challenges for traditional data architectures

**From the lecture:**
- New types of data such as unstructured and semi-structured data
- Increasingly large amounts of data flowing into organisations
- New computational paradigms using non-traditional **NoSQL** databases to rapidly mine and analyse very large data sets
- Increasing cost of storing and analysing large amounts of data
- Increasing use of data analytics, which requires significant storage and processing capabilities

**Explanation:** This is the direct "problem statement" for the whole course. Traditional systems were built assuming: (a) data fits on one system or a small, tightly-controlled cluster of expensive servers, (b) data has a fixed, known schema in advance, and (c) query patterns are relatively predictable. Big Data breaks all three assumptions, which is exactly why Section 2's challenges (Volume, Variety, Velocity) required a new architecture — which the rest of the lecture (Hadoop) introduces.

### 3.3 Data Lake architecture

**From the lecture:** The slide shows "A sample Data Lake architecture" as a diagram (visual, not text).

**Explanation:** A **Data Lake** is a storage repository that holds a vast amount of raw data in its native/original format (structured, semi-structured, and unstructured) until it is needed, as opposed to a traditional **Data Warehouse**, which stores processed, structured data organized for a specific purpose (typically reporting/analytics) — data is transformed *before* it is loaded (schema-on-write). A Data Lake instead follows a "schema-on-read" philosophy — you decide how to interpret/structure the data only when you actually query or process it. This is directly relevant to Hadoop, since HDFS is very commonly used as the storage layer underneath a Data Lake.

### 3.4 Hardware scalability dimensions

**From the lecture:** "Hardware for Big Data has two scalability dimensions" (shown as a diagram).

**Explanation — the two standard scalability dimensions referred to here are:**
1. **Vertical scaling (scale-up):** making a *single* machine more powerful — adding more CPU, RAM, or disk to one server. This has a hard ceiling (you eventually can't add more hardware to one box) and gets expensive fast at the high end.
2. **Horizontal scaling (scale-out):** adding *more machines* to a cluster rather than making one machine bigger. This is the approach Big Data systems (like Hadoop) are built around, because it can scale almost without limit by simply adding more commodity nodes, and it's usually far more cost-effective than vertical scaling.

This distinction is the hardware-level justification for why Big Data platforms are built as clusters (Section 1) rather than as ever-bigger single servers.

---

## 4. Meet Hadoop!

### 4.1 What is Hadoop?

**From the lecture:**
- Hadoop, in terms of its developers, is a project that develops **open-source software for reliable, scalable, distributed computing**.

### 4.2 Features of Hadoop

**From the lecture:**
- Capability to handle large data sets — simple scalability and coordination
- File sizes ranging from gigabytes to terabytes
- Can store **millions** of such files
- High fault tolerance
- Supports **data replication**
- Supports **streaming access** to data
- Supports **batch processing**
- Supports **interactive, iterative, and stream processing**
- Implements a data consistency model of **write-once-read-many (WORM)** access
- Runs on **commodity hardware**, not high-performance computers
- **Inexpensive**
- Can be deployed **on-premises or in the cloud**

**Explanation — "write-once-read-many" (WORM):**
This means once a file is written to HDFS, it is not expected to be modified afterward (no arbitrary in-place edits, though appends are supported in modern Hadoop) — it can only be read (possibly many times, by many processes) afterward. This greatly simplifies consistency and replication, at the cost of not supporting typical database-style updates. This directly foreshadows a limitation you'll see explicitly stated for HDFS in Lecture 3 ("not designed for … multiple writers, arbitrary file modifications").

**Explanation — "commodity hardware":**
"Commodity hardware" means ordinary, mass-produced, relatively inexpensive servers — not specialized supercomputer-grade equipment. Because such hardware fails more often than premium hardware, Hadoop is designed from the ground up to *expect* and *tolerate* individual machine failures (through replication and automatic recovery) rather than trying to prevent failures altogether. This is a deliberate cost/reliability trade-off: many cheap, failure-prone machines + software-level fault tolerance, instead of few expensive, highly-reliable machines.

### 4.3 Core components of Hadoop

**From the lecture:** The slide shows "Core components of Hadoop" as a diagram (visual, not text).

**Explanation:** Hadoop's core is typically described as three layers, which map directly onto the rest of this course:
1. **HDFS (Hadoop Distributed File System)** — the storage layer (covered in depth in Lecture 3).
2. **YARN (Yet Another Resource Negotiator)** — the resource management/coordination layer (also covered in depth in Lecture 3).
3. **MapReduce** — the original processing/computation layer (covered in depth in Lecture 2).

### 4.4 The Hadoop Ecosystem

**From the lecture:** The slide shows the "Hadoop ecosystem" as a diagram (visual, not text).

**Explanation:** Beyond the three core components above, an "ecosystem" of tools is typically built on top of Hadoop to make it easier to use for different purposes — several of which appear later in this course's syllabus:
- **Hive** — SQL-like querying on top of Hadoop data (data warehousing use case)
- **Pig** — a high-level data-flow scripting language (Pig Latin) for processing data on Hadoop
- **HBase** — a NoSQL, column-oriented database built on top of HDFS
- **Spark** — a faster, largely in-memory alternative/complement to MapReduce
- **Sqoop** — a tool for transferring data between Hadoop and relational databases
- **Flume/Kafka** — tools for ingesting streaming/log data into Hadoop
- **Zookeeper** — a coordination service used by many distributed systems (including Hadoop) to manage configuration and synchronization
- **Oozie** — a workflow scheduler for Hadoop jobs

As noted in Section 3 of the MapReduce lecture: "Many high-level data processing languages are abstractions of MapReduce" — Pig, Hive, and Spark specifically are called out as being heavily influenced by MapReduce concepts.

### 4.5 Commercial Hadoop Landscape

**From the lecture:** The slide shows the "Commercial Hadoop landscape" as a diagram (visual, not text).

**Explanation:** This refers to companies and cloud vendors that historically packaged, supported, or extended Hadoop for enterprise customers — for example, distributions/services such as Cloudera, Hortonworks (later merged with Cloudera), MapR, and cloud-native managed Hadoop offerings like Amazon EMR, Google Cloud Dataproc, and Azure HDInsight. The general idea being illustrated is that Hadoop is not just an academic project — it has a real commercial ecosystem of vendors around it.

### 4.6 Master–slave architecture of Hadoop clusters

**From the lecture:** The slide shows the "Master-slave architecture of Hadoop clusters" as a diagram (visual, not text).

**Explanation:** This is the same master–slave concept introduced generally in Section 1.4, now applied specifically to Hadoop: certain nodes run "master" daemons (coordinating processes, e.g., the NameNode for HDFS and the ResourceManager for YARN), while the rest of the nodes run "slave"/worker daemons (e.g., DataNodes and NodeManagers) that do the actual storage and computation work. The full detail of exactly which daemon runs where is the subject of Lecture 3.

### 4.7 What a Hadoop cluster typically consists of

**From the lecture:**
- Hadoop clusters can support **up to 10,000 servers** and achieve **near-linear scalability** in computing power.
- A typical Hadoop cluster consists of:
  - A set of **master nodes (servers)** where the daemons supporting key Hadoop frameworks run.
  - A set of **worker nodes** that host the storage (HDFS) and computing (YARN) work.
  - **One or more edge servers**, used for accessing the Hadoop cluster to launch applications.
  - **One or more relational databases** (e.g., MySQL) for storing metadata repositories.
  - **Dedicated servers for special frameworks**, such as Kafka.

**Explanation — "near-linear scalability":** this means that, roughly speaking, doubling the number of nodes roughly doubles the processing capacity — a key promise of the shared-nothing, horizontally-scalable design discussed in Section 3.4.

**Explanation — edge servers:** An edge server (sometimes called a "gateway node") is a machine that isn't part of the core storage/compute cluster itself, but is where users/clients log in and submit jobs to the cluster — it acts as the entry point, keeping direct access to the master/worker nodes restricted.

### 4.8 Pseudo-distributed mode

**From the lecture:**
- Hadoop also supports a **pseudo-distributed mode**:
  - All HDFS and YARN daemons run on a **single node**.
  - It highly simulates a full cluster.
  - It is easy for beginners to practice with.
  - It is easy for testing and debugging.
- **This unit's lab setting uses pseudo-distributed mode** — the single node is an **Ubuntu 22.04 Virtual Machine (VM)**.

**Explanation:** Since setting up a real multi-machine cluster is expensive and complex, pseudo-distributed mode lets every daemon (NameNode, DataNode, ResourceManager, NodeManager, etc.) run as separate processes on **one** machine, communicating over network sockets exactly as they would across real machines. This is different from **standalone (local) mode**, where Hadoop runs with no distributed daemons at all (useful only for the simplest debugging), and from **fully-distributed mode**, which is the real production setup across many physical/virtual machines. Knowing your lab VM runs pseudo-distributed mode is directly useful context for any lab exercises in this course.

---

## 5. Big Data on Database Clusters

### 5.1 What is a database cluster?

**From the lecture:**
- A **database cluster** is a collection of databases managed by a **single instance** of a running database server.
- A very large database in a database cluster is **partitioned** over a number of smaller databases, each located on a separate node of a computer cluster.

### 5.2 Requirements and benefits

**From the lecture:**
- Database clustering **requires replication and sharding**.
- Database clustering **improves performance, availability, and scalability**.

**Explanation:**
- **Sharding** = splitting a large dataset into smaller, independent pieces ("shards"), each stored on a different node — this is how you get horizontal scalability for a database.
- **Replication** = keeping copies of the same data on multiple nodes — this is how you get high availability and fault tolerance (if one node dies, another has a copy of the same data).
- Together, sharding + replication let a "database cluster" survive node failures (like the general computer cluster in Section 1.2) while still scaling out for larger volumes of data (matching the "Volume" challenge from Section 2).

### 5.3 Classes of database systems supporting clustering

**From the lecture:**
| Class | Examples |
|---|---|
| **NoSQL systems** | MongoDB, RavenDB, Cassandra, Amazon Aurora |
| **NewSQL systems** | ClustrixDB, NuoDB, CockroachDB, Pivotal GemFire XD, Altibase, MemSQL, VoltDB |
| **Improved OldSQL systems** | Oracle RAC, SQL Server (Windows Server Failover Cluster), DB2 Cluster, PostgreSQL, MySQL Cluster |

**Explanation:**
- **NoSQL** ("Not Only SQL") systems were built from the ground up to be schema-flexible and horizontally scalable — a natural fit for the Variety and Volume challenges of Big Data.
- **NewSQL** systems try to combine the horizontal scalability of NoSQL with the strong consistency and SQL query language of traditional relational databases.
- **"Improved OldSQL"** refers to traditional relational database systems (Oracle, SQL Server, DB2, PostgreSQL, MySQL) that have added clustering/replication features on top of their classic single-node architecture, so they can also participate in a clustered, higher-availability deployment.

---

## 6. Big Data on Kubernetes

### 6.1 What is Kubernetes?

**From the lecture:**
- **Kubernetes (K8s)** is a container/microservice platform that **orchestrates computing, networking, and storage infrastructure workloads**.
- In plain language: Kubernetes is an **orchestration platform to manage any containerized application**.
- A **Kubernetes cluster** consists of a **single master node** and potentially multiple corresponding **worker nodes**.

### 6.2 Benefits of Kubernetes

**From the lecture:**
- Horizontal scaling
- Automated rollouts and rollbacks
- Service discovery and load balancing
- Storage orchestration
- Self-healing
- Batch execution
- Automatic bin-packing

**Explanation:**
- A **container** (e.g., Docker) packages an application together with everything it needs to run (code, runtime, libraries) so it behaves consistently across different machines. Kubernetes automates the deployment, scaling, and management of many such containers across a cluster of machines.
- Notice the pattern again: **one master node + many worker nodes**, exactly mirroring the master–slave pattern seen in generic clusters (1.4), Hadoop clusters (4.6), and database clusters. This recurring master/worker theme is one of the most fundamental architectural ideas across all of distributed/Big Data systems.
- **"Self-healing"** means Kubernetes automatically restarts or replaces failed containers — directly analogous to the "automatic replacement of a failed node" property of computer clusters described in Section 1.2.
- This slide signals that Hadoop/HDFS/YARN is not the *only* way to run Big Data workloads today — modern practice increasingly also runs Big Data / distributed applications as containerized workloads orchestrated by Kubernetes, as an alternative or complement to traditional Hadoop clusters.

---

## 7. References (as given in the lecture)

- White, T. *Hadoop: The Definitive Guide — Storage and Analysis at Internet Scale*, O'Reilly, 2015. (Available through UOW library)
- Vohra, D. *Practical Hadoop Ecosystem: A Definitive Guide to Hadoop-Related Frameworks and Tools*, Apress, 2016. (Available through UOW library)
- Aven, J. *Hadoop in 24 Hours, SAMS Teach Yourself*, SAMS, 2017.
- Alapati, S. R. *Expert Hadoop Administration: Managing, Tuning, and Securing Spark, YARN and HDFS*, Addison-Wesley, 2017.

---

## 8. Self-Check Questions (for revision)

1. What is the difference between a computer cluster and a computer grid?
2. Why does "shared-nothing" architecture help clusters scale well?
3. Give the 3 core V's of Big Data and explain what problem each one causes for traditional systems.
4. Why is "Big Data" defined relative to a single machine's storage capacity rather than as a fixed number of terabytes?
5. What is the difference between OLTP and OLAP?
6. What is the difference between a Data Lake (schema-on-read) and a Data Warehouse (schema-on-write)?
7. What is the difference between vertical scaling and horizontal scaling, and which one does Hadoop rely on?
8. List at least five features of Hadoop that make it suitable for Big Data.
9. What does "write-once-read-many" mean, and why is it a reasonable trade-off for Hadoop?
10. What roles do master nodes, worker nodes, and edge servers play in a Hadoop cluster?
11. What is pseudo-distributed mode, and why is it used for this unit's labs?
12. What do sharding and replication each provide in a database cluster?
13. Name the three broad classes of database systems that support clustering, with one example each.
14. What does Kubernetes orchestrate, and what pattern does its master/worker cluster structure share with Hadoop clusters?
