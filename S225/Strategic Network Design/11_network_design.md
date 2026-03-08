# Network Design

---

## Outline
- **Design Process**
- **Vendor, Equipment, and Service-provider Evaluations**
  - Developing Goals
  - Developing Criteria for Technology Evaluations
  - An Architectural Approach to Network Design
  - Network Architecture Design Elements
  - Guidelines and Constraints
  - Making Technology Choices for the Design
- **Network Layout**
- **Design Traceability**
- **Design Metrics**

---

## 1. Design Process
- **Network Design**: Culmination of **Network Analysis** and **Network Architecture**.
- Includes evaluations of vendors/equipment/service-providers and network layout.

### Design Products
- **Network Blueprints**: Physical specs (device locations, connections, security).
- **Component Plan**: Mechanism and interactions for functions.
- Vendor/equipment/service-provider selections, traceability, and metrics.

---

## 2. Vendor, Equipment, and Service-provider Evaluations
### Evaluation Process
- Goal: Choose the best candidates based on technocal fit, price, reputation, and backup resources.
- **Seeding Process**: Collect documentation, set evaluation rules.
- **Candidate Discussions**: Informal communication aids but must be monitored for transparency.
- **Data Gathering**: Refine plans through discussions, ensure fairness.
- **Rating Development**: Objective criteria: Cost (20%), Technology (30%), Performance (30%), Risks (10%), Scalability (10%).
- **Prioritization**: Compare and rank proposals independently.
- **Modifying Candidates**: Adjust based on results.

---

## 3. Developing Goals
### Common Goals
- Optimize deployment/operation costs, security (maximize, customize, multiple models), performance, ease of use, adaptability, supportability.
- Trade-offs: Security vs. cost, performance vs. cost.
- Initial conditions: New network are free, upgrades constrained.
- Flow analysis: Indicates high-performance, traffic consolidation, capacity planning.
- Prioritization varies by network area; users may need negotiation.

### Trade-offs
- Results in prioritized goals: Primary (overrides) and secondary (support) goals.

---

## 4. Developing Criteria for Technology Evaluation
- Use design goals as criteria: Minimize costs/ease of use, maximize performance (capacity, RMA), ensure adaptability (dynamic reconfiguration).
- Evaluate against reference architecture and flowspecs.

---

## 5. Design Criteria
- Explicit goals for project success, used for recommendations and evaluations.
- **Primary Criteria**: Essential for success.
- **Secondary Criteria**: Desirable but sacrificable.
- Guidelines: Specific, avoid vague language, use bulleted lists or tables.

---

## 6. An Architectural Approach to Network Design
### Concepts
- Defines technologies, protocols, capabilities, and segment interconnections, not detailed design.
- Supports conceptual design, aligns with business strategy.

### Major Considerations
- Conceptual design, business characteristics, competition, customer channels, technology trends, user types, security policy, geographic reach, applications, capacity analysis.
- Ensures alignment with current/future business needs.

### Outcomes
- Design directions, architecture diagrams, high-level topology, protocols.

---

## 7. Network Architecture Design Elements
### Categories
- **Concept Elements**: Business environment, technology, scalability, dependability, security, management, compatibility, limitations, flexibility, distribution, optimization, risks, performance, simplicity.
- **Technology Elements**: Nodes, links, topology, interfaces, services, protocols, traffic mapping.

---

## 8. Guidelines and Constraints
### Predictable/Guaranteed Requirements
- Restrict to technologies supporting stable RMA, capacity, delay (QoS, DiffServ, IntServ).
- Must determine state, allocate, prioritize, bill, handle over-demand; configure buffers, I/O, CPU.

### Multipart Flowspecs
- Plan capacity per flow, evaluate scalability; best-effort 60%, predictable 80% or higher, adjust for burstiness.

### Constraints
- Costs, pre-existing networks, facility implications.

---

## 9. Making Technology Choices
### Method
- Segment network, use black box method, apply criteria/guidelines per area.
- Segmentation based on geography, user concentration, flow hierarchy, functions (WAN, NAP, core, specialized, general).

---

## 10. Network Layout
### Factors
- Topology, technology, vendor choices, strategic locations; develops logical diagrams, blueprints, component plans.

### Logical Diagram
- Shows connectivity and relationships, prioritizes logic over physical accuracy.

### Network Blueprints
- Details physical aspects (devices, cables, security) to scale.

### Strategic Locations
- Boundary points, monitoring/management areas, QoS zones, router interfaces, multifunction areas.
- Reference standards like TIA 942.

### Component Plans
- Separates functions (VoIP, security, VPN) as needed.

---

## 11. Design Traceability
### Concept
- Links analysis, architecture, and design decisions for transparency and defensibility.

---

## 12. Design Metrics
### Measurement
- Measures capacity, delay, RMA, and user/device requirements.
- Summarizes performance in an SLA-like document.