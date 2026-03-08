#################
# Flow Analysis #
#################

---

## What’s Flow Analysis? 🚗
- **Definition**: It’s about characterizing **data flows** (traffic moving from A to B) to know where they go, what they need (speed, reliability), and which ones are VIPs.

- **Why?**: Helps design networks that don’t choke on traffic. We use the requirements map from Week 4 to track where flows happen.

- **Key Point**: Focus on flows with the biggest impact, not every tiny one.

---

## 1. Flows – The Data Highways
- **What Are They?**: Flows are chunks of network traffic with shared traits (e.g., source/destination addresses, app type, direction).

- **Types**:
  - **Individual Flows**: One app session (e.g., a single Zoom call).
  - **Composite Flows**: Multiple flows sharing a path (e.g., apps using the same backbone).
  - **Critical Flows**: VIP flows needing top performance (e.g., financial apps).

- **Example**: A flow from a payroll server to an accountant’s PC needs 100% uptime.

---

## 2. Identifying and Developing Flows
- **How?**: Use the **Requirements Specification** (users, apps, devices, networks) to:
  - Find **sources** (data creators like servers, cameras) and **sinks** (data receivers like storage, displays).
  - Pick key apps/devices based on priority (e.g., Top 5 apps: email, web, database).
  - Create a **profile**: Group flows with similar needs (e.g., Profile P1: 100Kb/s, 100% reliability for video apps).
  - Map flows using the requirements map to see where they go.

- **Steps**:
  1. Identify apps/devices generating/ending flows.
  2. Focus on critical ones (e.g., mission-critical apps like CAD for engineers).
  3. Use requirements map to track flow paths.

- **Example**: In a hospital, a flow from an X-ray machine (source) to a doctor’s PC (sink) is critical.

---

## 3. Flow Models
- **What?**: Group flows by behavior patterns (direction, hierarchy).
- **Types**:
  - **Peer-to-Peer**: Equal flows, no clear source/sink (e.g., file sharing like BitTorrent).
  - **Client-Server**: Server sends data to clients (e.g., web browsing). Asymmetric, server-heavy.
  - **Hierarchical Client-Server**: Multi-level client-server (e.g., enterprise with branches).
  - **Distributed Computing**: Scattered flows (e.g., cloud apps).
- **Key Traits**:
  - **Directionality**: Some flows favor one direction (e.g., server-to-client for streaming).
  - **Hierarchy**: Spot where flows combine or are critical.
- **Example**: Zoom uses client-server (server sends video to your PC).

---

## 4. Flow Prioritization
- **Why?**: Not all flows are equal. Prioritize based on:
  - App importance (e.g., mission-critical like banking apps).
  - User importance (e.g., CEO’s traffic).
  - Performance needs (e.g., low delay for video calls).

- **Example**: Prioritize a hospital’s real-time surgery app over general email traffic.

---

## 5. Flow Specification
- **What?**: A **flowspec** is a detailed “contract” for a flow’s needs (capacity, delay, reliability).

- **How?**: Combine performance requirements into one profile (e.g., “Video flow: 2Mb/s, <150ms delay, 99.9% reliability”).

- **Why?**: Ensures the network meets promises for critical flows.

---

## 6. Flowspec Algorithm
- **What?**: An algorithm to automate flowspec creation for big networks.

- **How?**: Analyzes requirements map, prioritizes flows, and allocates resources (e.g., bandwidth).

- **Example**: Ensures a finance app gets 50% of backbone bandwidth, email gets 10%.

---

## Key Takeaways
- Flow Analysis is like mapping traffic to avoid jams – know your flows, prioritize VIPs, and spec them out!
- Use requirements maps to track where data flows and what it needs.
- Models (client-server, peer-to-peer) help you organize flows like a pro.
- Practice by mapping a small network (e.g., your office) to spot critical flows.
