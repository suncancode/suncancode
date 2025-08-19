# Requirement Analysis Process

---

## The Big Picture: What’s This Process All About?
- **Definition Time**: A "requirement" is what the network *must* have (like needs vs. wants), and the "process" is a series of steps to nail it down.
- **The Flow**: It's a loop of 5 steps (from McCabe, 2007): Gather & List Requirements → Develop Service Metrics → Characterize Behavior → Develop Requirements → Map Requirements. Think of it as building a roadmap for your network adventure!

--- 

## Step 1: Gathering and Listing Requirements – Hunt for the Basics!
- **Why?**: Start with initial conditions to set the stage – these are your project's "why" and "how."

- **Key Stuff to Gather**:
    - *Project Types*: `New network`, `upgrade`, `analysis`, `outsourcing`, `consolidation`.
    - *Scope*: `Size`, `sites`, `distances` – e.g., one building or global?
    - *Goals*: `Boost performance`, `add security`, `support new apps/users/devices`.
    - *Outside Forces*: `Politics`, `admin hurdles`, `budgets`.
    - *Constraints*: `Money limits`, `org politics`, `existing gear` (user resistance or custom software).

- **Pro Tips**:
    - *Work with users* via surveys, chats, meetings – but balance time!
    - *Set expectations*: If they say "real-time" but mean "fast enough," clarify to avoid drama.
    - *Watch for red flags*: Vague terms like "high-performance" or wild expectations.
    - *Performance Targets*: Multi-tier (high/low thresholds for critical stuff) or single-tier (one-size-fits-all).
    - *Measure peaks* on testbeds or real networks to spot issues.
    - *Tracking*: Use paragraphs with track changes, spreadsheets, or tools like Jira. Keep 'em updated and accessible!

- **Output**: A Requirements Spec doc with tables (
    `ID`, 
    `Date`, 
    `Type`, 
    `Description`, 
    `Locations`, 
    `Status`, 
    `Priority`
). 

---

## Step 2: Developing Service Metrics – Measure What Matters! 📏
- **Why?**: Turn requirements into measurable bits to check if the network delivers (high vs. low perf, guaranteed vs. best-effort).

- **Cool Metrics**:
    - *RMA* (Reliability, Maintainability, Availability):
        - `Reliability`: MTBF (avg time between fails), MTBCF (for critical fails).
        - `Maintainability`: MTTR (avg repair time).
        - `Availability`: Up/down-time, error rates (e.g., 99.999% uptime).
    - *Capacity*: Peak/sustained/min data rates, burst sizes.
    - *Delay*: End-to-end/round-trip, latency, jitter (delay wiggle).

- **Tools**: 
    - `PING` for delay/loss.
    - `Traceroute` for paths/delays.
    - `SNMP/MIBs` (Management Information Base) for monitoring.

---

## Step 3: Characterizing Behavior – How Does Everything Act? 🕵️‍♂️
- **Why?**: Figure out real-world usage to predict traffic and pitfalls.

- **Break It Down**:
    - *System Characterization*: `Boundaries` (what's in/out), `interactions` (user-app-device-net), overall description.
    - *Application Behavior*: Group by `type` (mission-critical: high RMA; rate-critical: high bandwidth; real-time: low delay). Note `locations`, `components` (client-server, peer-to-peer).
    - *User Behavior*: `Locations` (campus, remote), `patterns` (numbers, times, growth). E.g., Engineers hog bandwidth mornings.
    - *Device Behavior*: `Types` (desktops, servers, specialized like supercomputers), `locations`, `specs` (storage, CPU, memory).
    - *Network Behavior:*: `Locations`, `dependencies`, `constraints`.

- **Pro Tip**: This avoids surprises – like realizing remote users need VPN for secure access.

---

## Step 4: Developing Requirements – Refine and Get Technical! 🔧
- **Why?**: Turn fuzzy reqs into crisp, tech specs using metrics and behavior.

- **Key Developments**:
    - *RMA*: Thresholds like MTBF > 100k hours.
    - *Capacity*: Limits/envelopes (best/worst-case data rates, bursts).
    - *Delay*: Thresholds like <150ms end-to-end for voice.
    - *Security*: Encryption, access control.
    - *Affordability*: Budget fits.
    - *Manageability*: Easy ops.
    - *QoS*: Quality of Service.

- **Envelopes**: Graphs showing perf boundaries to dodge bottlenecks.

- **Example**: User says "reliable" → Develop to "99.9% availability with MTTR <1 hour."

---

## Step 5: Mapping Requirements – Put It on the Map! 🗺️
- **Why?**: Visualize where reqs live to spot dependencies and flows.

- **How?**: Use `geographic maps` (for WAN), `logical diagrams` (for LAN), or `tables` (requirement map for locations).

- **Benefits**: E.g., Map critical apps to sites needing fast links – highlights where to beef up backbone.

- **Output**: `A requirements map showing locations and ties` (e.g., App X at Site A needs low-delay to Device Y at Site B).

---

## Wrapping Up: Why This Rocks and Key Takeaways 🎉
- This process loops to refine everything – skip it, and your network might flop like a bad code deploy!
- **Benefits**: Objective designs, no biases, scalable networks.
- **My Engineer Tip**: Treat it like debugging: 
    Gather facts 
        |
        v
    Measure 
        |
        v
    Characterize bugs (behaviors)
        |
        v 
    Fix (develop)
        |
        v
    Map the flow. 