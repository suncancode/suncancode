GRAPH DATA MODEL

This guide summarizes Graph Data Models from Data Management Systems course. Graph models are used to represent relationships between objects (people, subjects, teachers,...) in a structured way.

1. What are Graph Data Model?
Graph data models are like maps that show how objects are connected. They use:
- NODES: Represent objects.
- EDGES: Represent relationships.

There are 3 main types:
(1) Property Graph
(2) Hypergraph
(3) Nested Graph

2. Property Graph
A Property Graph is a graph where nodes and edges have:
- Labels
- Properties
Each node and edge must has a Unique ID

Example: Instagram
- Node: People
    + Sun (ID: S1, Name: sunhehe)
    + Khoi (ID K1, Name: khoihuhu)
- Edge: Relationship
    + Sun follows Khoi (Edge ID: E1, Type: "FOLLOWS", Date: 10/10/2010)
    + Khoi likes Sun's post (Edge ID: E2, Type: "LIKES", Date: 10/10/2010)

(Sun) --[FOLLOWS, 10/10/2010]--> (Khoi)
(Khoi) --[LIKES, 10/10/2010]--> (Sun's Post)

3. Hypergraph
A Hypergraph is a graph where an edge (hyperedge) can connect MORE THAN  2 NODES.

Example: Group Project 
- Nodes:
    + Person: Sun (ID: P1, Role: Leader)
    + Person: Khoi (ID: P2, Role: Member)
    + Person: Bach (ID: P3, Role: Member)
-  Hyperedge:
    + Team works on project (Hyperedge: "WORK", ID: HE1, Start date: 10/10/2010)
    + Connect: {Sun, Khoi, Bach} --[WORK]--> Web development

3. Nested Graph
A Nested Graph is a graph where a node can contain an entire SUBGRAPH (a smaller graph inside it). Fit for hierarchical structures (organization, family tree,...).

Example: Company Structure
- Hypernode (Node containing subgraph)
    + EBS Department (ID: D1, Type: Outsource)
        Subgraph inside:
        Node:
            . Employee: Sun (ID: EP1, Role: Tester)
            . Employee: Khoi (ID: EP2, Role: Developer)
        Edge:
            . Sun collaborates with Khoi (Edge: "COLLABORATES", ID: E1, Project: Sound2Light)
- Outer Edge:
    EBS Department assigns Sun as lead (Edge: "LEADS", ID: E2)


