# CSIT985 - Week 7: Network Addressing and Routing

---

## 1. Introduction to Network Addressing and Routing
- **Concepts**:
  - Addressing: Assigns unique identifiers to devices (e.g., IP addresses).
  - Routing: Determines data paths across networks.
  
- **Role**: Connects architecture (Week 6A) to design, supports flows (Week 5) like HD/4K video.

- **Relationship**: Addressing influences routing; both optimize based on requirements (e.g., low latency <50ms).

---

## 2. Addressing Components
- **Composition**:
  - Format: IPv4 (32-bit, e.g., 198.51.100.0/24), IPv6 (128-bit).
  - Classification: Public, Private, Multicast.
  - Assignment: Static, Dynamic (DHCP), Auto-configuration (SLAAC).

- **Key Components**:
  - Subnetting: Divides network into sub-networks.
  - Address Resolution: IP to MAC (ARP).
  - NAT: Translates addresses for external access.

- **Relationships**:
  - Tradeoffs: Subnetting improves management but adds complexity.
  - Dependencies: NAT relies on routing tables.
  - Constraints: IPv4 limited to 4.3 billion addresses.

---

## 3. Routing Components
- **Composition**:
  - Mechanisms: Routers use routing tables.
  - Protocols: Static, Dynamic (OSPF, BGP).
  - Types: Interior (IGP), Exterior (EGP).

- **Key Components**:
  - Path Selection: Chooses routes based on metrics (hop count, bandwidth).
  - Load Balancing: Distributes traffic for spikes.
  - Convergence: Updates routing tables on changes.

- **Relationships**:
  - Tradeoffs: Dynamic routing is flexible but resource-intensive.
  - Dependencies: Routing requires correct addressing.
  - Constraints: BGP is complex, needs expertise.

---

## 4. Optimization and Design Considerations
- **Optimization**:
  - Addressing: Use IPv6 for scalability, efficient subnetting.
  - Routing: Select OSPF/BGP for flows, reduce delay <50ms.

- **Design Considerations**:
  - Hierarchical Design: Access → Distribution → Core.
  - Redundancy: Backup routes for 24/7.
  - Security: Encrypt routing (e.g., OSPF authentication).

- **Implementation**: Use PPDIOO (Plan, Design, Implement, Operate).
