# CSIT985 - Week 6B: Security and Privacy Architecture

---

## 1. Introduction to Security and Privacy Architecture
- **Concepts**:
  - Security: Protects data using CIA triad (Confidentiality, Integrity, Availability).
  - Privacy: Ensures personal data isn’t misused, complying with laws (e.g., Australian Privacy Act 1988).

- **Objectives**: Meet security (e.g., encryption) and privacy (e.g., anonymization) requirements from analysis.

- **Role**: Extends network architecture (Week 6A), integrates into reference architecture, impacts performance/management.

- **Scope**: Covers internal network and external interactions (e.g., CDN).

---

## 2. Security Components
- **Composition**: Functions (e.g., prevention, detection), Mechanisms (e.g., firewalls, IDS), Internal Relationships (tradeoffs, dependencies, constraints).

- **Key Components**:
  - Access Control: Authentication, authorization (mechanisms: LDAP, RADIUS).
  - Intrusion Detection/Prevention (IDS/IPS): Detect/thwart attacks (mechanisms: signature-based, anomaly-based).
  - Encryption: Protect data (mechanisms: AES, TLS).
  - Audit and Monitoring: Track violations (mechanisms: log analysis).

- **Internal Relationships**:
  - Tradeoffs: Encryption boosts security but increases delay.
  - Dependencies: IDS relies on audit logs.
  - Constraints: IPS may cause false positives, affecting flows.

---

## 3. Privacy Components
- **Composition**: Functions (e.g., protect personal data), Mechanisms (e.g., anonymization), Relationships.

- **Key Components**:
  - Data Anonymization: Hide identity (mechanisms: hashing, masking).
  - Consent Management: Manage user consent (mechanisms: pop-ups, logs).
  - Data Minimization: Collect only necessary data (mechanisms: policy enforcement).

- **Internal Relationships**:
  - Tradeoffs: Anonymization enhances privacy but hinders analytics.
  - Dependencies: Consent needs audit trail.
  - Constraints: Legal limits (e.g., Australian Privacy Act).

- **Integration**: Combines with security (e.g., encryption + anonymization).

---

## 4. Architectural Models and Optimization
- **Models**:
  - Perimeter-based: Protect boundaries (firewalls, DMZ).
  - End-to-end: Secure entire path (encryption, TLS).
  - Zero Trust: Continuous authentication.
  - Privacy by Design: Build privacy from start (anonymization).

- **Optimization**:
  - Based on flows: Prioritize video with encryption, reduce delay with QoS.
  - Tradeoffs: Perimeter manageable but bypassable; Zero Trust resource-intensive.
  - Dependencies: Security needs privacy policies; privacy needs security tools.

- **Implementation**: Use PPDIOO (Plan, Design, Implement, Operate).
