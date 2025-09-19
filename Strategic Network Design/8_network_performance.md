# Network Performance

---

## 1. Definition
- Performance is the set of levels for capacity, delay, and RMA in a network. It is usually desirable to optimize these levels, either for all (user, application, and device) traffic flows in the network, or for one or more sets of traffic flows, based on groups of users, applications, and/or devices.

- **Components**:
  - `Controlling traffic inputs` (admission and rate controls).
  - `Adjusting baseline` performance (traffic or capacity engineering).
  - `Controlling the network` for specific services (prioritizing scheduling, conditioning).
  - `Implementing feedback loops` to users, applications, devices, and management.

## 2. Developing Goals for Performance
- **Process**: Begin during the requirements phase; users requirements, flow specifications, and maps and inputs.

- **Considerations**:
  - Performance is desirable but must be necessary and sufficient.
  - Key questions:
    - Are mechanisms necessary?
    - What are we solving, adding, or differentiating?

- **Approach**: Smart simple-implementation; ensure customer needs and maintainance.

- **Objectives**: 
  - Improve overall performance.
  - Support specific groups.
  - Enhance profitability.
  - Merge traffic types.
  - Differentiate services.

- **Types**: `Single-tier` (all flows) or `Multi-tier` (specific groups).

- **Goal settings**: Define levels (e.g., bandwidth for real-time voice/video via QoS or overbuilding).

---

## 3. Performance Mechanisms
### 3.1 Quality of Service (QoS)
- Determines, sets, and acts on traffic priority levels.
- Includes `IP QoS` (ToS), `ATM Cos`, `Frame Relay CIR`.

- **IP QoS**:
  - *DiffServ*: 
    - Aggregates flows per-hop.
    - Scalable.
    - Classes: Best-effort.
    - Assured Forwarding (AF), Expedited Forwarding (EF).
    - Uses DSCP.
  - *IntServ*: 
    - End-to-end for individual flow.
    - Uses RSVP bandwidth reservation.
  - *MPLS*: 
    - Ensures packets follow the samne route.
    - Supports QoS and SLAs.
    - Uses LER and LSR for hardware-based routing.
  - *Comparison*:
  | Feature          | DiffServ         | IntServ          |
  |------------------|------------------|------------------|
  | Scalability      | Large networks   | Small/medium     |
  | Granularity      | Aggregated       | Per-flow         |
  | Scope            | Per-hop          | End-to-end       |

### 3.2 Resource Control
- **Prioritization**: Ranks based on importance (e.g., protocol, port).

- **Traffic Management**: Admission control, traffic conditioning (classification, metering, shaping, dropping).

- **Scheduling**: Orders traffic.

- **Queuing**: Stores packets (FIFO, Priority, CBQ, WFQ, RED, WRED).

### 3.3 Service Level Agreements (SLAs)
- Formal contracts defining provider responsibilites (e.g., data rate, delay, availability).

### 3.4 Policies
- Links management views with QoS and SLAs.
- Defines resource access and permissions.

---

## 4. Architectural Considerations
- Evaluate against requirements, goals, and environment.

- **Internal**: Trade-offs between end-to-end vs. per-hop, individual vs. aggregated flows.

- **External**: 
  - With Addressing/Routing: Coupled with DiffServ/MPLS.
  - With Network Management: Configures, monitors, bills performance.
  - With Security: Reduces capacity/delay; compensation needed.

  