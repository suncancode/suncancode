# Network Management 

---

## Outline
- **Network Management Architectures**
- **Network Devices and Characteristics**
- **Network Management Mechanism**
  - Monitoring Mechanisms
  - Instrumentation Mechanisms
  - Configuration Mechanisms
- **Architectural Considerations**
  - In-band and Out-of-band management
  - Centralized, distributed, and hierarchical management
  - Scaling network management traffic
  - Check and balances
  - Management of Network Management Data
  - MID selection
  - Internal relationships
  - External relationships

---

## 3. Network Management Architectures
- **Functions**: Control, Plan, Allocate, Deploy, Coordinate, Monitor network resources.

- **Areas to Address**:
  - Deciding which network management protocol.
  - Reconfiguring the network for changing requirements.
  - Testing service-provider compliance with SLAs and policies.
  - Proactive monitoring.
  - Implementing high-level asset management.

- **Structure Coverage**:
  - *Business Management*: Budgets, resources, planning, agreements.
  - *Service Management*: Access bandwidth, data storage, application delivery.
  - *Network Management*: All devices across the network.
  - *Element Management*: Collections of similar devices (e.g., access routers).
  - *Network-Element Management*: Individual devices (e.g., single router).
  - *Multi-Layer Structure*: From abstract policies (Business) to concrete components and parameters. (Network-Element).

- **Two basic functions**:
  - Transport of management information across the network -> (SNMP).
  - Management of network management information elements -> MIB (Management Information Base).

- **Four Categories of Network Tasks**:
  - Monitoring for event notification, or for trend analysis and planning.
  - Configuring network parameters.
  - Troubleshooting the network.
  - Planning.

---

## 4. Network Devices and Characteristics
### Network Device
An individual component of the network that participates at one or more layers of the protocol (e.g., end devices, routers, switches, hubs,...).
- Management of network devices includes:
  - Network planning.
  - Initial resource allocation.
  - FCAPS model from the telecommunication network management: fault, configuration, accounting, performance, security management.

### Network characteristics
- **End-to-end**: (Availability, capacity, delay, jitter, throughput, error,...)
  - Can be measured across multiple network devices in the path of one or more traffic flows.
  - May be extended across the entire network or between devices.
- **Per link/network/element characteristics**:
  - Specific to the type of element or connection between elements.
  - May be used individually or combined to form an end-to-end characteristics.
  - Per link: Propagation delay, link utilization.
  - Per element: IP forwarding rates, buffer utilization.

### Network Management:
- Network planning, resource allocation.
- FCAPS model: Fault, Configuration, Accounting, Performance, Security.

---

## 5. Network Management Mechanisms
- **Protocols**:
  - SNMP: Collect/configures parameters, sends traps (SNMPv3: secure, block retrieval).
  - CMIP/CMOT: Historical, more complex than SNMP.

- **MIB** (Management Information Base):
  - Defines managed objects/variables (not a database, an abstraction).
  - MIB-II: Monitors iflnOctets, ifOutOctets, iflnErrors, etc.

- **Mechanisms**:
  - Monitoring: Collect end-to-end/per-link characteristics.
  - Intrumentation: Tools (SNMP, ping, Nagios).
  - Configuration: Set parameters (CLI, remote, file downloads).

### Monitoring Machanisms
- **Components**:
  - Collection: Polling devices.
  - Processing: Event notification or trend analysis.
  - Display: Tables, graphs, logs, alarms on VDU.
  - Archiving: Store data for analysis.

- **Event notification**:
  - Event: Errors, threshhold crossing, upgrades.
  - Real-time analysis with short polling (trade-off: resource intensive).

- **Trend Analysis**:
  - Long-term behavior, establish baselines (availability, delay, utilization).

- **Tools**: CLI Nagios, Zabbix, ICMP (ping).

### Intrumentation Mechanisms:
- **Tools**: Ping, traceroute, TCPdump, Telnet, FTP.
- **Requirement**:
  - Accuracy: Collect from multiple points.
  - Dependability: Separation, replication.

### Configuration Mechanisms
- **Methods**: Direct access, remote access, download configuration files.

---

## 6. Architectural Considerations:
- **Key Decisions**:
  - Characteristics to monitor, intrumentation, display, storage duration.
  - FCAPS model for management.

### Considerations
- **In-band vs. Out-of-band**:
  - *In-band*: Uses same network paths, affected by user traffic issues.
  - *Out-of-band*: Separate path, secure but costly.
  - *Hybrid*: Combines both for balance.

- **Centralized, Distributed, Hierarchical**:
  - *Centralized*: Single system, simple but single point of failure.
  - *Distributed*: Multiple systems, redudant but costly.
  - *Hierarchical*: Distributed functions across platforms, scalable.

- **Scaling Traffic**: Keep management traffic <2-5% LAN, 1 device per WAN-LAN interface.

- **Checks and Balances**: Duplicate measurements for accuracy.

- **Data Management**: Local for events, archival at night, include metadata (datatype, timestamp).

- **MIB Selection**: MIB-II for basic health, enterprise MIB for servers/users.

- **Internal Relationships**:
  - Northbound interface (SNMP, CORBA, HTTP) to OSS.
  - Dependencies: Data flows rely on network capacity/reliability.

- **External Relationships**:
  - Addressing/Routing: Management depends on routing, defines domains.
  - Performance: Measures performance, but management traffic adds overhead.
  - Security: Security polocies may impede management flows.
  