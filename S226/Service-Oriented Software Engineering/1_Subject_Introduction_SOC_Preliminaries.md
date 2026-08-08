# Lecture 1 — Subject Introduction & Service-Oriented Computing (SOC) Preliminaries

---

## 0. Why This Lecture Matters (Read This First)

Before diving into services, registries, and protocols, it helps to understand *why* this subject exists. Traditional software engineering builds monolithic applications where every piece of functionality lives inside one deployable unit. **Service-Oriented Computing (SOC)** is a different philosophy: instead of building everything yourself, you expose (or consume) discrete, reusable units of functionality — **services** — that can be found, combined, and orchestrated to build larger systems, often across organizational boundaries.

This whole subject is essentially the *lifecycle* of that idea:
1. Understand what a service is (this lecture).
2. Learn how to **describe** a service so others can understand and use it (Lecture 2).
3. Learn how to **model the business processes** that services support or automate (Lecture 3).
4. Add **semantics** so machines — not just humans — can reason about services (later lectures).
5. Learn how to **design, compose, and architect** systems out of services.
6. Learn how to **operate, monitor, and govern** those systems once they're live.

Keep this "roadmap" in mind — it's expanded in Section 4 below.

---

## 1. Course Administration & Logistics

### 1.1 Teaching Staff
| Role | Details |
|---|---|
| Lecturer | A/Prof Hoa Khanh Dam |
| Qualifications | PhD (Computer Science, RMIT University); M.App.Sc (IT, RMIT University); BCompSc (University of Melbourne) |
| Industry background | Technical Architect / Project Manager at B.A.O. Solutions; Software Engineer at Exari Systems |
| Research interests | Artificial Intelligence & Software Engineering |
| Office | 3.201 |
| Consultation hours | Monday 09:30–11:30, Thursday 09:30–11:30 |
| Email | hoa@uow.edu.au |

> 💡 **Why it matters for you:** the lecturer's own background (technical architecture + project management + research) reflects the dual nature of this subject — it blends practical software engineering (build systems) with conceptual/research-level thinking (modelling languages, R&D challenges).

### 1.2 Timetable
| Session | Weeks | Time | Notes |
|---|---|---|---|
| Lecture | Week 1–13 | Wednesday 13:30–14:30 | Core content delivery |
| Lecture/Tutorial | Week 2–12 | Wednesday 14:30–16:30 | First half continues the lecture; second half is tutorial/workshop (order sometimes swapped) |

**Attendance policy:** Class attendance is required and may be recorded/tracked.
**Delivery mode:** Online lectures/tutorials are exclusively for **Liverpool campus** students. **Wollongong campus** students must attend all classes **in person**.

### 1.3 Subject Objectives
By the end of this subject, you should be able to:
1. **Build** service-oriented systems and **describe their architecture**.
2. **Identify and apply** software engineering methodologies/tools specific to service-oriented systems.
3. **Apply techniques and tools** for the **management and maintenance** of service-oriented systems (i.e., it's not just about building — it's about running them long-term).
4. **Discuss R&D challenges and open questions** in the field (this subject sits at the intersection of industry practice and active research).

> 💡 **Prerequisite expectation:** Basic background/experience in programming (front-end and/or back-end) is recommended before taking this subject — this is a design/modelling-heavy subject built *on top of* programming skills, not a replacement for them.

### 1.4 Resources
- **Lectures:** PDF slide decks.
- **Assignments:** distributed via the subject's learning platform.
- **Supplementary materials:** additional readings, papers.
- **One-stop shop:** Moodle (all of the above are hosted here).

### 1.5 Assessment Breakdown
| Component | Weight | Details |
|---|---|---|
| Quiz | 5% | Held in Week 6 Tutorial |
| Group Project | 40% | Progress report due Week 4; final deliverables + presentations in Week 12 |
| Examination | 55% | Final exam |

**⚠️ Technical Fail (TF) rule:** To be eligible for a Pass, a student must achieve **at least 40% in the Final Examination**, *regardless of overall mark*. If a student's overall mark would otherwise be a Pass but they score below 40% in the exam, they can be awarded a **Technical Fail (TF)** instead. This means:
- You cannot rely purely on quiz + group project marks to carry you through.
- You must dedicate real, standalone effort to exam preparation, independent of how well the group project goes.

### 1.6 The Group Project
- **Group size:** 5–6 people.
- **Formation:** Students are responsible for forming their own groups (use the Moodle forum to find teammates if needed).
- **Deadline to register:** End of Week 2 — group membership details must be submitted via Moodle's group registration link.
- **Rule:** Only **one registration per group** (i.e., someone submits on behalf of the whole group, not everyone individually).
- **Milestones:** Progress report (Week 4) → Final deliverables + presentations (Week 12).

### 1.7 The "Q&A" Slide — What It's Really Telling You
The lecture includes a humorous Q&A exchange about getting a High Distinction (HD). Stripped of the humor, the actual advice is:
- **Yes, an HD is achievable** — but there's no shortcut.
- You need to: do the **lab exercises every week**, work consistently on the **group project**, **attend lectures regularly** (explicitly called "very important" for this subject), and **read the reference texts and slides**.
- **Cramming in the last week doesn't work** — the subject rewards steady, cumulative effort (unsurprising, given it's a modelling/design subject where concepts build on each other week-to-week).
- Even aiming for a bare Pass (P) requires doing essentially the *same activities* — just to a lower depth/quality. There is no "low-effort path" through this subject; the studying process is the same, only the polish/depth changes.

---

## 2. Topics Covered in This Subject

The subject slide lists these topics in order:
1. Service-Oriented Computing: Preliminaries
2. Service Modelling
3. Business Process Modelling and Management
4. Semantic processes and services
5. Service Design, Composition, Interoperation
6. Enterprise Service Architectures
7. Service-oriented architectural patterns
8. Service analytics & process mining
9. Case studies + Modern industry trends
10. Service compliance management

---

## 3. Understanding the Big Picture: How These Topics Connect

The topic list above can look like an arbitrary sequence of buzzwords until you see how they build on each other. Here is an expanded, explained roadmap (this goes beyond the bare titles on the slide, to help you situate each future lecture):

| # | Topic | What it's actually about | Where it fits |
|---|---|---|---|
| 1 | **SOC Preliminaries** (this lecture) | Foundational vocabulary: what is a service, a provider, a consumer, a registry, composition. | The "alphabet" you need before anything else makes sense. |
| 2 | **Service Modelling** | How do we *formally describe* a service (its functionality, how to invoke it, its quality)? Introduces BSRL and standards like WSDL/OWL-S. | Answers: "How do I write down what a service does, so someone else — human or machine — can understand and use it?" |
| 3 | **Business Process Modelling & Management (BPMN)** | How do we model the *business processes* — the sequences of activities, actors, and decisions — that services support or automate? | Services rarely exist in isolation; they're invoked as steps inside a larger business process. BPMN is the notation for drawing that process. |
| 4 | **Semantic processes and services** | Adding machine-readable *meaning* (ontologies, semantics) to service/process descriptions, so software agents can automatically discover, match, and compose services without a human manually reading documentation. | Extends Topic 2 with "smarter" descriptions — moves from *syntax* (data formats) to *semantics* (meaning). |
| 5 | **Service Design, Composition, Interoperation** | Principles and techniques for designing individual services well, and combining ("composing") multiple services into a working solution, even when they come from different vendors/technologies ("interoperation"). | Practical engineering — how to actually build with services once you know how to describe and model them. |
| 6 | **Enterprise Service Architectures** | How services fit into an organization's overall IT architecture (e.g., Enterprise Service Bus, layered SOA reference architectures, governance structures). | Zooms out from a single service/process to the whole enterprise landscape. |
| 7 | **Service-oriented architectural patterns** | Reusable, proven design solutions (e.g., broker, façade, gateway patterns) for recurring problems when architecting SOA-based systems. | The "design patterns" equivalent, but for service architectures specifically. |
| 8 | **Service analytics & process mining** | Once processes/services are *running*, how do we analyze the data they generate (logs, events) to understand actual behaviour, detect bottlenecks, and improve them? | Moves from *design-time* concerns (topics 1–7) to *run-time/operational* concerns. |
| 9 | **Case studies + Modern industry trends** | Real-world applications and current trends (e.g., microservices, API economy, cloud-native services) that show how these academic concepts are used in practice today. | Grounds the theory in reality. |
| 10 | **Service compliance management** | Ensuring that services and processes conform to regulations, internal policies, and contractual obligations (governance and auditing). | Closes the loop — once systems are built and running, are they still *allowed* to operate this way? |

> 💡 **Mental model:** Think of it as **Describe (2) → Orchestrate as a Process (3) → Make Machine-Understandable (4) → Build & Combine (5) → Fit into the Enterprise (6–7) → Operate & Improve (8) → Ground in Reality (9) → Govern (10)**.

---

## 4. Core Reading: Papazoglou's "Service-Oriented Computing: Concepts, Characteristics and Directions"

The lecture sets a reading exercise based on the paper by **Mike P. Papazoglou** (2003), a foundational SOC paper. You are asked to answer a set of conceptual questions and give an example for each. Below is a fully worked-through set of answers — useful both as an answer key and as a way to firmly ground the vocabulary you will use for the *entire rest of the subject*.

### 4.1 What is a service?
A **service** is a self-contained, technology-neutral, well-defined unit of functionality that can be **published, discovered, and invoked** over a network using standard protocols. It exposes *what it does* through a public interface while hiding *how it does it* (its internal implementation).

> **Example:** An online currency-conversion service that accepts an amount plus two currency codes and returns the converted amount — any application can call it without knowing (or caring) how exchange rates are computed internally.

### 4.2 What are service characteristics?
Common characteristics repeatedly emphasized in the SOC literature:
- **Loosely coupled** — provider and consumer depend on each other only through the published interface, not on internal implementation details.
- **Encapsulated / black-box** — internal logic is hidden.
- **Platform/technology-neutral** — invocable regardless of the caller's programming language or platform, via standard protocols (e.g., XML, HTTP).
- **Discoverable / self-describing** — a published description allows others to find and understand it.
- **Composable** — services can be combined to build higher-level services or processes.
- **Location-transparent** — a consumer can invoke a service without needing to know its physical location (this is what a registry is for).
- **Reusable** — designed to be used across multiple applications/contexts, not tied to one.
- **Coarse-grained** — services typically expose business-significant chunks of functionality, rather than fine-grained method calls.

> **Example:** A bank's "credit-check" service can be reused, unmodified, by a loan-approval process, a credit-card application process, and a mortgage pre-qualification tool — none of which need to know how the credit score is actually calculated.

### 4.3 What are the two main service types?
- **Elementary / atomic services** — perform a single, indivisible unit of work; not built by combining other services.
- **Composite services** — built by combining (orchestrating) two or more atomic and/or composite services to deliver a higher-level function.

> **Example:** A "verify-passport" service is atomic. A "process-visa-application" service that internally calls verify-passport, check-criminal-record, and issue-visa-document is composite.

### 4.4 What are the differences between a service and a software functionality?
| Aspect | Ordinary software function/module | Service |
|---|---|---|
| Coupling | Tightly coupled to the application it's embedded in | Loosely coupled — independent of the caller |
| Invocation | Local call / proprietary API, technology-specific | Standard, network-based, technology-neutral protocol |
| Visibility | Often internal only, not published for external use | Published via a description that others can discover |
| Reuse scope | Usually reused within the same codebase/team | Designed to be reused across applications, teams, even organizations |
| Deployment | Bundled and deployed with the application | Independently deployable and versionable |

> **Example:** A private `calculateTax()` method buried inside a payroll application is a software functionality. A published "tax-calculation-as-a-service" that any external payroll system can call over the internet is a service.

### 4.5 What is a service provider?
The organization or system that **implements**, **hosts**, and **publishes** a service, and is responsible for delivering the promised functionality (and honoring its quality-of-service commitments) whenever the service is invoked.

> **Example:** Stripe is the service provider of the Stripe Payments API.

### 4.6 What is a service client/consumer?
The application, process, or another service that **discovers** a published service description and **invokes** it to accomplish part of its own functionality.

> **Example:** An e-commerce checkout page that calls Stripe's Payments API is the service consumer.

### 4.7 What is a service registry?
A **directory/repository** where service providers **publish** descriptions of their services (interface details, location, sometimes quality attributes), allowing consumers to **search and discover** suitable services, and then **bind** to them.

> **Example:** UDDI (Universal Description, Discovery and Integration) is the classic registry standard from the Web services stack (see also Lecture 2).

> 💡 **The classic SOA triangle:** Provider **publishes** → Registry; Consumer **finds** → Registry; Consumer **binds/invokes** → Provider. This "publish–find–bind" pattern is the backbone of almost every concept in this subject.

### 4.8 What is a service interface?
The **published, technology-neutral specification** of *how to interact* with a service — the operations it offers, and the format of the inputs/outputs for each — without exposing how the service works internally.

> **Example:** A WSDL document describing a weather service's `getForecast` operation: input = (city, date), output = (XML-formatted forecast).

### 4.9 What is a service specification?
Broader than the interface. A specification captures both the **functional** aspects (what the service does — its operations, inputs/outputs, and possibly pre/post-conditions) and the **non-functional** aspects (quality of service, cost, security, etc.) — i.e., the full "contract" governing the service. (This foreshadows BSRL in Lecture 2, which formalizes exactly this idea: goals, conditions, QoS, schedules, penalties.)

> **Example:** A specification for a "package-delivery" service states not just *what* it does (accept a package, deliver to address), but also its guaranteed delivery time (QoS), cost, and penalty if it's late.

### 4.10 What is the difference between service deployment and service realization?
- **Service deployment** = making the service **technically available for execution** — installing/hosting it on infrastructure and publishing its description. It answers *"where and how is it made available?"*
- **Service realization** = the actual **execution** of the underlying logic/process/system that fulfils the service when it is invoked. It answers *"how is the functionality actually produced/delivered?"*

> **Example:** Deploying a "flight-booking" service means putting the software on a server and registering its WSDL. Realizing the service means the actual backend logic — checking seat availability, reserving a seat, charging payment — that runs each time someone calls it.

### 4.11 What is a service aggregator?
An entity/role that **combines multiple existing services** (often from different providers) into a new **composite service**, effectively becoming a provider of the composite while consuming the constituent services underneath.

> **Example:** A travel-booking website that combines a flight-search service, a hotel-search service, and a car-rental service into one "trip-package" service — the website is the aggregator.

### 4.12 What is service composition? (Real-life example, different from the paper)
**Service composition** is the process of combining two or more existing services — via **orchestration** or **choreography** — to create a new, higher-level service or business process that achieves an outcome no individual service could deliver alone.

> **Example (original, not from the paper):** A ride-hailing app composes: a *location service* (find nearby drivers), a *matching service* (assign a driver to the rider), a *payment service* (charge the rider's card), and a *notification service* (send SMS/push updates). None of these alone provides "get a ride" — but composed together, they do.

---

## 5. Key Takeaways / Review Checklist

- [ ] I can state the assessment breakdown and explain the Technical Fail rule.
- [ ] I know the group project size, registration deadline, and milestone weeks.
- [ ] I can explain, in my own words, what SOC is and why it differs from traditional monolithic software development.
- [ ] I can define: **service, service provider, service consumer, service registry, service interface, service specification, service deployment vs. realization, service aggregator, service composition**, and give an example of each.
- [ ] I can describe the "publish–find–bind" triangle.
- [ ] I can explain the difference between an **atomic** and a **composite** service.
- [ ] I can list the 10 topics of the subject and roughly explain how they connect (see Section 3).
