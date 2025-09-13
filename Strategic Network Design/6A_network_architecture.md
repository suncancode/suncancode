# CSIT985 - Week 6A: Network Architecture

---

## 1. Introduction to Architecture and Design
- **Architecture vs. Design**:
  - Architecture: Broad, generalized, independent; focuses on relationships between network functions.
  - Design: Focused, in-depth, dependent; focuses on specific technologies and equipment.

- **Role**: Bridge between analysis (requirements, flows) and implementation. Solves nonlinear problems by balancing top-down (requirements) and bottom-up (components).

- **Multidimensional**: Addresses security, performance, management in a 3D approach.

- **Process Model**: Input (requirements, flows) → Components → Models → Reference Architecture.

---

## 2. Component Architectures
- **Composition**: Functions (main capabilities), Mechanisms (hardware/software), Internal Relationships (tradeoffs, dependencies, constraints).

- **Key Components**:
  - Addressing and Routing: Assign identifiers, learn connectivity (mechanisms: routers, protocols).
  - Network Management (NM): Monitoring, configuring (FCAPS model; mechanisms: centralized/distributed).
  - Performance: Capacity, delay, RMA (mechanisms: QoS, SLA).
  - Security: Confidentiality, integrity (mechanisms: firewalls, encryption).

- **Internal Relationships**:
  - Tradeoffs: e.g., Centralized NM easier but failure-prone.
  - Dependencies: e.g., QoS depends on SLA.
  - Constraints: e.g., RIP limited for large hierarchies.

- **Optimizing**: Support high-priority flows; link requirements → flows → architecture.

---

## 3. Reference Architectures
- **Definition**: Complete network architecture integrating all components, with internal (within components) and external relationships (between components).

- **Combining Components**: Balance priorities (e.g., low delay requires adjusting NM/security).

- **Optimizing Tradeoffs**:
  - Performance & Security: Inspection increases delay.
  - NM & Security: NM access creates vulnerabilities.
  - NM & Performance: In-band NM impacts user data.
  - Addressing & Performance: Coupled routing adds complexity.

---

## 4. Architectural Models
- **Topological Models**: LAN/MAN/WAN (geographic); Access/Distribution/Core/DMZ (functional – Access generates flows, Distribution aggregates, Core transports, DMZ for external).

- **Flow-based Models**: Peer-to-peer, Client-server, Hierarchical client-server, Distributed computing.

- **Functional Models**: Service-provider (delivery), Intranet/Extranet (secure access), End-to-end (full path).

- **Recipe**: Start with topological, add flow/functional for complete reference architecture.