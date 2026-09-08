# Conceptual Data Warehouse Design

## 1. Why a Dedicated Conceptual Model for Data Warehouses?

Standard database design follows: **Conceptual (ER diagram) → Logical (normalized relational schema) → Physical (DBMS implementation)**.

Data warehouse design follows the same three-step idea:

```
Conceptual (MultiDim model) → Logical (star/snowflake schema) → Physical (DW implementation)
```

Conceptual data models in general:
- Allow better communication between designers and users to understand application requirements
- Are more stable than implementation-oriented (logical) schemas, which change with the platform
- Provide better support for visual user interfaces

**Problem before MultiDim**: currently, data warehouses are commonly designed directly using logical models (star/snowflake schemas), which is difficult for non-technical users to read and limits requirements to only what the underlying implementation can support. There was no well-established conceptual model for multidimensional data, and prior proposals (based on UML, ER, or ad-hoc notations) had two main problems: they could not express complex kinds of hierarchies, and they lacked a mapping to the implementation platform.

**MultiDim**:
- Based on the entity-relationship model
- Extended with multidimensional concepts: dimensions, hierarchies, facts, measures
- Supports the various kinds of hierarchies found in real-world applications
- Can be mapped to star or snowflake relational structures

## 2. MultiDim Model — Notation

MultiDim reuses many ideas you already know from ER modeling, extended for multidimensional concepts:

| MultiDim concept | ER equivalent you already know | Difference |
|---|---|---|
| **Level** | Entity type | A level sits inside an ordered parent-child chain (a hierarchy); a generic entity type does not |
| **Cardinality** between two levels | Cardinality between two entities via a relationship | Same notation: (0,1) / (1,1) / (0,n) / (1,n) |
| **Fact** | (n-ary) Relationship | A fact must connect to the **leaf level** of multiple dimensions and carries measures — a plain relationship has no such requirement |
| **Key attribute / Descriptive attribute** | Primary key / ordinary attribute | Same concept as in ER |
| **Hierarchy, Criterion** | No direct equivalent in basic ER | Entirely new: basic ER does not support multiple parallel hierarchies for the same dimension |

### Core terms
- **Dimension**: a level, or one or more hierarchies.
- **Hierarchy**: several related levels, forming a sequence of mappings from lower (detailed) to higher (general) levels.
- **Level**: an entity type.
- **Member**: every instance of a level.
- **Child / Parent levels**: the lower and higher levels in a parent-child relationship.
- **Leaf / Root levels**: the first (most detailed) and last (most general) levels in a hierarchy.
- **Cardinality**: minimum/maximum number of members at one level related to members at another level.
- **Criterion**: names/distinguishes different hierarchies that express different hierarchical structures used for analysis (relevant when a dimension has multiple hierarchies).
- **Key attribute**: indicates how child members are grouped.
- **Descriptive attributes**: describe characteristics of members (do not participate in defining a fact).

### Fact
A sample fact with 5 dimensions (Customer, Time, Order, SalesReason, Shipper) illustrates:
- **Fact**: relates measures to leaf levels in dimensions.
- Dimensions can be related to a fact with **one-to-one**, **one-to-many**, or **many-to-many** cardinality.
  - Example of many-to-many: an order (`Sales`) can have several `SalesReason`s (e.g., a promotion *and* a referral at the same time), and one `SalesReason` applies to many orders.
- A dimension can be related to a fact **multiple times, playing different roles** — called a **role-playing dimension**.
  - Example (Northwind): `Time` is linked to `Sales` three times: `OrderDate`, `DueDate`, `ShippedDate`. All three use the same underlying hierarchy (`All → Year → ... → Day`), but each carries a different analytical meaning (do not confuse this with *cardinality*, which separately describes the min/max count for each of those individual links).

### MultiDim Conceptual Schema of the Northwind Data Warehouse
A complete worked example combining all the above: fact `Sales` (measures: Quantity, UnitPrice, Discount, Freight, SalesAmount, ...) connected to dimensions `Time` (hierarchy `Calendar`: Day→Month→Quarter→Semester→Year), `Product` (hierarchy `Categories`), and several role-playing/geography dimensions (hierarchy `Geography`: City→State→Region→Country→Continent) for Customer, Employee, Supplier, etc.

## 3. Understanding ER Cardinality Notation (Foundational — Read First)

A **(min, max)** cardinality pair measures **one single thing**: the number of instances of *one* level, per single instance of the *other* level. It is **not** "one number for the parent, one number for the child" — both numbers in the pair describe the *same* counted entity.

Rule of thumb: the cardinality written near one end of a relationship counts **how many instances of the entity at the opposite end** relate to a single instance at *this* end.

Worked example — `Product`—`Category`:
```
Product ──(1,1)───────────(1,n)── Category
         │                        │
   "each Product belongs   "each Category has at
    to exactly 1 Category"  least 1, possibly many,
    (counts Category)        Products" (counts Product)
```

- **(1,1)** near `Product`: counts *Category* per Product → exactly one.
- **(1,n)** near `Category`: counts *Product* per Category → at least one, possibly many.

| Notation | Reading | Meaning |
|---|---|---|
| (1,1) | mandatory-one | Each instance has **exactly 1** related instance |
| (0,1) | optional-one | Each instance has **0 or 1** related instance |
| (1,n) | mandatory-many | Each instance has **at least 1**, possibly many |
| (0,n) | optional-many | Each instance has **0 or many** related instances |

Worked example — `Employee`—`Department`:
```
Employee ──(1,1)──────────(0,n)── Department
```
- (1,1) near `Employee`: each Employee belongs to exactly one Department (counts Department per Employee).
- (0,n) near `Department`: each Department can have 0 or many Employees (counts Employee per Department — e.g., a newly opened department may not have staff yet).

This notation is the key to correctly distinguishing Balanced vs Unbalanced hierarchies below.

## 4. Dimension Hierarchies — 5 Types

### a) Balanced Hierarchy
**Schema level**: a single path; all parent-child relationships are **many-to-one and mandatory** — i.e., counting the parent per child is (1,1), and counting the child per parent is (1,n).

**Instance level**: members form a balanced tree — every branch has the same length. Every parent has at least one child, every child belongs to exactly one parent.

Example: `Product → Category`. Every product belongs to exactly one category; every category has at least one product.

```
                all
        ┌────────┼────────┐
    Beverages    ...    Seafood
     ┌───┼───┐          ┌───┼───┐
   Chai Chang ...     Ikura Konbu ...
```

### b) Unbalanced Hierarchy
**Schema level**: still one path, still many-to-one, but **some cardinalities are optional** — specifically, the child-per-parent count can be **(0,n)** instead of the mandatory (1,n): a parent is allowed to have zero children at the immediately lower level.

Example: `ATM → Agency → Branch → Bank`. Not every Bank has a Branch, not every Branch has an Agency (some banks transact directly).

**Instance level**: the tree is unbalanced — branches have different lengths, because some branches terminate early where an intermediate level has zero members.

```
                    bank X
        ┌─────────────┼─────────────┐
     branch 1      branch 2      branch 3
     ┌───┴───┐   (no children,  ┌───┴───┐
  agency11 agency12  ends here) agency31 agency32
    ┌─┴─┐
 ATM111 ATM112
```

### c) Recursive Hierarchy
A special case of Unbalanced hierarchy: the **same level** is linked to itself through the two roles of a single parent-child relationship. Used when all hierarchy "levels" express the same semantics, and the characteristics of parent and child are similar (or identical).

Example: `Employee — Supervision → Employee` (an employee supervises other employees, who may themselves supervise others).

```
                Andrew Fuller
      ┌────┬────────┼────────┬────┐
   Nancy Janet   Margaret  Steven  Laura
                             ┌──┴──┐
                          Michael Robert
```

Because the depth of supervision chains is unknown in advance (some employees supervise no one, others supervise people who themselves supervise others), aggregating "total sales of everyone under Andrew Fuller" requires a **recursive** roll-up (`RECOLLUP`) that traverses an arbitrary number of levels, rather than a regular `ROLLUP` which only aggregates across a single, fixed step between two levels.

### d) Generalized Hierarchy
**Schema level**: **multiple mutually exclusive paths**, sharing at least the leaf level (and possibly other levels too). The exclusive-or relationship is drawn with an **X inside a circle (⊗)** on the connecting lines.

Example: `Customer` (shared leaf) splits into two exclusive paths: `Sector` (for company customers) or `Profession` (for individual customers), which converge again at a shared level, `Branch`.

```
Customer (shared leaf)
    │
   CustType (branching point, marked with ⊗)
   ╱                  ╲
Sector              Profession
   ╲                  ╱
        Branch (convergence point)
```

**Instance level**: each member belongs to exactly one of the paths (e.g., "company Z" follows Sector, "person X" follows Profession — never both).

Relation to ER: this corresponds to **specialization/generalization (is-a)** in Extended ER — a child entity has multiple mutually-exclusive subtypes.

**Generalized vs Recursive**: Recursive has only **one** level type that links to itself. Generalized has **multiple, distinctly named** level types (e.g., Sector and Profession) standing in parallel, mutually exclusive, that converge again at a shared level.

### e) Noncovering Hierarchy
Also called **ragged** or **level-skipping** hierarchy. A special case of Generalized hierarchy, but the alternative paths arise from **skipping one or more intermediate levels within the same hierarchy** — not from two genuinely different kinds of entities.

Example: `City → State → Region → Country`. For most countries the full 4-level path applies, but for Vatican (a very small country) there is no State/Region — it goes directly `City (Vatican) → Country (Vatican)`.

**Instance level**: the path length from leaf to the same-typed ancestor can differ per member (e.g., Belgium goes through a `Region` — "Wallonie" — before reaching Country, while Germany or Vatican may not).

**Generalized vs Noncovering** (a common point of confusion):
- **Generalized**: two (or more) genuinely different kinds of entities, going through **differently named** levels (e.g., Sector vs Profession).
- **Noncovering**: the **same** chain of identically-named levels, just with some members skipping a few steps in the middle (e.g., still City→...→Country, only missing State/Region for some members).

**Practical difficulty**: if a cube's granularity requires the `Region` level specifically, members like Vatican (which have no Region value at all) create a problem — either they get a `NULL` at that level (and effectively disappear from Region-level reports, causing undercounted totals), or the design must handle the gap explicitly. The standard fix (from the Vaisman & Zimányi textbook) is to introduce a **placeholder member** at the missing level — e.g., create a fictitious `Region` named "Vatican" (same name as the country) so every member has a value at every level, and roll-up remains complete and consistent. The rule is therefore *not* "never skip levels" — skipping is unavoidable for some members — but rather "the design must explicitly account for skipped levels," typically via placeholder members.

### Summary table

| Type | Number of paths | Child→Parent cardinality | Parent→Child cardinality | Key trait |
|---|---|---|---|---|
| Balanced | 1 | (1,1) | (1,n) mandatory | Every branch has equal length |
| Unbalanced | 1 | (1,1) (or (0,1) for skipped members) | (0,n) optional | Branches vary in length; some parents have zero children |
| Recursive | 1 (same level repeats) | (0,1) or (1,1) | (0,n) or (1,n) | Special case of Unbalanced; only one level type, self-referencing |
| Generalized | multiple, mutually exclusive (⊗) | many-to-one per branch | — | Distinctly named levels per branch, converging at a shared level |
| Noncovering | multiple (from level-skipping) | many-to-one | — | Same-named levels throughout; some members skip intermediate steps |

## 5. Full Concept Map (End-to-End)

Two parallel branches, joined only through *members*:

```
Dimension → Hierarchy (fixed set of Levels) → Level → Member → Attribute
                                                          │
                                                          ▼ (one Member per dimension, combined)
                                              Fact / Cell → Measure
```

- **Dimension**: an axis of analysis.
- **Hierarchy**: the entire, fixed structure of levels for that dimension (defined once).
- **Granularity**: the specific level, within that hierarchy, chosen for a given cube (can differ between cubes that share the same hierarchy).
- **Member**: a concrete value at a given level.
- **Attribute**: descriptive information about a member; does not participate in defining a fact.
- **Fact / Cell**: the unique combination obtained by picking one member from each dimension (at the cube's chosen granularity).
- **Measure**: the numeric value stored inside a fact.

## Cross-references to prior (ER/SQL) knowledge

| You already know (SQL/ER) | New (MultiDim) knowledge |
|---|---|
| Entity, Relationship, Attribute, Cardinality | Level, Hierarchy (child/parent), Attribute, Cardinality — same notation, extended semantics |
| Self-referencing relationship (e.g., Employee–Manager) | Recursive hierarchy |
| Specialization/Generalization (is-a) in EER | Generalized hierarchy (mutually exclusive paths) |
| — | Data cube, dimension, fact, measure — new concepts unique to the multidimensional model |
| — | Noncovering/ragged hierarchies and placeholder members for level-skipping |
