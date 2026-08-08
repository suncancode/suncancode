# Lecture 2 — Service Modelling

---

## 0. Where This Fits
Lecture 1 gave you the vocabulary (service, provider, consumer, registry...). Lecture 2 answers the natural next question: **how do you actually *write down* a service so that both humans (business analysts, contract managers) and machines (software agents, discovery engines) can understand it?** This is "service modelling" — designing a *description language* for services. The lecture builds up to the **Business Service Representation Language (BSRL)**, which tries to be expressive enough to describe *both* a low-level web service *and* a high-level business service (e.g., a legal or consulting service) using the same framework.

---

## 1. Key Ideas: What Must a Service Description Contain?

The lecture poses this as an open question, and answers it by identifying three essential ingredients:

1. **A description of service functionality** — what does the service actually do?
2. **Information on how to invoke the service and interpret its outputs** — the technical "calling convention": data formats, protocols, message structures.
3. **Non-functional (Quality-of-Service, QoS) factors** — how *well* does it do it (speed, reliability, cost, etc.), not just *what* it does.

This leads to the central design question of the lecture:

> **Can we devise a single service description language that seamlessly spans the spectrum from *business services* (e.g., "legal consultation service", "insurance claims service") all the way to *web services* (e.g., a REST/SOAP API)?**

This is the motivating problem behind BSRL — most existing standards (below) were designed *only* for web services, and don't naturally describe a purely business-level service like "our company's dispute-resolution service."

---

## 2. The Existing Landscape of Service Description Standards

Before introducing BSRL, the lecture surveys what already exists, to show what's missing.

### 2.1 Classic Web Service Standards
| Standard | Purpose | Analogy |
|---|---|---|
| **WSDL** (Web Services Description Language) | **Description** — defines a service's operations, and the input/output message formats | The service's "user manual" / interface contract |
| **SOAP** (Simple Object Access Protocol) | **Invocation** — the messaging protocol used to actually call the service and get a response | The "phone line" used to talk to the service |
| **UDDI** (Universal Description, Discovery and Integration) | **Discovery** — the registry standard where services are published so they can be found | The "phone book" (this is the *service registry* concept from Lecture 1!) |

> 💡 Notice this maps exactly onto the "publish–find–bind" triangle from Lecture 1: WSDL is *what* you publish, UDDI is *where* you publish it (and find others), SOAP is *how* you actually call it once found.

### 2.2 Semantic Web Service Modelling Languages
These go a step further than WSDL/SOAP/UDDI by adding **machine-interpretable meaning** (semantics), so software agents — not just humans — can automatically understand, match, and compose services (this previews Lecture 4, "Semantic processes and services"):
- **OWL-S** — an OWL (Web Ontology Language)-based ontology for describing services semantically.
- **WSMO** (Web Service Modeling Ontology) — a comprehensive conceptual model/ontology for semantic web services.
- **WSDL-S** — a lighter-weight approach that adds semantic annotations *on top of* existing WSDL, rather than replacing it.

### 2.3 The Common Underlying Pattern: IOPE
The lecture notes that **most** of these semantic approaches follow the same underlying structure, called **IOPE**:
| Element | Meaning |
|---|---|
| **I — Input** | What data/parameters the service needs to be given |
| **O — Output** | What data/result the service returns |
| **P — Precondition** | What must be true of the world *before* the service can be validly invoked |
| **E — Effect** | What becomes true of the world *after* the service has executed (a.k.a. postcondition) |

> 💡 IOPE is essentially describing a service the same way you'd describe a function in formal logic/programming: given these inputs (and assuming these preconditions hold), the service produces these outputs (and causes these effects on the world). This IOPE thinking directly reappears — expanded — in BSRL's treatment of "Goals" and "Conditions" below.

---

## 3. Business Service Representation Language (BSRL)

BSRL is proposed as a way to describe services that is rich enough to cover **both** business-level and web-service-level descriptions, using a common set of building blocks: **Goals, Conditions & Assumptions, QoS, Delivery Schedules, Payment Schedules, and Penalties.**

### 3.1 Goals

**Definition:** Goals represent **states of affairs we desire to achieve** through the service.

> ❓ **Why are goals described separately from postconditions, if postconditions are also "what becomes true after the service runs"?**
> Because **not every postcondition is *desired*.** Some postconditions are simply unavoidable side effects — "collateral" consequences of executing the service — while a *goal* specifically captures the outcome the client actually *wants*. E.g., a "vaccinate-patient" service has the desired goal "patient-immune", but might also have the collateral postcondition "patient-experiences-mild-soreness" — a true postcondition, but not a goal.

**Three basic kinds of goals a service can help achieve:**
1. **Achieving a condition** — bring about a state that wasn't true before (e.g., "package delivered").
2. **Maintaining a condition** — keep a state true over a period, even as the environment might threaten to change it (e.g., "server uptime maintained above 99.9%").
3. **Avoiding a condition** — prevent a state from ever becoming true (e.g., "no unauthorized data access occurs").

**More complex goals** go beyond simple achieve/maintain/avoid — e.g., **"make the light blink every 5 minutes"** is a *cyclical/temporal* goal: it's not a single state to achieve once, nor a state to maintain constantly, nor one to avoid — it's a *repeating pattern over time*. This shows that goal languages need enough expressive power to capture temporal/periodic behaviour, not just static states.

**How are conditions (used in goals) actually written down?** Three broad approaches:
1. **Natural language** — easy for humans to read, but ambiguous and hard for machines to process automatically.
2. **Structured document formats** — e.g., XML — more machine-processable, still human-readable, but limited expressive/reasoning power.
3. **Formal logic** — most precise and reasoning-capable, but harder to write and read:
   - **First-order logic (FOL)** — good for describing **static** worlds (facts that are simply true or false, without a notion of time/change).
   - **Temporal logic** — good for describing **dynamic** worlds (how truth values of conditions change *over time* — essential for goals like "maintain X" or "make the light blink every 5 minutes").
   - **Other logics** — e.g., dynamic logic (reasoning about actions/programs and their effects), non-monotonic logic (reasoning where conclusions can be retracted as new information arrives), etc.

> 💡 **Takeaway:** there's a fundamental trade-off between *expressiveness/precision* (formal logic) and *ease of authoring/understanding* (natural language). The right choice depends on whether the description needs to be read by a person, parsed by a program, or reasoned over automatically.

### 3.2 Conditions and Assumptions

| Term | Definition |
|---|---|
| **Precondition** | Conditions in the operating environment that **must be true at the start** of the service (before it can be validly invoked). |
| **Postcondition (Effect)** | Conditions that are **made true via the execution** of the service (the outcome, whether desired/goal or merely collateral). |
| **Assumption** | Conditions the service **relies on being true**, but which **cannot be evaluated in advance (a-priori)**. |

**Understanding assumptions in more depth:**
- A service is sometimes invoked *contingent* on certain assumptions holding, even though there's no way to check them beforehand.
- **If an assumption later turns out to be false/incorrect**, the correct behaviour is to **abort and roll back** the service execution — you can't simply continue as if nothing happened.
- This raises a composition-level question: **how do we ensure assumptions are properly managed when services are composed together?** Specifically, we need to **ensure consistency of assumptions** across all the services being composed — if Service A assumes X is true and Service B assumes X is false, composing them creates a logical inconsistency that could cause failures.
- **Classic real-world example of an assumption: the FORCE MAJEURE clause** in contracts — a service (or contract) implicitly assumes "no extraordinary/unforeseeable event (natural disaster, war, etc.) occurs"; if that assumption is violated, obligations may be excused/rolled back rather than enforced as normal.

> 💡 **Precondition vs. Assumption — what's the difference?** A precondition *can* be checked before invoking the service (it's evaluable a-priori). An assumption *cannot* be checked in advance — you only find out it was false *after* something goes wrong, which is precisely why it needs a rollback/abort mechanism rather than an upfront validation check.

### 3.3 Quality of Service (QoS)

**Definition:** QoS specifications provide a **measure of the effectiveness** of a business service — i.e., not just *whether* it achieves its goal, but *how well*.

- QoS specifications are **constraints describing operational aspects** of service quality.
- QoS factors can be described **qualitatively** (e.g., "high reliability") or **quantitatively** (e.g., "99.9% uptime").
- Formally represented as a **set of `<QoS-factor, range>` pairs**, where the range gives the upper/lower bounds for quantitative factors, or a qualitative value/label otherwise.

> **Examples of QoS factors:** `<response-time, ≤ 2 seconds>`, `<availability, ≥ 99.9%>`, `<cost, $0.01 per call>`, `<reliability, "high">`.

### 3.4 Delivery Schedules and Payment Schedules

| Concept | Representation | Meaning |
|---|---|---|
| **Delivery schedule** | Set of `<functionality, deadline>` pairs | Specifies *when* each piece of functionality must be delivered. |
| **Payment schedule** | Similar representation to delivery schedules | Specifies *when* payments are due, tied to milestones/functionality delivered. |

> **Example:** `<baggage-located, within 48 hours>` is a delivery-schedule entry; `<50% deposit, on-order-confirmation>` and `<remaining balance, on-delivery>` are payment-schedule entries.

### 3.5 Penalties

**Definition:** Specified as a set of **`<condition, amount>`** pairs. Given a condition **C**, a penalty **P** is invoked as **reparation** if condition **C** becomes true (i.e., something goes wrong or a term is violated).

> **Example (from the lecture):** *"If paint is spilled on the carpet, then the penalty is the cost of cleaning the carpet."* → `<paint-spilled-on-carpet, cost-of-cleaning>`.

---

## 4. Service Composition

Illustrated using a **Travel Service** example.

### 4.1 Commonly Occurring Functionalities in a Travel Service
- Airline ticket booking
- Airport transfer booking
- Hotel booking
- Tour booking
- Theatre ticket booking

If each of these is available as a separate service (each possibly atomic, or itself a composite service), a **composite "travel service"** can be built by composing them.

### 4.2 Specifying the Composite Service
**Functional requirements** (what must be jointly true — a conjunction of goals from the constituent services):
```
air-ticket-booked AND airport-transfer-booked AND hotel-booked
AND tour-booked AND theatre-booked
```

**Non-functional requirements** (constraints over the aggregated QoS of the constituents):
```
Σ cost < BUDGET
Σ time < DEADLINE
```

> 💡 **The core insight:** a composite service isn't just "call these services one after another." It has to satisfy a **combined functional goal** (all sub-goals achieved) *and* **combined non-functional constraints** (aggregated cost, time, etc. still within limits). This is exactly why BSRL's QoS/schedule/penalty machinery matters at the composition level — you need a formal way to *sum up* and *check* these constraints across multiple services, not just describe one service in isolation.

---

## 5. What Do We Do With Service Models? (Applications)

Once services are formally modelled (using something like BSRL), the models themselves become valuable organizational assets, used to:

1. **Maintain a clear understanding of enterprise/system capabilities and know-how**, via:
   - **Service catalogues** — a browsable inventory of what services the organization has.
   - **Intellectual property (IP) asset repositories** — treating well-defined services as protectable/valuable IP.
   - **Enterprise architectures** — situating services within the broader IT/business architecture (previews Lecture 6).

2. **Dynamically generate functionality** — e.g., to handle exceptional situations, by composing existing services on-the-fly rather than hand-coding every scenario in advance.

3. **Analyze compliance** — checking whether services/processes actually adhere to rules, regulations, or contracts (previews Lecture 10, "Service compliance management").

4. **Strategic alignment analysis:**
   - *Do we have services to realize all of our enterprise strategies?* (gap analysis — are there strategic goals with no supporting service?)
   - *Why do we support certain services?* — answered by pointing to which strategies each service supports (traceability from service → business strategy).
   - **Enterprise re-engineering/rationalization** — identifying *redundant* services (multiple services doing the same thing, candidates for consolidation).

---

## 6. Worked Exercise: Lost Baggage Claim Service (Airport), Modelled in BSRL

*(The original lecture poses this as a pen-and-paper exercise: "Use BSRL to specify a 'Lost Baggage Claim Service (Airport)'." Below is a fully worked model, applying every BSRL element covered above — useful as a template for how to answer similar exercises.)*

**Service name:** Lost Baggage Claim Service (Airport)

**Goals:**
- *Achieve*: `baggage-returned-to-owner` **OR** `compensation-paid-to-owner` (the service succeeds if either outcome is reached).
- *Maintain*: `passenger-kept-informed` — the passenger's claim status should remain visible/updated throughout the process (a maintenance goal, not a one-off achievement).

**Preconditions:**
- Passenger holds a valid baggage claim tag / boarding pass.
- The missing baggage has been reported within the airline's required reporting window (e.g., within 24 hours of flight arrival).
- Passenger has provided valid identification and contact details.

**Postconditions (Effects):**
- A formal claim record is created in the airline's baggage-tracking system. *(This is a collateral postcondition — it always happens, whether or not the baggage is actually found — as distinct from the desired goal above.)*
- Either: baggage is located and delivered to the passenger, **or** the baggage is confirmed lost and a compensation case is opened.

**Assumptions:**
- The airline's baggage-tracking / RFID scanning system is fully operational (cannot be verified in advance — if it turns out to be down, the claim process must be aborted/escalated to manual investigation and any downstream steps rolled back).
- Connecting-flight baggage-handling records (for transit passengers) are accessible and accurate.
- The passenger's supplied contact details are correct (if not, status updates cannot reach them — again, not verifiable up front).

**Quality of Service (QoS):**
- `<claim-lodgement-response-time, ≤ 30 minutes>`
- `<case-resolution-time, ≤ 5 business days>`
- `<service-availability, 24/7>`
- `<tracking-accuracy, ≥ 95%>`

**Delivery Schedule:**
- `<initial-status-update, within 24 hours of claim lodgement>`
- `<baggage-delivered-or-compensation-offer, within 5 business days>`

**Payment Schedule:**
- `<interim-compensation-payment, within 7 days of confirmed loss>`
- `<final-settlement-payment, within 21 days of confirmed loss>`

**Penalties:**
- `<baggage not located within 21 days, full compensation up to carrier liability limit>`
- `<baggage found damaged during airline storage, cost of repair or replacement>`

---

## 7. Key Takeaways / Review Checklist

- [ ] I can list the three essential ingredients of a service description (functionality, invocation/output info, QoS).
- [ ] I can name the three classic web service standards and what each one covers (WSDL = description, SOAP = invocation, UDDI = discovery).
- [ ] I can name the three semantic web service languages (OWL-S, WSMO, WSDL-S) and explain the common **IOPE** pattern they follow.
- [ ] I can explain why postconditions and goals are described separately (collateral vs. desired effects).
- [ ] I can name and give an example of the three basic goal types: **achieve, maintain, avoid** — plus explain why more complex (temporal/periodic) goals need temporal logic.
- [ ] I can distinguish **precondition** vs. **postcondition/effect** vs. **assumption**, and explain why assumptions require rollback rather than upfront checking.
- [ ] I can represent QoS, delivery schedules, payment schedules, and penalties in their `<...>` pair notations.
- [ ] I can explain the travel-service composition example, including both its functional and non-functional requirements.
- [ ] I can list at least 3 organizational uses of service models (catalogues, compliance, strategic alignment, etc.).
- [ ] I could model a new, unseen service end-to-end in BSRL (goals, conditions, assumptions, QoS, schedules, penalties) — see the worked Lost Baggage example as a template.
