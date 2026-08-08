# Lecture 3 — Business Process Modelling and Management (BPMN)

---

## 0. Where This Fits
Lecture 2 taught you how to describe a **single service**. But services rarely act alone — they're invoked as steps inside a larger sequence of business activities. Lecture 3 teaches you how to model that larger sequence: the **business process** itself, using the industry-standard notation **BPMN (Business Process Modeling Notation)**. Think of it this way: Lecture 2 = describing *one LEGO brick*; Lecture 3 = the *instruction diagram* showing how many bricks fit together over time, who places each one, and in what order.

---

## 1. Business Processes: Foundations

**Definition:** A **business process** consists of a **set of activities**, performed by their **relevant roles or collaborators**, to **intentionally achieve a set of common business goals**.

- Business processes are **core assets** of any enterprise, spanning many industry aspects: design, engineering, manufacturing, purchasing, physical distribution, production management, and supply chain management.
- **Examples:** the production line of a car manufacturer, the enrolment process at a university, an insurance claim handling process.

> 💡 Notice the deliberate similarity to the definition of a *service* from Lecture 1 (a unit of functionality achieving a goal) — the key difference is that a **process** is explicitly about the *ordered flow of multiple activities and actors over time*, while a *service* is a single callable unit. A process typically *orchestrates* multiple services (and human tasks) as its individual activities.

---

## 2. Why Process Modelling Matters

### 2.1 The Questions That Arise
When trying to describe a process, several natural questions come up:
- Which steps are *really* necessary?
- *Who* should perform them?
- Should they be kept **in-house** or **outsourced**?
- *How* should they be done?
- What **capabilities** are needed to do them?
- What **results** do we expect, and **how will they be monitored**?

➡ These questions all point to the same conclusion: we need a **commonly agreed, explicit description** of the business process in question. Without a shared model, different stakeholders (analysts, developers, managers) will each carry a different mental picture of "how the process works," leading to miscommunication and errors.

### 2.2 The Value of Business Process Models
Business process models are **essential knowledge assets** that let an organization manage its processes by:
1. **Documenting and implementing** procedures.
2. **Controlling** their execution (making sure the process actually runs as intended).
3. **Analyzing** their performance (are they efficient? where are the bottlenecks?).
4. **Improving** them — the model becomes the *basis for process improvement, understanding, communication, and execution.*

### 2.3 Scale in Practice
Organizations committed to long-term Business Process Management (BPM) can accumulate **hundreds or thousands** of process models:
| Organization | Process Model Repository Size |
|---|---|
| IBM BIT Process Library | 735 process models |
| SAP Reference Model | 604 process models |
| Suncorp (insurance) | 6,000+ process models |

> 💡 **Why this matters:** at this scale, informal descriptions (a paragraph of English, a rough flowchart drawn by one person) simply don't scale. You need a **standardized, unambiguous notation** so that thousands of models, created by different people over many years, remain consistent and interpretable by anyone in the organization — this is precisely the problem BPMN was designed to solve.

---

## 3. Characteristics of Business Processes & Choice of Modelling Language

Business processes typically involve:
- **Multiple actors** (people, business units, systems, etc.)
- **Concurrent activities** (things happening at the same time, not just one after another)
- **Explicit synchronization points** — e.g., a task cannot start until several other concurrent tasks are complete (this foreshadows the "Gateway" concept below).
- An **end-to-end flow** of activities from trigger to completion.

Because of this complexity, a dedicated **modelling language** is needed. Options include:
- **BPMN (Business Process Modeling Notation)** — the new/emerging standard at the time, and the focus of this lecture.
- **UML Activity Diagrams** — a more general-purpose UML diagram type, sometimes used for process flows.
- **Petri Nets** — a mathematically rigorous formalism for modelling concurrent/distributed systems, often used as a *theoretical foundation* for verifying process models (e.g., checking for deadlocks).

---

## 4. Introduction to BPMN

### 4.1 Purpose of BPMN
Quoting the BPMN 2.0 specification's stated intent (paraphrased): BPMN's primary goal is to provide a notation that is **readily understandable by everyone involved** — from the **business analysts** who draft the initial process, to the **technical developers** who implement the systems that execute it, to the **business people** who manage and monitor it once running.

In short: **BPMN is designed as a standardized bridge between business process *design* and process *implementation*.** It's meant to be the *one diagram* that a non-technical manager and a software engineer can both read and agree upon.

### 4.2 The Four Basic Categories of BPMN Elements
BPMN organizes all of its notation into four categories:
1. **Flow Objects** — the "verbs and nouns" of the process: Activities, Events, and Gateways (the main building blocks describing *what happens*).
2. **Connecting Objects** — the "glue" that links Flow Objects together and shows the order/communication between them (Sequence Flow, Message Flow, Association).
3. **Swimlanes** — the visual mechanism for organizing *who* does *what* (Pools and Lanes).
4. **Artifacts** — supplementary information that adds context without changing the flow logic itself (Data Objects, Text Annotations, Groups).

The rest of this lecture works through each category in detail.

---

## 5. Flow Objects — Part A: Activities

**Definition:** An **activity** is work performed within a business process.
- It can **take time** to perform and typically involves **one or more resources**.
- It can be **atomic** (a **Task**) or **compound** (a **Sub-Process**).
- It can be performed **once**, or can have **internally defined loops**.

### 5.1 Tasks
A **Task** is an **atomic** activity within a process — used when the work is **not broken down further** into finer detail. It's the "leaf node" of process decomposition — you don't zoom into a Task any further.

### 5.2 Sub-Process
A **Sub-Process** is a **compound** activity — it *can* be broken down into a finer level of detail (an entire sub-process, itself made of further activities/events/gateways).
- Sub-Processes enable **hierarchical process development**: you can model a high-level process with a small number of big steps, then "expand" any one step into its own detailed diagram.
- A **collapsed** sub-process is shown as a single box (often with a small "+" marker); an **expanded** sub-process shows its internal flow directly nested inside the box.
- **Example (from the lecture):** an "Assess Claim" Sub-Process, shown expanded, reveals the detailed sequence of activities used to actually assess an insurance claim.

> 💡 **Why this matters:** hierarchical decomposition lets you keep a top-level diagram readable (e.g., 5–7 big steps) while still being able to "drill down" into arbitrary detail for any step that needs it — exactly like decomposing a large function into sub-functions in programming.

### 5.3 Multi-Instance Activities
Sometimes an activity needs to be performed **many times, each with a different data set.**

- **Example:** When a major corporation checks the financial results of *all* its subsidiaries, it must repeat the same "check financial results" activity once per subsidiary, each time using that subsidiary's own data.
- BPMN supports this with a **Multi-Instance Activity** (sometimes called a **"For Each"** construct).
- Multi-instance activities can run in two modes:
  - **Parallel** — all instances run simultaneously (independent of each other).
  - **Sequential** — instances run one after another, in order.

---

## 6. Flow Objects — Part B: Events

**Definition:** An **Event** is something that **"happens"** during the course of a business process.
- An Event may **affect the flow** of the process, and usually has a **trigger** (what causes it) or a **result** (what it produces).
- Events can **start, delay, interrupt, or end** the flow of the process.

BPMN distinguishes three positions where events can occur: **Start**, **Intermediate**, and **End**.

### 6.1 Start Events
A **Start Event** shows **where a process begins**.
- Different types of Start Event indicate different situations that can *trigger* the start of the process.
- A Start Event can **only have outgoing** Sequence Flows (nothing flows *into* a start event — it's the origin).
- **Trigger-based Start Events can only exist in top-level processes** — they are **not used inside Sub-Processes** (a sub-process is triggered by the flow arriving from its parent, not by an external trigger of its own).

**Common Start Event trigger types (as covered in the lecture):**
| Trigger type | Meaning |
|---|---|
| **Message** | Triggered by a direct communication from another business participant. The sender and receiver must be in **separate Pools** — a message cannot be sent from one Lane to another Lane *within the same Pool*. |
| **Timer** | Triggered by a specific date/time (e.g., "January 1, 2026 at 8am") **or** a recurring time (e.g., "every Monday at 8am"). |
| **Signal** | Triggered by a **broadcast** signal that has **no specific target or recipient** — *all* processes/participants can potentially "see" the signal, and it is up to each one individually to decide whether to react to it. |
| **Conditional** | Triggered when a defined **condition on data** becomes true. Important rule: the condition must become **false, then true again**, before the event can be triggered a *second* time (it can't keep re-firing while the condition simply stays true). |

### 6.2 Intermediate Events
An **Intermediate Event** indicates that something happens/occurs **after the process has started and before it has ended**.
- They may also **interrupt** the normal flow of an in-progress Activity (e.g., attached to the boundary of a Task to represent "if X happens while this task is running, break out and handle it").
- Every Intermediate Event type can either **throw** or **catch** the event:
  - **Catching** Intermediate Event: the process **waits** for something to happen (i.e., it pauses until the trigger's circumstance occurs).
  - **Throwing** Intermediate Event: the process **immediately fires** the event (actively creating the circumstance defined by the trigger, e.g., actively sending a message).
- **Rule:** A **Throwing** Intermediate Event **cannot be attached to the boundary of an Activity** (boundary attachment is specifically an *interrupting/catching* pattern — you "catch" something that interrupts a running task; you don't "throw" from a task's boundary).

### 6.3 End Events
Different types of **End Event** indicate different categories of **result** for the process.
- A **result** is something that occurs at the end of a particular path of the process (e.g., a message sent, a signal broadcast).
- **All End Events are "throw" results** (an end event actively produces its result as the process path concludes — it never "waits").
- **Only incoming** Sequence Flow is permitted at an End Event — Sequence Flow **cannot leave** an End Event (symmetric to Start Events, which only have outgoing flow).
- A **None End Event** (no specific result type) is **always used to mark the end of a Sub-Process** — i.e., when control moves back up one hierarchical level to the parent process.

> 💡 **Summary rule of thumb:** Start = outgoing only; End = incoming only; Intermediate = both incoming and outgoing (it sits *within* the flow). Start/End events describe *when the whole process begins/ends*; Intermediate events describe things that happen *along the way*.

---

## 7. Flow Objects — Part C: Gateways

**Definition:** **Gateways** control **how the process diverges or converges** — i.e., they **split** and **merge** the flow of a process.
- There are several different **types** of Gateway, each with different splitting/merging semantics.
- **Important rule:** the type of a single Gateway (for splitting vs. merging) must **match** — e.g., a Gateway **cannot** be Parallel on the input side and Exclusive on the output side. A given Gateway symbol behaves consistently, whichever direction the flow is going through it.

### 7.1 Exclusive Gateway (XOR)
**Splitting behaviour:**
- Splits the flow when it has **2 or more outgoing paths**.
- Each outgoing path has an associated **condition**.
- **Exactly one** of those conditions must evaluate to true — the process takes **only one** of the alternative paths (mutually exclusive choice — hence "Exclusive").
- **Default Condition:** to guarantee the process never "gets stuck" if none of the explicit conditions evaluate to true, the modeller can designate one outgoing flow as the **Default**. The Default path is taken automatically **if all other conditions turn out false** — it acts as a safety-net "else" branch.

**Merging behaviour:**
- When multiple paths converge back at an Exclusive Gateway, it simply lets **whichever single path arrives** pass straight through — there's no waiting or synchronization, since by definition only one of the alternative paths would ever have been taken in the first place.

### 7.2 Event-Based Exclusive Gateway
- A variant of the Exclusive Gateway where the branching decision is based on **which of two or more Events occurs** — **not** on data-oriented conditions (unlike the ordinary Exclusive Gateway above).
- **Example use case:** "wait for either a payment-received message OR a 24-hour timer to elapse, whichever happens first" — the branch taken depends on *which event happens first*, not on evaluating a data condition.

### 7.3 Parallel Gateway (AND)
**Splitting behaviour:**
- **No conditions are evaluated** at all.
- The Parallel Gateway simply **creates parallel paths** — *all* outgoing paths are activated simultaneously (an "AND-split").

**Merging behaviour (synchronization):**
- The Parallel Gateway **waits for a token to arrive on every single incoming Sequence Flow** before proceeding.
- When the *first* token arrives, there's no condition evaluation — the token is simply **"held"** at the Gateway and does **not** continue onward yet.
- Only once **all** expected tokens have arrived are they **merged**, and a **single token** then proceeds down the outgoing Sequence Flow.
- This is the classic **"AND-join" / synchronization barrier"** pattern — e.g., "don't proceed to shipping until *both* payment confirmation *and* inventory-reservation are complete."

### 7.4 Inclusive Gateway (OR)
**Splitting behaviour:**
- Creates **alternative paths** based on conditions attached to each path (similar to Exclusive), **but**:
- **One or more** paths can be activated (not necessarily just one).
- **Every** condition that evaluates to true results in a token going down that path.
- **At least one** of the conditions must evaluate to true (there must always be a valid way forward).

**Merging behaviour (partial synchronization):**
- This is more sophisticated than the Parallel Gateway's merge: when the *first* token arrives, the Inclusive Gateway **looks upstream** along each of its other incoming Sequence Flows to determine **whether a token might still arrive later** on that path (based on which paths were actually activated at the corresponding upstream split).
- The Gateway then **waits only for the tokens it actually expects** (not necessarily *all* possible incoming flows — only those that were genuinely activated upstream).
- Once all the **expected** tokens have arrived, the flow is **synchronized** (merged) and proceeds.

### 7.5 Comparison Table: The Four Gateway Types
| Gateway | Splitting behaviour | Merging behaviour | Real-world analogy |
|---|---|---|---|
| **Exclusive (XOR)** | Exactly 1 of N paths taken, based on data condition (+ optional default) | Simple pass-through, no waiting | "Choose exactly one" — e.g., pay by card **or** pay by cash |
| **Event-based Exclusive** | Exactly 1 of N paths taken, based on which **event** occurs first | Simple pass-through | "Whichever happens first" — e.g., payment received **or** timeout |
| **Parallel (AND)** | All N paths taken simultaneously, no conditions | Waits for **all** N tokens (full synchronization) | "Do everything at once, then regroup" |
| **Inclusive (OR)** | 1-to-N paths taken, based on conditions (at least 1 must be true) | Waits only for the **expected/activated** tokens (partial synchronization) | "Do whichever apply, then regroup on those" |

---

## 8. Connecting Objects

Connecting Objects link Flow Objects together to actually define the process graph:
| Connecting Object | Connects | Notes |
|---|---|---|
| **Sequence Flow** | Two Flow Objects **within the same Pool** | Shows the **order** in which activities are performed. Sequence Flow **can cross Lane boundaries** (within one Pool), but **cannot cross a Pool boundary** — i.e., a single process is always fully contained within one Pool. |
| **Message Flow** | Two objects in **different Pools** | Shows communication **between separate participants**. Message Flow can **never** be used to connect two objects inside the *same* Pool, and is never used *within or across Lanes* of a single Pool (Lanes are for internal partitioning, not external communication). |
| **Association** | A Flow Object to an **Artifact** (e.g., a Text Annotation or Data Object) | Shows non-flow relationships, e.g., linking a note to the activity it comments on, or linking a Data Object as input/output of an Activity. |

---

## 9. Swimlanes

BPMN uses **"swimlanes"** to visually partition and organize the objects in a diagram. There are two main types:

### 9.1 Pools
- Act as **containers for a Process**.
- Each Pool represents **one participant** in a collaborative Business Process Diagram (e.g., "Customer", "Restaurant", "Delivery Platform").
- Sequence Flow is fully contained *within* a single Pool; communication *between* Pools happens only via Message Flow.
- A Pool can be shown as a **"black box"** (its internal process hidden — Message Flow then connects to the Pool's boundary) or with its full internal process visible.

### 9.2 Lanes
- Often assumed to represent **internal business roles** within a process (e.g., Manager, Administration, Associate).
- More generally, Lanes provide a **generic mechanism for partitioning** objects **within a Pool** based on *any* characteristic of the process or its elements (e.g., organizational department, underlying technology, or even product line — not strictly "roles").
- **Sequence Flow can cross Lane boundaries** (unlike Pool boundaries).
- **Message Flow is not used within or across Lanes** of a single Pool.
- **Lanes can be nested** (a Lane can itself contain sub-Lanes).

> 💡 **Pool vs. Lane, in one sentence:** a **Pool** = a separate participant/organization (crossing it = external communication, Message Flow); a **Lane** = an internal subdivision *within* one participant (crossing it = still internal, Sequence Flow).

---

## 10. Artifacts

Artifacts add supplementary information to a diagram **without changing its control-flow logic**.

### 10.1 Data Objects
- Represent **data and documents** used in the process.
- Usually define the **inputs and outputs of Activities**.
- Data Objects can have **"states"** — depicting how the object's status changes as it moves through the process (e.g., an "Invoice" Data Object might move through states: Draft → Submitted → Approved).

### 10.2 Data Flow
- Represents the **movement of Data Objects** into and out of Activities.
- **Important:** In BPMN, **data flow is decoupled from Sequence Flow** — the two are shown separately. Sequence Flow tells you the *order* of activities; Data Flow tells you *what data* moves between them. They're not the same arrows.

### 10.3 Text Annotations
- Provide the ability to add further **descriptive information or notes** about a process and its elements.
- Text Annotations can either **connect to a specific object** (via an Association) or **float freely** anywhere on the diagram.

---

## 11. Orchestration vs. Choreography

These two terms describe two different "viewpoints" on describing multi-participant behaviour — a distinction that matters a lot once you get into Lecture 5's territory (service composition/interoperation):

| Concept | Definition | Represented as |
|---|---|---|
| **Orchestration** | Describes how a **single** business entity (a process participant — e.g., a buyer, shipper, seller, or supplier) **does things** — i.e., its own internal step-by-step process. | Each orchestration lives inside **its own Pool**. Each Pool represents exactly **one** participant. |
| **Choreography** | Depicts the **interactions between two or more** business entities (each modelled as a Pool). | Shown via the **Message Flow** connecting the Pools. In BPMN 2.0, Choreography can also be shown as its own dedicated flow-chart-style diagram that sequences the interactions between participants (rather than showing each participant's internal steps). |

> 💡 **Orchestration** = "what happens *inside* one participant" (a single Pool's internal Sequence Flow). **Choreography** = "what gets exchanged *between* participants" (the Message Flow pattern across Pools). A full collaborative process diagram typically shows *both* at once: each Pool's own orchestration, plus the Message Flows choreographing them together.

---

## 12. Worked Exercises

### 12.1 Exercise 1 (Pen and Paper): "Describe the behaviour of this process"
This exercise (slide 34, following the Parallel Gateway content) refers to a **diagram image** that was not captured in this text-based export of the slides. To answer it properly, you'll need to look at the actual diagram in the original slide deck. As general guidance for *any* such gateway-behaviour question, walk through it systematically:
1. Identify every Gateway in the diagram and its **type** (Exclusive, Event-based, Parallel, or Inclusive).
2. For each **split**, determine: how many paths can be activated, and under what condition(s)?
3. For each **merge**, determine: is it a simple pass-through, a full synchronization (wait for all), or a partial synchronization (wait only for expected tokens)?
4. Trace a token's journey through the whole diagram, describing in plain English what has to happen for the process to reach its End Event(s).

### 12.2 Exercise 2 (Pen and Paper): Online Food Delivery Process

**Scenario (as given):** A customer uses an online food delivery platform to order food from a restaurant. After browsing the menu, the customer submits an order, received by the restaurant. The restaurant checks whether all requested items are available. If any item is unavailable, the restaurant rejects the order, notifies the customer, and the process ends. Otherwise, the restaurant accepts the order and begins preparing the food. At the same time, the delivery platform assigns a delivery driver — if no driver is immediately available, the platform keeps searching until one accepts. Once the food is ready **and** a driver has been assigned, the driver collects the order and delivers it to the customer. The customer confirms receipt, after which the platform records the completed order and sends an electronic receipt.

**Worked BPMN design (textual description):**

**Pools (participants):** Customer | Restaurant | Delivery Platform | Driver

| Step | Pool | Element type | Description |
|---|---|---|---|
| 1 | Customer | Start Event (None) | Customer browses menu and submits an order |
| 2 | Customer → Restaurant | Message Flow | Order details sent to the Restaurant |
| 3 | Restaurant | Task | "Check item availability" |
| 4 | Restaurant | **Exclusive Gateway** (split) | Condition: "All items available?" |
| 5a | Restaurant | Task *(No branch)* | "Reject order" |
| 5b | Restaurant → Customer | Message Flow | "Notify customer of rejection" |
| 5c | Restaurant | **End Event** | Process ends (rejected path) |
| 6a | Restaurant | Task *(Yes branch)* | "Accept order & prepare food" |
| 6b | Restaurant → Delivery Platform | Message Flow | Order acceptance triggers driver search |
| 6c | Delivery Platform | **Sub-Process / looping Task** | "Search for available driver" — loops (using a repeat/loop marker) until a driver accepts; this can be modelled as a Task with a standard loop marker, or as an **Event-based Exclusive Gateway** repeatedly checking "driver accepted?" vs. "no driver yet, retry" |
| 7 | Restaurant + Delivery Platform | **Parallel Gateway (split, then join)** | Food preparation (Restaurant) and driver assignment (Delivery Platform) happen **concurrently**; a Parallel Gateway join waits for **both** "food ready" **and** "driver assigned" tokens before proceeding — this is the explicit synchronization point mentioned in Section 3 |
| 8 | Driver | Task | "Collect order from restaurant" |
| 9 | Driver → Customer | Task / Message Flow | "Deliver order to customer" |
| 10 | Customer → Driver/Platform | Message Flow | "Confirm receipt of order" |
| 11 | Delivery Platform | Task | "Record completed order" |
| 12 | Delivery Platform → Customer | Message Flow | "Send electronic receipt" |
| 13 | Delivery Platform | **End Event** | Process ends (successful path) |

**Key modelling decisions to notice (and be ready to justify in class/exam):**
- The **rejection path** and the **success path** both terminate at their own **End Event** — a process can have multiple End Events representing different outcomes.
- The **Exclusive Gateway** at step 4 is the correct choice (not Inclusive) because the two outcomes ("reject" vs. "accept") are strictly mutually exclusive — only one path is ever taken.
- The **concurrent** food-preparation and driver-search activities (step 7) are the textbook use-case for a **Parallel Gateway split → join**, since the scenario explicitly says these happen "at the same time" and the driver must **wait** until both conditions ("food ready" and "driver assigned") are satisfied before collection can begin — exactly the "explicit synchronization point" behaviour described in Section 3.
- Communication between **separate Pools** (Customer ↔ Restaurant ↔ Delivery Platform ↔ Driver) must always be shown as **Message Flow**, never Sequence Flow, since each is a distinct participant.
- The driver-search "loop until accepted" behaviour is a good candidate for either a **looping Task** or an **Event-based Gateway** that keeps cycling back until the "driver accepted" event occurs — both are valid BPMN patterns for "retry until success."

> 📝 **Optional simplified visual (flowchart-style, not strict BPMN):**
> ```mermaid
> flowchart TD
>     A([Customer submits order]) --> B[Restaurant: Check availability]
>     B --> C{All items available?}
>     C -- No --> D[Reject order] --> E[Notify customer] --> F([End: Rejected])
>     C -- Yes --> G[Accept order & prepare food]
>     C -- Yes --> H[Assign delivery driver]
>     H -.retry until accepted.-> H
>     G --> I{{Parallel Join: food ready AND driver assigned}}
>     H --> I
>     I --> J[Driver collects order]
>     J --> K[Driver delivers to customer]
>     K --> L[Customer confirms receipt]
>     L --> M[Platform records order & sends e-receipt]
>     M --> N([End: Completed])
> ```
> *(This Mermaid flowchart is a simplified visual aid for your own review — it uses generic flowchart shapes, not the official BPMN icon set. For the actual assessment, redraw it using proper BPMN notation: Pools/Lanes, Start/End Event circles, Task rectangles, and Gateway diamonds.)*

---

## 13. Key Takeaways / Review Checklist

- [ ] I can define a business process and explain why explicit process models matter (documentation, control, analysis, improvement).
- [ ] I can name the four BPMN element categories: Flow Objects, Connecting Objects, Swimlanes, Artifacts.
- [ ] I can distinguish a **Task** (atomic) from a **Sub-Process** (compound), and explain **Multi-Instance** activities (parallel vs. sequential).
- [ ] I can explain the rules for **Start Events** (outgoing only, trigger types: message/timer/signal/conditional, top-level-only for triggered starts).
- [ ] I can explain **Intermediate Events** (catching vs. throwing; throwing cannot attach to an activity boundary).
- [ ] I can explain **End Events** (incoming only, always "throw", None End Event for sub-processes).
- [ ] I can explain and compare all four Gateway types: **Exclusive, Event-based Exclusive, Parallel, Inclusive** — both their splitting AND merging behaviour.
- [ ] I can distinguish **Sequence Flow** (within a Pool) vs. **Message Flow** (between Pools).
- [ ] I can distinguish **Pools** (participants) vs. **Lanes** (internal roles/partitions within a Pool), and know which flow type crosses which boundary.
- [ ] I can explain **Data Objects**, **Data Flow** (decoupled from Sequence Flow), and **Text Annotations**.
- [ ] I can distinguish **Orchestration** (single participant's internal process) vs. **Choreography** (interactions between participants).
- [ ] I can design a complete BPMN diagram from a written scenario (see the food-delivery worked example) — including correctly choosing Gateway types and identifying synchronization points.

---

## References
- Stephen A. White and Derek Miers, *BPMN Modeling and Reference Guide*, 2008.
- BPMN specification: http://www.bpmn.org
