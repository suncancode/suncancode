# Lecture 3 — Hadoop Architecture

---

## 0. How This Lecture Connects to the Rest of the Course

Lecture 1 explained *why* Hadoop exists (clusters + Big Data's 3 V's break traditional architectures). Lecture 2 explained the MapReduce *programming model* (map/reduce functions, key-value pairs) that lets you describe a computation in a way that *can* be automatically parallelized. **This lecture answers the final piece: which actual software processes (daemons), running on which machines, make all of that really happen?**

By the end of this lecture, the picture from Lecture 1's "core components of Hadoop" (Section 4.3) becomes concrete:
- **HDFS** = the storage layer → covered in Part 1 below.
- **YARN** = the resource-management/coordination layer → covered in Part 2 below.
- **MapReduce** = the processing layer (from Lecture 2) → which, as you'll see in Part 2, actually *runs on top of* YARN.

The lecture's own summary states explicitly: *"Next: Interaction with Hadoop and 'dive' into the MapReduce framework"* — meaning the following week (Week 2) goes on to cover HDFS Interfaces (how to actually operate HDFS) and a deeper dive into the MapReduce Data Processing Model, building directly on the architecture you learn here.

---

## Part 1 — Hadoop Distributed File System (HDFS)

### 1.1 What HDFS is designed for

**From the lecture — HDFS IS designed for:**
- Very large files
- Stream data access
- Commodity hardware

**From the lecture — HDFS is NOT designed for:**
- Low-latency data access
- Lots of small files
- Multiple writers, arbitrary file modifications

**Explanation:**
This "designed for / not designed for" framing is the single most testable idea about HDFS, so it's worth understanding *why* each trade-off exists:

- **Very large files, not lots of small files:** HDFS was built assuming files in the gigabyte-to-terabyte range (recall Lecture 1's "file sizes range from gigabytes to terabytes"). Each file's metadata (name, permissions, block locations) is held in memory on a single master node (the NameNode, see Section 1.4). Millions of *tiny* files would each consume metadata memory on that single master, without any corresponding benefit — so tiny files are inefficient for HDFS, whereas the same amount of data stored as fewer, larger files is efficient.
- **Stream data access, not low-latency access:** HDFS is optimized for reading a file from start to end in one large continuous pass (a "batch" read pattern), which favors high overall *throughput*. It is not optimized for quickly seeking to and reading a small random piece of a file, the way a traditional database or a local disk with low-latency random access would be.
- **Commodity hardware:** as in Lecture 1, HDFS assumes it is running on ordinary, relatively inexpensive, failure-prone hardware — so its design (block replication, described below) must tolerate frequent individual disk/node failures gracefully rather than assuming highly reliable hardware.
- **Multiple writers / arbitrary modifications are NOT supported:** this connects directly to the "write-once-read-many (WORM)" model mentioned in Lecture 1 — a file, once written, is treated as essentially immutable (aside from appends, in modern Hadoop versions). This greatly simplifies how HDFS keeps replicas consistent, at the cost of not behaving like a general-purpose read/write filesystem or database.

### 1.2 Key components of HDFS

**From the lecture:**

**NameNode:**
- HDFS **master node process**.
- Manages the **filesystem metadata**.
- **Does not store a file itself.**

**SecondaryNameNode and Standby NameNode:**
- **SecondaryNameNode** expedites the filesystem metadata recovery.
- **Standby NameNode** (optional) provides high availability.

**DataNode:**
- Runs the HDFS **slave node process**.
- Manages **block storage and access** for reading or writing data, and **block replication**.

**Explanation:** This is a direct, concrete instance of the master–slave pattern introduced generally in Lecture 1 (computer clusters) and echoed for Hadoop clusters specifically (Lecture 1, Section 4.6): the **NameNode is the single master**, coordinating and tracking everything but not doing any heavy storage work itself; **DataNodes are the many slave/worker nodes**, which actually hold and serve the real file data.

### 1.3 HDFS as a virtual filesystem, blocks, and replication

**From the lecture:**
- HDFS is a **virtual filesystem** — it appears to a client as one unified filesystem, but the data is actually stored across multiple different physical locations.
- HDFS is deployed **on top of native filesystems** (such as **ext3, ext4, xfs** in Linux) — i.e., HDFS doesn't replace the underlying OS filesystem on each machine; it's built as a layer above it.
- Each file in HDFS consists of **blocks**.
  - The default block size is **128 MB** (configurable).
  - The default number of replicas per block is **3** (configurable).

**Explanation:**
- **"Virtual filesystem":** from a user or application's point of view, you interact with HDFS as if it were one giant, seamless drive — you don't need to know or care which of the (possibly hundreds of) physical DataNode machines actually holds any given piece of your file. The NameNode's metadata is what makes this illusion possible: it silently keeps track of exactly which physical blocks, on which DataNodes, together make up your logical file.
- **Blocks and their size:** rather than storing a file as one giant contiguous chunk, HDFS splits every file into fixed-size blocks (128 MB by default — much larger than a typical local-filesystem block, which is usually a few KB, precisely because HDFS is optimized for very large files and streaming access, not small random reads). Each block is then distributed independently across the cluster, which is what enables *parallel* reading/writing and *parallel* MapReduce processing (recall "data locality" from Lecture 2 — each Map task can run right next to the specific block it needs).
- **Replication factor of 3 (default):** each block is stored on **three different DataNodes** (often across different physical racks) rather than just one. This is HDFS's core fault-tolerance mechanism: if one DataNode fails, the exact same block is still available from two other machines, and the NameNode can direct the system to create a fresh replica elsewhere to restore the replication factor back to 3. This is the concrete implementation, at the storage layer, of the general "automatic replacement of a failed node" idea from Lecture 1's discussion of computer clusters.

### 1.4 Logical view vs. physical implementation of data storage

**From the lecture:** The slides show a "Logical view of data storage" and a "Physical implementation of data file storage" as diagrams (visual content, not text).

**Explanation:** These two diagrams are illustrating exactly the "virtual filesystem" idea from Section 1.3, split into its two halves:
- The **logical view** is what the user/application sees: a single directory tree containing whole files, just like any normal filesystem (e.g., `/user/data/logs.txt`).
- The **physical implementation** is what actually exists on disk across the cluster: that same file broken into fixed-size blocks (e.g., Block 1, Block 2, Block 3…), with each block replicated 3 times and scattered across different DataNode machines — with the NameNode's metadata being the only thing that maps the logical file back to its true physical block locations.

### 1.5 NameNode metadata — detailed functions

**From the lecture:**
- The NameNode stores the **metadata** of the files in HDFS.
- **NameNode functions:**
  - Maintain the metadata pertaining to the file system (e.g., the **file hierarchy** and the **block locations for each file**).
  - **Manage user access** to the data files.
  - **Map the data blocks to the DataNodes** in the cluster.
  - **Perform file system operations** (e.g., opening and closing files and directories).
  - **Provide registration services and periodic heartbeats** for DataNodes.

**Explanation:**
Notice that the NameNode's job is entirely about **bookkeeping**, not about storing or moving actual file bytes (consistent with "does not store a file itself" from Section 1.2). It is essentially the "index" or "phone book" for the whole distributed filesystem: given a file path, it knows the block IDs that make it up, and given a block ID, it knows which DataNode(s) currently hold a replica of it. Because *everything* in HDFS depends on this metadata to find data at all, the NameNode is a uniquely critical single point that Hadoop takes special care to protect — which is exactly why the SecondaryNameNode and Standby NameNode exist (see Section 1.6).

### 1.6 DataNode and Secondary/Standby NameNode — detailed functions

**From the lecture — DataNode functions:**
- Provide **block storage** by storing blocks on the local file system.
- **Fulfil read/write requests.**
- **Replicate data** across the cluster.
- Keep in touch with the NameNode by sending periodic **block reports** and **heartbeats**.
  - A **heartbeat** confirms the DataNode is alive and healthy.
  - A **block report** shows the blocks currently being managed by that DataNode.

**From the lecture — Secondary NameNode and Standby NameNode functions:**
- Without a NameNode, there is **no way to know which files the blocks stored on DataNodes correspond to** — in essence, **all files in HDFS are effectively lost**.
- **Secondary NameNode:** periodically **backs up the metadata** in the (primary) NameNode, usually for recovery purposes.
- **Standby NameNode:** a "hot" node that runs together with the (primary) NameNode in the cluster, facilitating **high availability**.

**Explanation:**
- **Heartbeats and block reports** are how the NameNode keeps its metadata accurate and up to date in real time — if a DataNode's heartbeat stops arriving, the NameNode marks it as dead/unavailable and initiates re-replication of that DataNode's blocks elsewhere (this is the practical mechanism behind the fault-tolerant replication described in Section 1.3).
- This section explains *why the NameNode is so critical*: since only the NameNode knows how to reassemble scattered blocks back into files, losing the NameNode's metadata (with no backup) would make every file on the cluster effectively unreadable, even though the raw block data physically still exists on the DataNodes. This is why two different safety mechanisms exist:
  - **SecondaryNameNode** — despite its name, this is **not** a live backup/failover NameNode; it is a helper process that periodically merges/checkpoints the NameNode's metadata logs, which speeds up recovery *if* the NameNode needs to be restarted, but there is still some downtime involved.
  - **Standby NameNode** — this is the true high-availability solution: a second NameNode kept "hot" (continuously synchronized and ready) so that if the primary NameNode fails, the Standby can take over almost immediately with little to no downtime.
- A useful way to remember the naming: "Secondary" ≈ *periodic backup/checkpoint helper*; "Standby" ≈ *live failover replacement*. They solve related but distinct problems (faster recovery vs. near-zero downtime).

---

## Part 2 — Yet Another Resource Negotiator (YARN)

### 2.1 What is YARN, and why was it introduced?

**From the lecture:**
- YARN is the **core subsystem in Hadoop responsible for governing, allocating, and managing the finite distributed processing resources available on a Hadoop cluster**.
- YARN was **introduced in Hadoop 2** to improve the MapReduce implementation, but it is **general enough to support other distributed computing paradigms** (i.e., not only MapReduce).

**Explanation:**
Recall from Lecture 2 that "historically, Hadoop version 1 supported MapReduce only." In Hadoop 1, resource management and job scheduling were baked directly into the MapReduce system itself, which meant Hadoop clusters could *only* run MapReduce-style jobs. YARN's introduction in Hadoop 2 **separated resource management from the processing model** — YARN's job is purely to hand out cluster resources (CPU, memory) to whatever applications ask for them, while the actual computation logic (MapReduce, or later, other engines like Spark) runs as a YARN application. This is precisely why the Hadoop Ecosystem diagram from Lecture 1 shows tools like Spark able to run *on* the same Hadoop cluster alongside MapReduce — they can all share the same YARN-managed pool of cluster resources.

### 2.2 YARN's two long-running daemons

**From the lecture:**
YARN provides its core services via two types of long-running daemons:
- A **ResourceManager** (one per cluster) — manages the use of resources across the entire cluster.
- **NodeManagers**, running on all the nodes in the cluster — launch and monitor containers.

**Explanation:** This is, once again, the same master–slave pattern seen throughout this course: **ResourceManager = master** (one per cluster, global view), **NodeManager = slave/worker** (one per node, local view). It mirrors NameNode/DataNode almost exactly, except NameNode/DataNode manage *storage*, while ResourceManager/NodeManager manage *compute resources*.

### 2.3 Core YARN concepts: client, job, task, container

**From the lecture:**
- A **client** is the program that submits jobs to the cluster (it may also be the gateway/edge machine that the client program runs on — recall "edge servers" from Lecture 1).
- A **job**, also called an **application**, contains one or more **tasks**.
  - A task in a MapReduce job can be either a **mapper task** or a **reducer task**.
- Each mapper and reducer task runs **within a container**.
  - **Containers** are logical constructs representing a specific amount of memory and other resources (such as CPU cores).
  - Example: a container might represent **2 GB of memory and 2 processing cores**.
  - Containers may also refer to the **running environment** of an application.

**Explanation:** A **container** is YARN's fundamental unit of resource allocation — think of it as a "slice" of a machine's resources (a fixed amount of RAM + CPU) that YARN has promised to a particular task, and inside which that task's actual process runs, isolated from other containers on the same physical node. This is directly analogous to how HDFS breaks files into fixed-size **blocks** as its unit of storage — YARN breaks a node's compute capacity into **containers** as its unit of compute. Every single map task and reduce task from Lecture 2's MapReduce model ultimately executes inside one of these YARN containers.

### 2.4 ResourceManager — detailed functions

**From the lecture:**
- There is **one ResourceManager per cluster**, consisting of two key components: **Scheduler** and **ApplicationManager**.
- **Key functions of the ResourceManager:**
  - Creates the **first container** for an application, used to run that application's **ApplicationMaster**.
  - Tracks **heartbeats from NodeManagers** to manage them.
  - Runs the **Scheduler** to determine resource allocation among the applications on the cluster.
  - Manages **cluster-level security**.
  - Manages **resource requests from ApplicationMasters**.
  - **Monitors the status of ApplicationMasters** and restarts their container if it fails.
  - **Deallocates containers** when the application completes or after they expire.
- The role of the ResourceManager is **purely management and scheduling** — it **does not perform any actual data processing** (e.g., it never itself runs the Map and Reduce functions of a MapReduce application).

**Explanation:** The ResourceManager is intentionally kept "thin" and purely administrative — it decides *who gets what resources, when*, but it never touches actual application data or runs application code. This separation of concerns (deciding *what to run where* vs. *actually running it*) is what allows YARN to remain a general-purpose resource manager for many different kinds of distributed applications, not just MapReduce.

### 2.5 NodeManager — detailed functions

**From the lecture:**
- Each DataNode runs a **NodeManager** daemon to perform YARN functions (note: this is the practical reason HDFS worker nodes and YARN worker nodes are typically the very same physical machines — enabling the data-locality principle from Lecture 2).
- **Main functions of a NodeManager daemon:**
  - Communicates with the ResourceManager through **health heartbeats** and **container status notifications**.
  - **Registers and starts** the application processes.
  - **Launches** both the **ApplicationMaster** and the rest of an application's resource containers (i.e., the actual map and reduce tasks that run inside containers), on request from the ApplicationMaster.
  - **Oversees the lifecycle** of the application containers running on its node.
  - **Monitors, manages, and reports** on the resource consumption (CPU/memory) of the containers it hosts.
  - **Tracks the health** of the DataNode.
  - Provides **auxiliary services** to YARN applications, such as services used by the MapReduce framework for its **shuffle and sort** operations (recall the shuffle/sort step described in Lecture 2's WordCount example — this is where that step is physically implemented).

**Explanation:** The NodeManager is the local "supervisor" on each individual machine — it's the thing that actually starts and stops container processes on that node, watches their resource usage, and reports back to the central ResourceManager. It also quietly supports MapReduce's shuffle/sort mechanism, which is the piece of "magic" from Lecture 2 that automatically groups intermediate key-value pairs by key across the whole cluster — this section shows that this grouping is implemented as an auxiliary service running as part of the NodeManager infrastructure.

### 2.6 ApplicationMaster — detailed functions

**From the lecture:**
- For **each YARN application**, there is a **dedicated ApplicationMaster**.
- **Functions of the ApplicationMaster:**
  - Managing **task scheduling and execution**.
  - Allocating resources **locally** for the application's tasks.
- The ApplicationMaster runs **within a container**.
- Its existence is tied to the running application: when an application completes, its **ApplicationMaster no longer exists**.
- Once created, the ApplicationMaster is in charge of **requesting resources with the ResourceManager** to run the application.
- Resource requests are **very specific**, for example:
  - The **file blocks** needed to process the job,
  - The **amount of resources** needed (in terms of the number of containers to create for the application),
  - The **size of the containers**, etc.

**Explanation:** The ApplicationMaster is essentially a **per-application manager**, in contrast to the ResourceManager, which is the single **per-cluster** manager. Think of the relationship this way:
- **ResourceManager** = the cluster-wide "landlord" who owns and allocates resources (containers) among many tenants (applications).
- **ApplicationMaster** = each tenant's own "project manager," dedicated to exactly one running application, who negotiates with the landlord for the specific resources that particular application needs, and then locally coordinates how those resources are actually used (e.g., deciding which map/reduce tasks run in which containers).

For a MapReduce job specifically: the ApplicationMaster is the process that requests containers to run the actual map tasks and reduce tasks, tracks their progress, and requests replacement containers if any task fails — this is the concrete mechanism that fulfills the "fault tolerance" design goal from Lecture 2's discussion of the 2004 Google MapReduce paper.

### 2.7 Putting it all together — the full lifecycle of a job in YARN

**Explanation (synthesis, connecting all the pieces above into one flow — not verbatim from the slides, but assembled directly from the functions described in Sections 2.3–2.6):**

1. A **client** (possibly from an edge server) submits a **job/application** to the cluster.
2. The **ResourceManager** creates the **first container** for this application and uses it to launch the application's dedicated **ApplicationMaster**.
3. The **ApplicationMaster** requests the specific resources it needs from the ResourceManager (e.g., "I need N containers, each with 2GB RAM and 2 CPU cores, ideally located near these specific HDFS blocks").
4. The ResourceManager's **Scheduler** grants containers on various nodes, taking data locality into account where possible.
5. On each of those nodes, the local **NodeManager** actually launches the requested containers and starts the map or reduce **tasks** inside them.
6. NodeManagers continuously send **heartbeats and container status** back to the ResourceManager; the ApplicationMaster tracks task progress and requests replacement containers if any task fails.
7. Map tasks read their input (ideally from a local HDFS block, thanks to data locality), and produce intermediate key-value output; the shuffle/sort auxiliary service (hosted by NodeManagers) groups this output by key and delivers it to the appropriate reduce tasks.
8. Once all tasks finish, the job's final output is written back to HDFS, and the **ApplicationMaster** (and its container) are torn down — "when an application is completed, its ApplicationMaster no longer exists."

This end-to-end flow is the concrete realization of everything discussed across all three lectures: Lecture 1's clusters and master-slave design, Lecture 2's Map/Reduce programming model and data locality principle, and this lecture's HDFS storage + YARN resource management machinery.

---

## Part 3 — Summary

**From the lecture:**
- **Hadoop is a leading platform for big data.**
- Hadoop consists of:
  - A **storage layer** (**HDFS**),
  - A **coordination and management layer** (**YARN**), and
  - A **processing layer** (e.g., **MapReduce**).
- **HDFS and YARN have key services (daemons).**
- **MapReduce is a fundamental computing model** (i.e., batch processing) for big data.
- **Next:** Interaction with Hadoop and a deeper "dive" into the MapReduce framework (i.e., the following week's topics: HDFS Interfaces and the MapReduce Data Processing Model).

**Explanation — the "three-layer" mental model to remember for the whole subject:**

| Layer | Component | Master daemon | Worker daemon | Analogy |
|---|---|---|---|---|
| Storage | **HDFS** | NameNode | DataNode | The cluster's "hard drive" |
| Coordination/resource management | **YARN** | ResourceManager (+ per-app ApplicationMaster) | NodeManager | The cluster's "operating system scheduler" |
| Processing model | **MapReduce** (runs as a YARN application) | — | Map tasks / Reduce tasks (run inside containers) | The actual "program logic" |

This table is a good one-glance summary to revise from: for the exam/assessment, you should be able to state, for any given function (e.g., "tracks block reports," "creates the first container," "manages shuffle and sort," "backs up metadata"), which exact daemon is responsible for it.

---

## Part 4 — References (as given in the lecture)

- White, T. *Hadoop: The Definitive Guide — Storage and Analysis at Internet Scale*, O'Reilly, 2015. (Available through UOW library)
- Vohra, D. *Practical Hadoop Ecosystem: A Definitive Guide to Hadoop-Related Frameworks and Tools*, Apress, 2016. (Available through UOW library)
- Aven, J. *Hadoop in 24 Hours, SAMS Teach Yourself*, SAMS, 2017.
- Alapati, S. R. *Expert Hadoop Administration: Managing, Tuning, and Securing Spark, YARN and HDFS*, Addison-Wesley, 2017.
- Apache Hadoop, HDFS Interface (official documentation)
- Apache Hadoop, YARN (official documentation)

---

## Part 5 — Self-Check Questions (for revision)

**HDFS:**
1. What three things is HDFS designed for, and what three things is it explicitly *not* designed for?
2. What does the NameNode do, and — critically — what does it *not* do?
3. What is the difference between the SecondaryNameNode and the Standby NameNode?
4. What is the default HDFS block size, and the default replication factor? Why are both configurable?
5. Why is HDFS described as a "virtual filesystem"?
6. What is a heartbeat, and what is a block report? Which daemon sends them, and to whom?
7. Why would losing the NameNode's metadata (with no backup) make all files in HDFS effectively lost, even though the block data still physically exists?

**YARN:**
8. What problem did YARN solve that existed in Hadoop 1 (MapReduce-only)?
9. Name YARN's two long-running daemons and state which is the master and which is the worker.
10. What is a "container" in YARN, and give the example figures used in the lecture (memory + CPU cores).
11. List at least four functions of the ResourceManager.
12. Why does the lecture emphasize that the ResourceManager does *not* perform any actual data processing?
13. List at least four functions of the NodeManager, including its role in the MapReduce shuffle/sort step.
14. What is the relationship between the ResourceManager and an ApplicationMaster? Use the "landlord vs. project manager" analogy to explain it in your own words.
15. Why does the ApplicationMaster "no longer exist" once its application completes?
16. Walk through, step by step, what happens from the moment a client submits a MapReduce job to the moment its final output is written back to HDFS.

**Big picture:**
17. Fill in the three-layer table from Part 3 from memory: layer name, component, master daemon, worker daemon.
18. Explain how "data locality" (from Lecture 2) is only possible because HDFS DataNodes and YARN NodeManagers typically run on the very same physical machines.
