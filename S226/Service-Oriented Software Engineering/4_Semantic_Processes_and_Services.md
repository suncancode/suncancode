# Lecture 4 — Semantic Processes and Services

---

## 1. Motivation: The Problem with BPMN

BPMN is the industry standard for modeling business processes, but it only captures **coordination semantics** — i.e., the control-flow relationships between tasks (e.g., "Task A must precede Task B").

**What BPMN does NOT capture:** the **effects** of tasks — what actually happens/changes when a task executes. Given a BPMN diagram, you cannot determine, at any point in the process, what has been achieved:

- **Functional effects** — what has been done (business-level outcomes)
- **Non-functional effects** — performance / Quality-of-Service (QoS) factors

A task's name (e.g., "Assess Package") is just a human-readable label — it carries no machine-interpretable semantic meaning about state changes.

> **Semantic annotation exists to fill this gap**, by attaching formal effect descriptions to BPMN tasks.

---

## 2. Benefits of Effect Annotation

### 2.1 Compliance Checking

Determining whether a process complies with regulatory/legislative requirements.

**Example:** *"Admit critically injured patients into consultation in no greater than 15 minutes after triage."*

This single requirement actually bundles two different kinds of constraints:

| Type | Example | Nature |
|---|---|---|
| **Functional effect** | Patient admission | A state that must be achieved |
| **Non-functional objective** | ≤ 15 minutes | A performance/QoS constraint on *how fast* |

With effect annotations, you can automatically check whether/where an effect (e.g., "patient admitted") is achieved in the model, and open the follow-up question: *how do you modify a non-compliant process model to make it compliant?*

### 2.2 Establishing Inter-Process Relationships

- **Change impact analysis** — a change to one process can ripple out to affect related processes.
- Real-world scale: Suncorp's insurance process repository has **6,000+ process models** — manually tracking effect dependencies across that scale is infeasible without formal tooling.

---

## 3. Functional Effects — the Design-Time Problem

Given any point in a process model, we want to determine (at **design-time**) what effects would hold if the process executed up to that point.

**The answer is non-deterministic**, represented as a **set of effect scenarios**, because:

1. Later process steps may "undo" (contradict) the effects of earlier steps — resolving these inconsistencies differently yields different scenarios.
2. Processes may take alternative paths (via gateways) to reach the same point.

---

## 4. Effect Annotations

- Analysts annotate each BPMN task with **immediate effect annotations**.
- These immediate effects are accumulated (usually automated) into **cumulative annotations**, describing functional effects (and non-functional properties) up to that point.

**Annotation styles:**
- Informal (plain English)
- Formal (FOL, LTL, CTL, etc.)
- Controlled Natural Language (CNL) — a restricted, structured subset of natural language that maps directly to formal assertions.

---

## 5. Methodology for Effect Annotation

1. **Identify objects of interest** (usually business objects) in the domain — look at nouns central to task names and the business flow.
2. **For each task, identify which objects are impacted.**
3. **Describe the impact** — usually a change of state for a business object.
   - *Example:* "Borrow a book" impacts the `Book` object (Available → On Loan) and the `Borrower Loan Record` (book added to record).
4. **Pay special attention to inter-object relationships** impacted by a task.
   - *Example:* "Enrolling in a subject" creates a relationship between `Student[423432]` and `Subject[CSCI927]`.

### 5.1 States vs. Relationships — the key distinction

| | State | Relationship |
|---|---|---|
| **Arity** | Unary predicate — `P(x)` | n-ary predicate (n ≥ 2) — `P(x, y, ...)` |
| **Describes** | A property of **one** object | A link **between two or more** objects |
| **Example** | `rejected(c)`, `approved(c)` | `investigated(c, o)`, `payout(c, t)` |

**Heuristic:** if describing the effect naturally requires the word "with" ("claim investigated *with* an outcome"), it's almost always a relationship, not a state.

Both states and relationships are simply **effects** (logical clauses) — the state/relationship distinction is about the *arity of the predicate*, not a different kind of thing.

### 5.2 Worked Example — Claim Department Process

Process: `Investigate Claim → XOR-split(valid/not_valid) → {Reject Claim | Determine Payout} → XOR-merge → Write Assessment Report`

**Objects of interest:** Claim `c`, Outcome `o`, Amount `t`

**States:** `rejected(c)`, `approved(c)`

**Relationships:** `investigated(c, o)`, `assessed(c, r)`, `payout(c, t)`

**Immediate effects per activity:**

| Activity | Immediate effect |
|---|---|
| Investigate Claim | `{investigated(c, o)}` |
| Reject Claim | `{rejected(c)}` |
| Determine Payout | `{approved(c), payout(c, t)}` |
| Write Assessment Report | `{assessed(c, r)}` |

---

## 6. Effect Scenarios — Formalism

An **effect scenario** is a triple:

$$(\text{cumulative effect},\ \text{scenario label},\ \text{exclude set})$$

| Component | Meaning |
|---|---|
| **Cumulative effect** | A consistent set of clauses describing what holds true at this point |
| **Scenario label** | The exact path taken — a **sequence** of activity IDs. Elements can themselves be **sets** of labels (needed to represent AND-splits, where order is undefined because branches run in parallel) |
| **Exclude set** | A set of label prefixes that this scenario must **never** be merged with (prevents XOR-split branches from being incorrectly combined via AND/OR-merges) |

**Why track the full path (not just the effect)?** Because the same effect at a point may be reachable via multiple paths. The path is needed to (1) determine correct exclude sets, and (2) check "exclusion-compatibility" when merging scenarios later.

---

## 7. Contiguous Task Accumulation

For two sequential tasks with immediate effects:

$$e_i = \{c_{i1}, c_{i2}, \ldots, c_{im}\}, \qquad e_j = \{c_{j1}, c_{j2}, \ldots, c_{jn}\}$$

$$acc(e_i, e_j) = e_j \cup S$$

where $S \subseteq e_i$ is a **maximal** subset such that $S \cup e_j \cup KB$ is consistent (satisfiable).

**Interpretation:** keep *all* of the later task's effect (it's the most recent truth) plus *as much as possible* of the earlier task's effect, dropping only what contradicts.

**Background Knowledge (KB):** some inconsistencies only surface via implicit business rules.
> Example: `RequestApproved` and `RequestDenied` are only inconsistent because of the rule `RequestDenied → ¬RequestApproved`.

**Non-uniqueness:** $acc(e_i, e_j)$ can have **multiple** maximal consistent subsets — each is a distinct, equally valid effect scenario. Non-uniqueness arises specifically when two or more clauses in $e_i$ are only *jointly* inconsistent with $e_j \cup KB$ (removing either alone restores consistency), not when they are inconsistent *independently* (which yields a single unique result).

### 7.1 Worked Example (canonical slide example)

$$e_1 = p \wedge q \ (T1), \qquad e_2 = r \ (T2), \qquad KB = r \rightarrow \neg(p \wedge q) \equiv (\neg p \vee \neg q)$$

**Step 1 — try keeping everything:** $\{p, q, r\}$ → $(\neg p \vee \neg q) = (F \vee F) = F$ → **violates KB**.

**Step 2 — test maximal subsets of $e_1$:**
- $S=\{p\}$: $\{p, r\}$ → $(\neg p \vee \neg q)=(F\vee T)=T$ → consistent ✓
- $S=\{q\}$: symmetric → consistent ✓

**Step 3 — conclusion:** two maximal subsets exist → **non-unique**, two effect scenarios:

$$acc_1(e_1,e_2) = \{r, p\}, \qquad acc_2(e_1,e_2) = \{r, q\}$$

**Detecting a contradiction:** there is no dedicated "contradiction symbol" — inconsistency is *discovered* by assigning truth values to every clause in the candidate set and evaluating the KB clause; if it evaluates to **False**, the set is inconsistent. (Formally, this is the same as deriving $\bot$.)

---

## 8. Accumulation over XOR-, AND-, OR- Splits and Merges

### 8.1 Exclude sets at an XOR-split

> Each effect scenario on the *n* outgoing flows immediately following an XOR-split includes, in its exclude set, the scenario labels of the other *n−1* branches. (Same applies to OR-splits with mutually exclusive guard labels.)

Guard conditions on split branches are also accumulated over outgoing flows, and must remain consistent with them.

### 8.2 AND-merge (ANDacc)

$$E = \{\,acc(es_{1i}, e) \cup acc(es_{2j}, e) \mid es_{1i}\in E_1,\ es_{2j}\in E_2,\ \{es_{1i}, es_{2j}\}\text{ exclusion-compatible}\,\}$$

Only scenarios that are **exclusion-compatible** (neither's label lies in the other's exclude set) may be combined — because both branches genuinely co-occur at runtime, so their effects must not originate from mutually-exclusive (XOR) paths.

### 8.3 XOR-merge (XORacc)

$$E = \{\,acc(es, e) \mid es \in E_1 \text{ or } es \in E_2\,\}$$

Simple union — no compatibility check needed, since only **one** of the branches actually executes at runtime.

### 8.4 OR-merge (ORacc)

$$ORacc(E_1, E_2, e) = ANDacc(E_1, E_2, e) \cup XORacc(E_1, E_2, e)$$

Combines both mechanisms, since an OR-split may result in one or both branches executing.

---

## 9. Worked Examples — Full Cumulative Effect Computations

### 9.1 Example A: Sequential process (no KB) — "Finance Dept"

Process: `Receive Payment Request → Process Payment → Prepare Payment Cheque`

**Objects:** Payment `p`, Money Amount `t`
**State:** `authorized(p)`
**Relationships:** `received(p, t)`, `cheque(p, t)`

| Activity | Immediate effect |
|---|---|
| Receive Payment Request | `{received(p,t)}` |
| Process Payment | `{authorized(p)}` |
| Prepare Payment Cheque | `{cheque(p,t)}` |

No KB → no contradictions possible → accumulation is plain set union at every step:

$$E_{end} = \{received(p,t),\ authorized(p),\ cheque(p,t)\} \quad \text{(unique)}$$

**Key lesson:** when there is no KB linking clauses, $acc(e_i, e_j) = e_i \cup e_j$ — the result is always unique.

### 9.2 Example B: XOR-split process — "Claim Dept"

Process: `Investigate Claim → XOR-split → {Reject Claim | Determine Payout} → XOR-merge → Write Assessment Report`

Using the effects from §5.2:

**Branch 1 (Reject):**
$$acc(e_1,e_2) = \{investigated(c,o), rejected(c)\}, \quad label\ (t_1,t_2), \quad exclude\ \{(t_1,t_3)\}$$

**Branch 2 (Payout):**
$$acc(e_1,e_3) = \{investigated(c,o), approved(c), payout(c,t)\}, \quad label\ (t_1,t_3), \quad exclude\ \{(t_1,t_2)\}$$

**After XOR-merge + accumulation with Write Assessment Report ($e_4=\{assessed(c,r)\}$):**

$$\text{Scenario 1: } \{investigated(c,o), rejected(c), assessed(c,r)\}, \quad (t_1,t_2,t_4), \quad \{(t_1,t_3)\}$$
$$\text{Scenario 2: } \{investigated(c,o), approved(c), payout(c,t), assessed(c,r)\}, \quad (t_1,t_3,t_4), \quad \{(t_1,t_2)\}$$

**Key lesson:** here, non-uniqueness comes from the **process structure** (XOR-split), not from a KB — a *different source* of multiple scenarios than §7.1.

### 9.3 Example C: Sequential process with contradictions (no split, no KB conflict-independence)

$e_1(T1)=\{p,q\}$, $e_2(T2)=\{v,r,\neg q\}$, $e_3(T3)=\{\neg p, s, h\}$. No KB given (contradictions are direct: $q/\neg q$, $p/\neg p$).

- $acc(e_1,e_2)$: $q$ conflicts directly with $\neg q$ → unique maximal subset $\{p\}$ → result $\{p, v, r, \neg q\}$
- $acc(\cdot, e_3)$: $p$ conflicts directly with $\neg p$ → unique maximal subset $\{v,r,\neg q\}$ → result:

$$E_{end} = \{v, r, \neg q, \neg p, s, h\} \quad \text{(unique — each conflict is independent, not symmetric/competing)}$$

### 9.4 Example D: XOR-split process combined with a KB

Same $e_1, e_2, e_3$ as §9.3, plus $e_4(T4)=\{x,y,z\}$, and $KB: h \rightarrow \neg z$.

Process: `T1 → XOR-split → {T2 | T3} → XOR-merge → T4`

**Branch via T2:** $acc(e_1,e_2) = \{p, v, r, \neg q\}$, label $(t_1,t_2)$, exclude $\{(t_1,t_3)\}$
**Branch via T3:** $acc(e_1,e_3) = \{q, \neg p, s, h\}$, label $(t_1,t_3)$, exclude $\{(t_1,t_2)\}$

**Accumulate T4 into each branch (applying KB where relevant):**

- Scenario A has no `h` → KB not triggered → union freely: $\{p, v, r, \neg q, x, y, z\}$
- Scenario B has `h`, and $e_4$ has `z` → **KB violated** ($h \rightarrow \neg z$) → `h` must be dropped (only clause in conflict): $\{q, \neg p, s, x, y, z\}$

$$\text{Scenario A: } \{p, v, r, \neg q, x, y, z\}, \quad (t_1,t_2,t_4)$$
$$\text{Scenario B: } \{q, \neg p, s, x, y, z\}, \quad (t_1,t_3,t_4)$$

**Key lesson:** a KB does not necessarily affect every scenario equally — it only "fires" where its relevant literals actually appear, which can differ across branches produced by an XOR-split.

---

## 10. Inter-Process Relationships

### 10.1 Part-Whole

Exists between two processes when one (the "whole") requires the other (the "part", commonly a sub-process) to fulfill some of its functionality. The whole process must have an activity representing the cumulative effects of the part process.

**Formal specialization condition:** process $Q$ is a specialization of process $P$ iff:

$$(i)\ \forall es_p \in CE(P)\ \exists es_q \in CE(Q): es_q \Rightarrow es_p$$
$$(ii)\ \forall es_q \in CE(Q)\ \exists es_p \in CE(P): es_q \Rightarrow es_p$$

where $x \Rightarrow y$ means $x$ semantically entails $y$, and $CE(\cdot)$ denotes the set of cumulative effect scenarios of a process.

### 10.2 Inter-operation

Exists between two processes when there is at least one message exchanged between them, **and** there is no cumulative effect contradiction between the activities involved in that message exchange.

---

## 11. Summary — Core Takeaways

1. BPMN captures **coordination**, not **effects** — semantic annotation fills that gap.
2. Effects are either **states** (unary) or **relationships** (n-ary, n≥2) — both are just predicates/clauses.
3. Effect propagation is **non-deterministic**: multiple valid **effect scenarios** can exist at any point.
4. Non-uniqueness of $acc(e_i, e_j)$ has **two distinct sources**:
   - A KB creates a **symmetric conflict** among clauses of $e_i$ (§7.1) — multiple maximal consistent subsets.
   - **Process structure** (XOR-splits) creates parallel scenarios (§9.2) — tracked via scenario labels + exclude sets.
5. Contradiction is not a symbol — it is **detected** when a clause set evaluates to False under a truth assignment, checked against KB.
6. AND-merges require **exclusion-compatibility** checks; XOR-merges are plain unions; OR-merges combine both.
7. Effect annotations enable **compliance checking** and **inter-process relationship analysis** (part-whole, specialization, inter-operation) at scale.

---

*Compiled from CSCI427/927 Lecture 4 slides and worked tutorial examples (A/Prof Hoa Khanh Dam, University of Wollongong).*
