# Advanced Networking Technologies

---

## Outline
- **Software-Defined Networking (SDN)**
- **Software-Defined Wide Area Network (SD-WAN)**
- **SDN and Big Data**
- **Network Automation**
- **Network Function Virtualization (NFV)**
- **Machine Learning (ML)**

---

## 1. Software-Defined Networking (SDN)
### Challenges Before SDN
- High demand for massive data transmission during unexpected flow increases.
- Inflexible network structure.
- Issues: Network sustainability, uncontrollability, and secuirty.
- Implementation of new technologies increases complexity and cost.

### What is SDN?
- **SDN** (Software-Defined Networking): A paradigm to redesign the Internet.
- Core technology: **OpenFlow** protocol, developed by Stanford University in 2008.

### Why SDN?
- Addresses limitations of traditional networks with a flexible, programmable approach.

### SDN vs. Traditional Network
- **Features**:
  - Separation of *control plane* and *data plane* for independent evolution.
  - Centralized control via an external *SDN Controller* or *Network Operating System (NOS)*/
  - Network programmability through software applications.
  - Flow-based forwarding rules instead of destination-based decisions.

### Application Plane
- Hosts network services and applications.
- Accesses global network view, uses high-level programming to execute functions via the control plane.
- Provide APIs for communication with other planes.

### Control Plane
- Differs from traditional control:
  - Programs data plane elements with standard interfaces.
  - Runs on separate hardware.
  - Manages multiple data plane elements from a single instance.
- **Roles**:
  - Manages infrastructure and implements policies via *southbound interface*.
  - Provides network view to the application layer via *northbound interface*.
- **SDN Controller**: Core of architecture, includes applications, NOS, network abstraction, and APIs (northbound: RESTful, Ad Hoc; soundbound: OpenFlow, ForCES; east-west: inter-controller communication).

### Data Plane
- Comprises virtual and physical SDN devices.
- Functions: Forwards traffic based on controller rules, gathers network state.

### SDN Featured Applications
- Network management, SDN virtualization for cloud computing, SD-WAN.

### Challenging Issues
- Non-standard northbound interface, security, QoS, distributed controllers, IoT integration.

---

## 2. Software-Defined Wide Area Network (SD-WAN)
- **WAN**: Wide Area Network connecting multiple LANs.
- **SD-WAN**: Sofrware-based approach for enhanced WAN management.

### Benefits
- Improved application experience, enhanced security, optimized cloud connectivity, simplified management.

---

## 3. SDN and Big Data
### Big Data
- Involves storing and processing large datasets with 5Vs: volume, variety, velocity, value, and veracity.

### SDN Features for Big Data
- Highlights SDN benefits for big data applications.

### Big Data benefits for SDN
- Traffic engineering, cross-layer design, security attack mitigation, intra/inter-data-center networks.

### Open Issues
- Scalable controller management, intelligent flow table management, flexible language abstraction, wireless mobile big data.

---

## 4. Network Automation
- Automates configuration, management, testing, deployment, and operation of network devices.

### Traditional vs. Automated Network
- Traditional: Manual, error-prone, time-consuming.
- Automated: Reduced errors, improves efficiency, ensures scalability and policy compliance.
- Tools: SDN, Ansible, Puppet, Python scripts.

---

## 5. Network Function Virtualization (NFV)
- **NFV**: Virtualizes network functionss on standard hardware (servers, switches, storage)/
- **VNF**: Virtual Network Function, the virtualized network function.

### NFV Features
- Virtualizes and chains network functions, decouples them from physical devices, enables on-demand execution.

### NFV Architecture
- Includes NFV infrastructure, VNFs, and NFV Management and Orchestration (MANO).

### Relation of SDN and NFV
- SDN and NFV complement each other in network design.

---

## 6. Machine Learning (ML) in Networking
- **ML**: Subsets of AI, enables systems to learn and predict based on experience.
- Applications: Image recognition, communication networks.

### AI, ML, and DL
- **AI**: General intelligence.
- **ML**: Machine Learning.
- **DL**: Deep learning.
- Workflow: Data collection, model training, deployment.
- Categories: Supervised, unsupervised, reinforcement learning.

### ML-Based Applications
- Predict models: Signal-to-noise ratio, next node, link quality, traffic volume, 5G revenue.
- **IDS**: Intrusion Detection System using historical data.
- **Routing**: DL-based routing for optimal paths.
- **QoS**: Maximizes throughput, reduces delay, improves QoE.
- **Resource Management**: Allocates resources (switches, bandwidth)/

### Challenges and Future trends
- High computaional lead, data privacy, imbalanced datasets, real-world testing, hybrid algoritms, 5G/6G advancements.