# Lecture 6: Enterprise Service Architecture

**Course:** CSCI427 / CSCI927 — Systems Development
**Topics:** Enterprise Architecture Foundations · TOGAF (incl. the Architecture Development Method) · ArchiMate
**Acknowledgement:** Adapted from the TOGAF Specification (opengroup.org/togaf), *Modeling Enterprise Architecture with TOGAF* by Gilbert Raymond & Philippe Desfray, and the ArchiMate Specification (opengroup.org/archimate).

---

## Table of Contents

1. [Foundations of Enterprise Architecture](#1-foundations-of-enterprise-architecture)
2. [TOGAF and the Architecture Development Method (ADM)](#2-togaf-and-the-architecture-development-method-adm)
3. [Worked Example: Discount Travel](#3-worked-example-discount-travel)
4. [ArchiMate](#4-archimate)
5. [Limitations of TOGAF](#5-limitations-of-togaf)
6. [References & Tools](#6-references--tools)

---

## 1. Foundations of Enterprise Architecture

### 1.1 What is an Enterprise?

An **enterprise** is any collection of organizations that has a common set of goals and/or a single bottom line. Examples: a government agency, a whole corporation, a division of a corporation, a single department, or a chain of geographically distant organizations linked together by common ownership.

### 1.2 What is an Architecture?

An **architecture** is a formal description of a system, or a detailed plan of the system at component level to guide its implementation. It comprises:

- the structure of the system's **components**,
- their **inter-relationships**, and
- the **principles and guidelines** governing their design and evolution over time.

### 1.3 What is Enterprise Architecture (EA)?

**Enterprise Architecture** is a formal description of an enterprise — a detailed map of the enterprise at component level to guide its changes. It covers the structure of an enterprise's components, their interrelationships, and the principles and guidelines governing their design and evolution over time.

> Enterprise Architecture is about understanding all of the different components that make up the enterprise and how those components inter-relate.

### 1.4 Why Enterprise Architecture?

Organizations spend increasing amounts of money building IT systems, yet find it increasingly difficult to keep those IT systems **aligned** with business needs. Without an overall architecture, application landscapes tend to grow into a tangle of overlapping, poorly integrated systems (customer administration, claims processing, financial applications, policy administration, etc., all loosely and inconsistently wired together) — exactly the situation EA is meant to prevent.

### 1.5 Architecture Description

An **architecture description** is a formal description of an information system, organized in a way that supports reasoning about the system's structural properties. It:

- defines the **components / building blocks** that make up the overall information system, and
- provides a plan from which products can be procured and systems developed that will work together to implement the overall system,

thereby enabling an organization to manage its overall IT investment in a way that meets business needs.

### 1.6 Architecture Framework

An **architecture framework** is a tool for developing a broad range of different architectures. It should:

- describe a **method** for designing an information system in terms of a set of building blocks, and show how the building blocks fit together;
- provide **a set of tools** and a **common vocabulary**;
- include a list of **recommended standards** and compliant products that can be used to implement the building blocks.

TOGAF is one of several architecture frameworks in use (others include DoDAF, MoDAF, FEAF, GEAF, etc.). A common way of organizing an architecture framework is around four domains, stacked from the most abstract to the most concrete:

```
Business  →  Data  →  Application  →  Technology
```

These four domains map directly onto TOGAF's B / C / D phases (see §2).

---

## 2. TOGAF and the Architecture Development Method (ADM)

TOGAF's **Architecture Development Method (ADM)** is a cyclical, iterative process for developing an enterprise architecture. It consists of a **Preliminary Phase**, eight lettered phases (**A–H**), and a central, continuous **Requirements Management** activity. It is usually drawn as a circle rather than a straight line, because Phase H can trigger a brand-new cycle, looping back to Phase A.

```
                     Preliminary
                          |
        H ← Architecture Change Management
        |                                 A ← Architecture Vision
        G ← Implementation Governance      \
        |                    Requirements   B ← Business Architecture
        F ← Migration Planning   Mgmt      /
        |                                 C ← Information Systems Architectures
        E ← Opportunities and Solutions   /
                          \               D ← Technology Architecture
                           \_____________/
```

### 2.1 Preliminary Phase

Prepares the organization to undertake successful architecture projects: defines/tailors the architecture framework to be used, establishes architecture principles, and secures management commitment.

### 2.2 Phase A — Architecture Vision

Initiates a new architecture cycle. Defines the scope and stakeholders, and produces the **Architecture Vision** — a high-level picture of the baseline (current) and target (desired) architecture. **Goals and objectives are established here**, and modeling activity starts at this point.

#### Goals vs. Objectives

TOGAF distinguishes between goals and objectives:

- A **goal** is the "**what**" — the desired result.
  *Example: "Be one of the global top five in our activity sector in 5 years."*
- An **objective** breaks a goal down into a **time-specific milestone**, corresponding to progress made toward the goal. It is the "**how**" — the course of action that leads to the goal being achieved.
  *Example: "Increase the use of our transport capabilities by 30% by the end of next year."*

Objectives set the targets for goals, so that progress can be monitored.

#### SMART Objectives

A good objective must be **SMART**:

| Letter | Meaning |
|---|---|
| **S**pecific | Determines exactly what must be done in the business |
| **M**easurable | Implements clear metrics for success |
| **A**ttainable | Breaks the problem down clearly and provides a basis for determining the elements and plans of the solution |
| **R**ealistic | Indicates deadlines and conditions that can be met by the enterprise's capabilities within stipulated time and cost limits |
| **T**imely | Explicitly indicates when interest in the solution will disappear |

#### Goal Decomposition

Goals are constructed **hierarchically**:

- For every high-level goal, ask *"How can we reach this goal?"* to identify lower-level goals (generally objectives).
- Conversely, for a low-level objective, ask *"Which objective or goal will this help us reach?"*
- For every breakdown, consider **alternative breakdowns**: *Do any obstacles hinder the realization of the current goal? What other paths could reach the higher-level goal?*
- Analysis of the resulting goal graph also examines **consistency and conflicts** between goals: some goals reinforce each other (**positive influence**), others contradict each other (**negative influence**).
  *Example: improving customer service (which requires more staff) conflicts with reducing costs.*

### 2.3 Phase B — Business Architecture

Models the goals, objectives, organization, business processes, functions and capacities, and business entities of the enterprise, at both baseline and target level.

A **business function** carries out one of the enterprise's capacities, performed continuously to guarantee one of the enterprise's missions. The enterprise as a whole is described through all of its capacities and the services that deliver them.

### 2.4 Phase C — Information Systems Architectures

Identifies IS components and their interactions in order to meet business architecture expectations, while guaranteeing overall consistency and respecting the rules of the architecture framework. It has two parts:

- **Data Architecture**
- **Application Architecture**

The central artifact of Phase C is the **Application Communication Diagram**, which presents the architecture and positioning of application components — from which components and applications are identified and their interfaces and interconnections are defined.

#### Data Architecture: Logical vs. Physical

| | Logical Data Architecture | Physical Data Architecture |
|---|---|---|
| Describes | Data entities, attributes, and relationships at the business/conceptual level | Concrete implementation on a specific technology: tables, data types, keys, indexes, storage allocation |
| Technology-dependent? | No — independent of implementation technology | Yes — tied to a specific DBMS/platform |
| ArchiMate equivalent | **Data Object** (Application Layer) | **Artifact** (Technology Layer) |

Separating the two levels is what lets an organization change database technology (e.g. Oracle → PostgreSQL) by redesigning only the physical layer, leaving the logical model untouched.

Typical Phase C deliverables include: Data Entity/Data Component Catalog, Data Entity/Business Function Matrix, Conceptual Data Diagram, Logical Data Diagram, Data Dissemination Diagram, Data Security Diagram, Data Migration Diagram, and Data Lifecycle Diagram.

### 2.5 Phase D — Technology Architecture

Describes the logical software and hardware capabilities required to support the deployment of business, data, and application services. Technology Architecture associates **application components** (from Phase C) with **technology components** representing software and hardware, giving a more concrete view of how application components will be **realized and deployed**.

### 2.6 Phase E — Opportunities and Solutions

The transition point from *planning* to *implementation*. Groups architecture elements into feasible **work packages**, evaluates solution options (build vs. buy, in-house vs. outsourced), and — if the baseline cannot be reached in a single step — defines intermediate **transition architectures**.

### 2.7 Phase F — Migration Planning

Produces a detailed, prioritized **migration plan** (cost, benefit, and risk based) — an **implementation roadmap** with a concrete order and timeline for the work packages defined in Phase E.

### 2.8 Phase G — Implementation Governance

Oversees the actual implementation, ensuring **architecture compliance**: that delivered systems conform to the architecture that was designed.

### 2.9 Phase H — Architecture Change Management

Establishes procedures for managing change to the new architecture after deployment. Monitors technology, regulatory, or business changes that may trigger a **new ADM cycle**, starting again from Phase A — which is why the ADM is drawn as a circle.

### 2.10 Requirements Management

Not a sequential phase but a **continuous process running throughout the whole ADM cycle**. It ensures that every requirement raised in any phase is:

- captured in a central requirements repository,
- tracked (active, addressed, discarded, etc.), and
- routed to the phase(s) responsible for resolving it —

without necessarily waiting for a new cycle to start.

### 2.11 Summary Table

| Group | Phase(s) | Focus |
|---|---|---|
| Preparation | Preliminary | Framework setup, principles |
| Direction | A | Vision, scope, goals/objectives |
| Architecture design | B, C, D | Business → Data/Application → Technology |
| Transition to delivery | E, F | Identify opportunities, plan migration |
| Delivery & maintenance | G, H | Compliance governance, change management → back to A |
| Cross-cutting | Requirements Management | Capture and route requirements across every phase |

---

## 3. Worked Example: Discount Travel

Discount Travel is a service provider that offers the public a list of trips not sold by travel agencies, at discounts of up to 50%, with fixed and often imminent departure/return dates (clients must be willing to depart within **2 weeks** of booking).

**Baseline (current state):**
- A telephone service, open 8am–8pm Monday–Friday; a customer advisor helps the client select a trip.
- Business processes are **not formalized**; the information advisors use is on **paper documents**, updated daily by the marketing department.
- A website exists that captures order elements, but these are then processed **manually** by an agent; orders are recorded by sales representatives in an internal application.

**Target (desired state):** an **online reservation service**, with improved customer service — which is why the information system design needs to be reviewed.

**Key data model (Logical Data Architecture):**

- A **Trip** corresponds to a *format* (a combination of Flight + Hotel + Car Rental), a *destination*, and an *accommodation service*.
- A **Destination** is identified by *continent* (North Africa, Africa except North Africa, Europe, Asia, America) and *country*.
- **Business rule:** a Trip takes place in exactly **one country only**.
- **Order** contains multiple **Order Lines**, each referencing a **Trip**; a **Client** books an **Order**.

**Key stakeholders/actors:** Client, Customer Advisor, Agent, Sales Representative, Marketing Department, Travel Agencies (external partner).

**Core use cases (target system):** Search/Consult Trips, Reserve Trip, Cancel Trip, Consult Order Status (Client); Update Trip Stock, Manage Travel-Agency Relationship / define priority products (Marketing).

**Core goals:** improve customer service; provide an online reservation service; reduce order/file processing time; increase the number of trips reserved per day.

This case is used throughout the lecture (and its accompanying handout) to illustrate goal diagrams, use case diagrams, class diagrams, and ArchiMate models using UML and BPMN, applying TOGAF.

---

## 4. ArchiMate

ArchiMate is a modeling **language** used to actually draw the architectures that TOGAF's ADM calls for (TOGAF itself is a *method*, not a notation — it borrows UML, BPMN, and ArchiMate to visualize architecture).

### 4.1 The Core Framework: 3 Layers × 3 Aspects

ArchiMate organizes concepts along **three layers** and **three aspects**, forming a 3×3 grid.

**The three layers** (each realizing the one above it):

| Layer | Description |
|---|---|
| **Business Layer** | Offers products and services to external customers, realized in the organization by business processes performed by business actors. |
| **Application Layer** | Supports the business layer with application services, realized by (software) applications. |
| **Technology Layer** | Offers infrastructure services (processing, storage, communication) needed to run applications, realized by computer/communication hardware and system software. |

`Technology Layer` → *realizes* → `Application Layer` → *realizes* → `Business Layer`

**The three aspects** (repeated in every layer):

| Aspect | Question answered | Description |
|---|---|---|
| **Active Structure** | *Who acts?* | The structural concepts — the business actors, application components, and devices that display actual behavior (the "subjects" of activity). |
| **Behavior** | *What do they do?* | Processes, functions, events, and services performed by the actors; behavioral concepts are assigned to structural concepts to show who/what performs the behavior. |
| **Passive Structure** | *On what do they act?* | The objects on which behavior is performed — usually information objects (business layer) or data objects (application layer), occasionally physical objects. |

A useful shortcut when meeting an unfamiliar term: (1) identify its **layer** from the prefix (Business.../Application.../Technology...); (2) identify its **aspect** — a noun for an actor/component/node is Active Structure, an "-ing"/process/function/service word is Behavior, an object/data noun is Passive Structure.

**Service vs. Function/Process**, at every layer, follow the same pattern: a **Service** is what the outside world sees (a promise of value), while a **Function**/**Process** is the internal way that promise is delivered — internal behavior can change without affecting the external service.

### 4.2 Business Layer

| Aspect | Concepts |
|---|---|
| Active Structure | Business Actor, Business Role, Business Collaboration, Business Interface, Location |
| Behavior | Business Process, Business Function, Business Interaction, Business Event, **Business Service** |
| Passive Structure | Business Object, Representation, Meaning, Value, Product, Contract |

- **Business Service**: externally visible behavior — a coherent piece of functionality that offers added value to the environment, independent of how it is realized internally.
- **Representation**: a specific way a Business Object is presented (e.g. *Electronic invoice* and *Paper invoice* are both Representations of the Business Object *Invoice*).

### 4.3 Application Layer

| Aspect | Concepts |
|---|---|
| Active Structure | Application Component, Application Collaboration, Application Interface (application-to-application or application-to-business) |
| Behavior | Application Function, Application Interaction, Application Process, Application Event, **Application Service** |
| Passive Structure | **Data Object** |

- **Application Component**: the main active-structure concept of this layer; component relationships form an *Application Collaboration*.
- **Application Service vs. Application Function**: Service = external behavior; Function = internal behavior realizing that service.
- **Data Object**: used the same way as a "class" in a UML class diagram; a representation of a business object at the application layer.

### 4.4 Technology Layer

| Aspect | Concepts |
|---|---|
| Active Structure | **Node**, Device, System Software, Infrastructure/Technology Interface, Communication Path |
| Behavior | Technology Function, Technology Process, Technology Interaction, Technology Event, **Technology (Infrastructure) Service** |
| Passive Structure | **Artifact** |

- **Node**: the main active-structure concept; models the purely structural aspect of a system (its behavior is modeled via an explicit relationship to behavioral concepts).
- **Infrastructure Service vs. Infrastructure Function**: e.g. a DBMS offers infrastructure services *Data access* and *Data management*, realized internally by functions *Providing data access* / *Managing data*. Message-Oriented Middleware (MOM) offers a *Messaging service* via an EJB server.
- **Artifact** (introduced in ArchiMate 3.0): a concrete piece of physical data (a file, a real database table) stored on a node — this is the **physical** counterpart of a (logical) Data Object.

### 4.5 Relationships

ArchiMate defines a fixed set of relationships connecting elements, grouped as follows.

**Structural relationships** ("how is this organized?"):

| Relationship | Meaning | Notation |
|---|---|---|
| **Composition** | A is an inseparable *part* of B — A cannot exist if B does not | filled diamond at the whole end |
| **Aggregation** | A belongs to B, but can exist independently | hollow diamond at the whole end |
| **Assignment** | assigns active structure to behavior (who performs what), or an actor to a role | filled circle at source, filled arrowhead at target |
| **Realization** | a concrete element realizes a more abstract one | dashed line, hollow triangle arrowhead |

**Dependency relationships** ("how does one depend on / affect another?"):

| Relationship | Meaning |
|---|---|
| **Serving** (formerly "used by") | A provides functionality that B uses |
| **Access** | a behavior reads/writes/updates/deletes a passive structure element |
| **Influence** | A affects B positively (+) or negatively (−) — heavily used in the Motivation extension (e.g. goal conflicts, see §2.2) |

**Dynamic relationships** ("what happens in what order / what moves?"):

| Relationship | Meaning |
|---|---|
| **Triggering** | one behavior's completion starts another (temporal sequence) |
| **Flow** | value/information/goods move from one behavior to another |

**Other relationships:**

| Relationship | Meaning |
|---|---|
| **Specialization** | an "is-a" relationship, like inheritance in UML |
| **Association** | a generic relationship when none of the above fits |

**Exam tip:** hollow triangle + **dashed** line = Realization; hollow triangle + **solid** line = Specialization — these two are the easiest to confuse.

### 4.6 Extensions Beyond the Core Three Layers

#### Motivation Extension — answers "WHY"

Wraps around all three layers, giving formal modeling elements to anchor goals/objectives (from Phase A) into the architecture:

- **Stakeholder** — a person/group with an interest in the architecture's outcome
- **Driver** — a condition motivating change (external: regulation, competition; internal: desire to improve)
- **Assessment** — the result of analyzing a driver (e.g. a SWOT finding)
- **Goal** — a desired end result (see §2.2)
- **Outcome** — a concrete, measurable result actually achieved
- **Principle** — a general guideline directing design
- **Requirement** — a specific demand the architecture must satisfy
- **Constraint** — a Requirement that is a limitation (budget, deadline, etc.)

Typical chain: *Stakeholder* has a *Driver* → *Driver* leads to an *Assessment* → *Assessment* suggests a *Goal* → *Goal* is realized via *Requirements*.

#### Strategy Extension (ArchiMate 3.0) — answers "WITH WHAT CAPABILITY"

Sits between Motivation and the Business Layer:

- **Resource** — an asset the enterprise owns/controls (people, finance, systems, knowledge)
- **Capability** — an ability the enterprise can deploy (e.g. "the ability to take online reservations")
- **Course of Action** — an approach/plan to achieve a goal by building/using a capability
- **Value Stream** — an end-to-end sequence of activities creating value for a stakeholder

#### Implementation & Migration Extension — supports ADM Phases E–H

- **Work Package** — a concrete project/package of work (Phase E)
- **Deliverable** — the output of a work package
- **Plateau** — a stable state of the architecture at a point in time (baseline, each transition architecture, and target are each a Plateau)
- **Gap** — the difference between two plateaus (gap analysis)
- **Implementation Event** — an event occurring during implementation

### 4.7 Other Elements

| Element | Meaning |
|---|---|
| **Location** | a geographic or logical position; can be assigned to any active-structure element (appears in the Business Layer's list of active-structure concepts) |
| **Grouping** | groups conceptually related elements for visual clarity — no structural meaning |
| **Junction** | a branch point (AND/OR) used when a relationship needs to split — e.g. one process triggering two others simultaneously |
| **Equipment** *(physical, Technology Layer, v3.0)* | physical devices — printers, scanners, trucks |
| **Facility** *(physical, v3.0)* | a physical facility — a data center, a warehouse |
| **Distribution Network** *(physical, v3.0)* | a physical network moving materials/energy (distinct from Communication Path, which moves data) |

---

## 5. Limitations of TOGAF

Formal architecture description does very well at capturing structural elements (Business/Data/Application/Technology), but has known gaps:

1. **No formal Motivation domain in the core BDAT model** — goals/drivers at Phase A are narrative text, not formally modeled elements that trace down to architecture components. This is exactly why ArchiMate had to add a separate Motivation extension.
2. **No Strategy layer in the original BDAT model** — no formal notion of Capability, Resource, or Course of Action (added later by ArchiMate 3.0's Strategy layer).
3. **TOGAF provides no modeling notation of its own** — it is a *method*, and must borrow UML, BPMN, or ArchiMate to actually draw the architecture.
4. **Informal/soft aspects of the organization** — culture, internal politics, tacit knowledge — are hard to capture in a formal architecture model.
5. **Architecture drift** — an architecture description is a static snapshot; without rigorous governance (Phase G/H) it easily becomes outdated as the real system evolves.
6. **Security and non-functional requirements** are not first-class domains in the original BDAT model, and are usually bolted on separately.
7. **Sequential framing of the ADM** can be a poor fit for organizations running multiple, interdependent change initiatives in parallel (e.g. agile/DevOps environments), since ADM governance leans toward centralized, longer-cycle control.

---

## 6. References & Tools

- TOGAF® Specification — The Open Group — <http://www.opengroup.org/togaf>
- *Modeling Enterprise Architecture with TOGAF* — Gilbert Raymond, Philippe Desfray
- ArchiMate® Specification — The Open Group — <http://www.opengroup.org/archimate>
- **Archi** — free, open-source, cross-platform ArchiMate modeling tool and editor — <https://www.archimatetool.com>
