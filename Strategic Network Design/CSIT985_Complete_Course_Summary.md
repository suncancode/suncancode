# Strategic Network Design Technology  
Lecturer: Dr. Chau Nguyen  
Reference: McCabe, *Network Analysis, Architecture and Design (3rd ed.)*

---

## 1 – Introduction & Strategic Planning
**Focus:** Establishing the purpose and scope of network design.

### Key concepts
- Strategic planning aligns network goals with business objectives.
- Planning questions: purpose, leadership commitment, cost/time.
- Planning team: includes technical, managerial, and financial rolse.
- Approaches:
  - **Top-down:** From business goals -> technical requirements.
  - **Bottom-up:** From existting technologies -> improvements.
  - **PPDIOO:** Prepare, Plan, Design, Implement, Operate, Optimize.
  - **Eight-Step McCabe Process:** Similar, with emphasis on analysis & architecture.

### Key words
Purpose - People - Process - Planning - Protocols

---

## 2 - Networking Fundamentals
**Focus:** Review of essential networking knowledge.

### Key concepts
- **OSI & TCP/IP models:** 7 layers <->  4 layers.
- **Network types:** LAN, MAN, WAN, PAN.
- **Topology:** Bus, Ring, Star, Mesh, Tree.
- **Protocols:** TCP (Reliable), UDP (real-time), HTTP, FTP, SMTP.
- **Devices:** Router, Switch, Hub, Access Point.

---

## 3 - Strategic Network  Design & Requirement Concepts
**Focus:** Understandiing how strategic needs translate to technical requirements.

### Key Concepts
- Strategic design = long-term alignment between IT and business.
- **Requirement Flow:** User -> Application -> Device -> Network.
- **Requirement Types:**
  - User: business-level needs.
  - Application: delay, capacity, QoS.
  - Device: capability and interface topology.
  - Network: protocols, routing, topology.
- **Change Strategies:**
  1. Rational-Empirical
  2. Normative-Reeducative
  3. Power-Coercive
  4. Environmental-Adaptive

---

## 4 - Requirement Analysis Process
**Focus:** Turning abstract needs into measurable requirements.

### The 5-step Process
1. Gather requirements
2. Develop service metrics
3. Characterise behaviour
4. Develop detailed requirements
5. Map requirements (to topology & geography)

### Service Metrics
- **Capacity, Delay, Reliability, Maintainability, Availability (RMA).**
- Formula: A = MTBF / (MTBF + MTTR)
- Delay thresholds:
  - Interaction delay: 10-30s
  - Human Response Time: ~100ms

### Mapping
Visualise where services, devices, and data flow reside (LAN, MAN, remote).

---

## 5 - Flow Analysis
**Focus:** Understanding how data moves through the network.

### Key concepts
- **Flow:** Stream of traffic between source & destination.
- **Flow Types:** Individual, Composite, Critical.
- **Flow Models:** 
  - Peer-to-Peer
  - Client-Server
  - Hierarchical Client-Server
  - Distributed
- **FlowSpec Algorithm:** Combines requirements.
  - One-Part (Best Effort)
  - Two-Part (Predictable)
  - Multi-Part (Guarenteed)

---

## 6A - Network Architecture
**Focus:** Designing the logical structure of the network.

### Types of Architecture
- **Component Architecture:** Addressing/Routing, Performance, Security, Management.
- **Reference Architecture:** Intergration of all components.

### Architecture Models
- Topological (Access-Distribution-Core)
- Flow-based
- Functional (Service-Provider, End-to-End)

### Internal Relationships
- **Trade-offs:** performance vs manageability.
- **Dependencies:** QoS depends on SLA and routing.
- **Constraints:** protocol limits or hardware capacity.

---

## 6B - Security & Privacy Architecture
**Focus:** Incorporating protection and policy into the design.

### CIA Triad
- **Confidentiality**  - Only anthorised users access data.
- **Integrity** - Data remains unaltered.
- **Availability** - Resources available when required.

### Process
Threat Analysis -> Risk Assessment -> Policy Development -> Mechanisms

### Mechanisms
- IPSec, SNMPv3, NAT, Firewalls, DMZ, Encription/Decryption.
- Trade-offs: stronger security may reduce performance.

---

## 7 - Network Addressing & Routing
**Focus:** Logical communication and addressing principles.

### Concepts
-  IP addressing and subnetting (VLSM).
- Routing protocol: Static, RIP, OSPF, EIGRP, BGP.
- Policy-based routing, redundancy, and failover design.

---

## 8 - Network Performance
**Focus:** Ensuring measurable service levels.

### Key concepts
- **Capacity, Delay, RMA (Reliability, Maintainability, Availability).**
- **QoS Mechanisms:**
  - DiffServ (per-hop behaviour, scalable)
  - IntServ (per-flow reservation)
- **Resource Control:**
  - Traffic classification, metering, shaping, dropping.
  - Scheduling: WFQ, RED, FIFO.
- **SLAs & Policies:** define performance guarantees between provider & user.

---

## 9 - Network Management
**Focus:** Controlling, monitoring, and maintaining the network.

### Architecture Layers
1. Business Management
2. Service Management
3. Network Management
4. Element Management
5. Network-Element Management

###  Protocols & Mechanisms
- **SNMP v3** - monitoring and configuration.
- **MIB (Management Information Base)** - data structure of monitored parameters.
- **FCAPS Model** - Fault, Configuration, Accounting, Performance, Security.

### Management Styles
- In-band, Out-of-band, Hybrid.
- Keep management traffic under 5-10% of total bandwidth.


---

## 11 - Network Design
**Focus:** Converting architecture into deployable design.

### Design Process
1. Vendor and service-provider evaluation
2. Develop goals & criteria (primary/secondary)
3. Choose technology & architecture
4. Create network layout (logical & physical)
5. Maintain traceability from requirement -> design.
6. Define design metrics

### Concept Elements
- Scalability - growth limits, segment rules.
- Dependability - availability, recoverability, fault tolerance.
- Security - rules per network zone.
- Compatibility, Flexibility, Simplicity.

---

## 12 - Advanced Networking Technologies
**Focus:** Modern and future trends in network design.

### Software-Defined Networking (SDN)
- Separation of **Control Plance** and **Data Plane**.
- Centralised **SDN Controller** using OpenFlow.
- Programmable, dynamic management.

### SD-WAN
- Extends SDN principles to WANS.
- Improves cloud connectivity and cost efficiency.

### Network Function Virtualisation (NFV)
- Converts network devices into software (VNF).
- Managed by **MANO (Management and Orchestration).**

### Network Automation
- Automates configuration, monitoring, and updates.
- Tools: Ansible, Puppet, Python scripting.

### Machine Learning in Networking
- Predicts traffic and link quality
- Enables smart routing, anomaly detection, QoS optimisation.


