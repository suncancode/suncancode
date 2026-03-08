# Strategic Network Design and Requirement Analysis Concepts

---

## Part A: **Plan for Strategic Network Design**
This section focus on the foundational steps before network analysis, including `defining the scope` and `developing a strategic network plan`.

### Defining the Scope

*Importance*: The first step in network design is to clearly define the scope. 
-> Building a new (`green field`) network.
(OR)-> Optimizing/expanding an existing one.

*Impact*:
- A new network requires fresh data on user needs and applications.
- An existing network involves assessing current infrastructure, dependencies, and constrains.

*Key Consideration*: ALWAYS identify if the design is for a completely new setup or an upgrade to avoid mismatched requirements.

---

### The Strategic Network Plan

*Overview*: A strategic network plan outlines how the network aligns with organizational goals. It brigdes the gap between `current state` and `desired future state`.

*To Plan or Not?*
- What `purpose` will the strategic plan serve?
- How will it `help the organization`?
- Will it be `better than the system we use` now?
- Are those in `leadership` positions `committed` to strategic 
planning?
- How much will it `cost` in terms of `time` and `personnel` 
effort?
- `Who` should be on the planning team?
- Does `anyone` have `experience` with strategic planning?
- Do we think `we can do it?`
- `Are we willing` to `make decisions` about our future?
- Will we `actually use the plan`?
- What overriding `crises` would `inhibit our ability` to plan?

---

### The Crouch Diagram

*Description*:
 1. Why are we in business? (Vision, Driving Force, Mission)
 2. How do we do business? (Values, Climate, Culture)

**Gap analysis**
 3. Where are we noew? (Strength, Weakness, Opportunity, Threat, Competition, Constrains - SWOT Analysis)
 4. Where do we want to be? (Strategy)
 5. How do we get there? (Tactics, Resources)
**End of Gap Analysis**

 6. How will we know we're arrived? (Coordination, Budget, Control, Report, Milestone)

---

### Strategy vs Tactics

- *Strategy*: Broad, long-term approach to achieving objectives.
- *Tactics*: Specific, short-term actions.

**Difference**
| Aspect | Strategy | Tactics |
| --- | --- | --- |
| Scale of Objective | Grand | Limited |
| Scope of Action | Broad and General | Narrowly Focused |
| Guidance Provided | General and Ongoing | Specific and Situational |
| Degree of Flexibility | Adaptable, but not hasty | Fluid and quick to adjust |
| Timing | Before Action | During Action |
| Resource Focus | Deployment | Employment |

---

### 6 Tips for Strategic Planning

 1. Treat it as an ongoing process, not a one-time event - the plan is never perfect.
 2. Keep it simple and manageable.
 3. Involve organizational leaders directly (DO NOT oursource to stagg or consultants).
 4. Emphasize creativity and innovation over rigid steps.
 5. Ensure strategies are implementable - consider how they will be executed.
 6. Remember, the plan is a tool to achieve the organization's mission, not an end goal.

---

### 10 Pitfalls of Strategic Planning (and How to avoid)

 1. Relying solely on stats/financials - balance with qualitative insights.
 2. Rushing with forms/deadlines - allow time for thoughtful input.
 3. Pretending support without resources - commit time and budget.
 4. Keeping incentives short-term - align with long-term goals.
 5. Blaming external factors - focus on internal improvements.
 6. Training for the future then downsizing - maintain consistency.
 7. Copying competitors - innovate based on your needs.
 8. Creating uninspiring visions - engage frontline staff.
 9. Limitting vision to finances - think holistically.
 10. Clinging to the past - embrace change.

---

### 4 Basic Strategies for Change

 1. *Rational-Empirical*: Assumes people act on self-interest, use information and incentives.
 2. *Normative-Re-educative*: Focuses on social norms, redefine norms and build commitment.
 3. *Power-Coercive*: Relies on authority, impose sanctions.
 4. *Environmental-Adaptive*: Build a new structure and transitions people gradually.

---

### Factors in Selecting Strategies

- *Degree of Resistance*: Strong resistance -> Power-Coercive or Environmental-Adaptive
- *Target Population*: Large groups need a mix of strategies.
- *Stakes*: High stakes require all strategies.
- *Time Frame*: 
    + Short -> Power-Coercive.
    + Longer -> Others.
- *Expertise*: Match strategies to team skills.
- *Dependency*: Negotiate if mutual dependency exists.

---

### Who should be involved?

- *Guidelines*: Include those planning, providing infor, reviewing, and authorizing.
- *Key Roles*: Chief executive, board chair, and directors for strategic direction.
- *Stakeholder*: Involve as many as possible, especially implements.
- *Phases*:
    + Board for mission/ vision/ values.
    + Staff for analysis/ issues/ goals.
    + Staff for strategies.
- *Rules*: When in doubt, include them - better to over-involve than exclude.

---

## Part B: **Requirement Analysis Concepts**
This section explains why and how to analyze requiremens for users, applications, devices, and networks.

---

### Why Requirement Analysis?

- *Background*: Requirements describe network functions and performance needed for users, applications, and devices.
- *Activities*: Identify/gather requirements, set performance thresholds, and device on service levels (best-effort, predictable, guaranteed).
- *Results*:
    + `Requirement Specification`: Document listing prioritized requirements.
    + `Requirement Map`: Show location dependencies. 
- *Categorizing Requirements and `RFC 2119 Keywords for Prioritization`*:
    + **Core** (essential): 
        . `Must`/ `Shall`/ `Required`.
        . `Must Not`/ `Shall Not`.
    + **Features** (desiable, but optional/future): 
        . `Should`/ `Recommended`.
        . `Should Not`/ `Not Recommended`.
        . `May`/ `Optional`.
    + **Rejected** (unnecessary): 
        . `May`/ `Optional`.
    + **Future**/**Informational**:
        . `Should`/ `Recommended`.
        . `Should Not`/ `Not Recommended`.
        . `May`/ `Optional`.
- *Payoff*: Objective choices, sized networks, performance tradeoffs, and bottleneck avoidance.
- *Risk of Skipping*: Designs based on blasses (e.g., favorite tech/ vendor) instead of needs.

---

### Network Services

- *Definition*: Configurable capabilites that must be end-to-end.
- *Requirements*: Services should be configurable, measurable, verifiable (via accounting).
- *Hierarchy*: General in backbone, specific near users.
- *Sources*: Derived from users, apps, devices.
- *Mismatches*: Cause bottlenecks - ensure alignment.

---

### User Requirement

- *Key Aspects*: Timeliness, Interactivity, Reliability, Presentation Quality, Adaptability, Security, Affordability, Functionality, Supportability, Future Growth.
- *Details*:
    + `Timeliness`: Reasonable access time.
    + `Reliability`: Consistent availability.
    + `Security`: Protect data integrity/ confidentiality.
    + Also track user numbers, locations and growth.
- *Nature*: Subjective and least technical.

---

### Application Requirements

- *Role*: App link users/devices to the network, often end-to-end.
- *Categories*: 
    + `Mission Critical`: High reliability/ maintainability/ availability (RMA).
    + `Rate Critical`: High capacity.
    + `Real-time/Interactive`: Low delay.
- *Locations*: Map apps to network positions for flow analysis.
- *User Requirements*: Translate to performance metrics (delay, reliability, capacity).

---

### Device Requirement

- *Type*:
    + `Generic`: Single-user, end-to-end needs (e.g., desktops, laptops).
    + `Server`: Multi-user, impact data flow.
    + `Specialized`: Location-dependent (e.g., supercomputer).
- *Performance*: Storage, processor, memory, bus speeds.
- *Overlooked Risk*: Ignoring devices leads to poor "last foor" design.

---

### Network Requirement
- *Consideration*: Existing networks' scaling, locations, constrains, dependencies, interoperability, and obsolescence.
- *Goal*: Ensure new design integrates without issues.
