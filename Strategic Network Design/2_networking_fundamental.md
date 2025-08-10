###########################
# NETWORKING FUNDAMENTAL  #
###########################

---

## 1. Network Elements
### Definition 
A computer network consists of two or more "END DEVICES" (hosts) connected via wired or wireless links.

- *End devices*: e.g., computers, servers, or IoT devices that initiate or receive data.

- *Intermediate Devices*:
    + `Hub`: Connects devices, broadcasts data to all ports.
    + `Switch`: Connects devices in a LAN, forwards data based on MAC address.
    + `Router`: Routes data between networks based on IP addesses.
    + `Bridge`: Connects network segments, reduces congestion.
    + `Gateway`: Translates protocols between different networks.
    + `Modem`: Converts digital to analog signals.
    + `Repeater`: Amplifies signals to extend transmission distance.
    + `Access Point`: Enables wireless connectivity.

- *IP Addresses*:
    + `IPv4`: 32-bit (e.g., 10.10.10.1).
    + `IPv6`: 128-bit (e.g., 2345:0425:2CA1:0000:0000:0567:5673:23b5).

- *Transmission Media*:
    + Copper wires (twisted pair, coaxial cables).
    + Optical fiber (high speed, long distance).
    + Wireless connection.

---

## 2. Network Categories

- `LAN` (Local Area Network): Small-scale network  (e.g., office, building), high speed, low cost.

- `MAN` (Metropolitan Area Network): City-wide network, connects multiple LANS.

- `WAN` (Wide Area Network): Large-scale network (e.g., Internet), connects geographically distant area.

- `The Internet`: Global network connecting billions of devices using TCP/IP.

---

## 3. Network Architecture

- `Cloud-based Network`: Resouces and data hosted on remote services (e.g., Dropbox, Google Drive).

- `Distributed Network`: Computers manage local resources and can operate independently.

- `Peer-to-Peer Network`: Devices have equal status, no central server, suitable for small networks.

- `Hybrid Network`: Combines multiple architectures for flexibility and efficiency.

---

## 4. Network Topology

Topology defines how network elements are interconnected. 5 Common LAN topologies:
- `Mesh`: Multiple direct links between devices.
    + Pros: Easy fault isolation, robust.
    + Cons: High cabling and I/O port costs.
            
- `Tree`: Hierarchical structure with a root node.
    + Pros: Scalable, suitable for large networks.
    + Cons: Dependent on the root node.

- `Bus`: Devices share a single backbone cable.
    + Pros: Simple, reliable, mininmal cabling.
    + Cons: Difficult to add nodes, backbone failure affects the entire network.

- `Star`: Devices connect to a central hub/switch.
    - Pros: Easy to install, manage, and troubleshoot.
    + Cons: Dependent on the central hub.

- `Ring`: Devices form a closed loop.
    + Pros: Simple for peer-to-peer networks.
    + Cons: Single device failure can disrupt the network.

### Applications
- Ring and Mesh: Suitable for peer-to-peer networks.
- Star and Tree: Ideal for client-server networks.
- Bus: Flexible for both.

---

## 5. Network Protocols
### Definition 
Rules and formats for communication between network devices.

### Protocol Requirements
- `Message Encoding`: Converts data into transmittable forms (e.g., light, electrical impulses).

- `Message Formatting and Encapsulation`: Defines data format based on message type and channel.

- `Message Size`: Specifies data packet size.

- `Message Timing`: Manages transmission rate (flow control) and delivery timing.

- `Delivery Options`:
    + Unicast: One-to-one communication.
    + Multicast: One-to-many (not all) communication.
    + Broadcast: One-to-all communication.

### Protocol Types
- Network Communication (TCP, UDP).
- Network Security (HTTPS, SSL/TLS).
- Routing (RIP, OSPF, BGP).
- Service Discovery (DNS).

### Protocol Models
(1) `TCP/IP Model`:
- **Application Layer**: Interfaces with users (FTP, DNS, HTTP).

- **Transport Layer**:
    + TCP: Reliable, connection-oriented, uses flow control, sequence numbers, and acknowledgements.
    + UDP: Unreliable, connectionless, suitable for high-speed applications (e.g., straming).

- **Internet Layer**: Routes data (IP).

- **Network Access Layer**: Manages hardware and media.

(2) `OSI Model` (7 layers):
- **Physical**: Transmits bits over media (e.g., copper, fiber, wireless).

- **Data Link**: Transmits frames, provides framing, link access, and error detection/correction.

- **Network**: Routes packets (IP), users routers.

- **Transport**: Manages process-to-process communication (TCP/UDP).
    + Multiplexing: Combines data into segments.
    + Demultiplexing: Delivers segments to correct sockets using port numbers (16-bit, 0-65535).

- **Session, Presentation, Application**: Manage sessions, data formatting, and user applications.
    
### Routing Algorithms
- `Centralized`: A controller computes and distributes fowarding tables.

- `Decentralized`: Each router runs its own routing algorithm.

- `Static`: Fixed routing tables.

- `Dynamic`: Tables update based on network with congestion.

- `Load-Sensitive`: Link cost varies with congestion.

- `Load-Insensitive`: Fixed link cost (e.g., RIP, OSPF, BGP).

- `Distannce-Vector`: Shares routing tables with neighbors (e.g., RIP uses hop count).

---

## 6. Key Takeaways

- Understanding network elements (end devices, intermediate devices, media) is important for designing networks.

- Network categories (LAN, MAN, WAN, Internet) define the scope and scale of connectivity.

- Architecture like cloud-based and peer-to-peer cater to different operational needs.

- Topologies (Mesh, Tree, Star, Ring) impact network performance and cost.

- Protocols (TC/IP, OSI) and routing algorithms ensure efficient and reliable commmunication.
