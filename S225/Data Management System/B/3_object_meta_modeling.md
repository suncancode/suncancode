########################
# Object Meta Modeling #
########################

----

## 1. Generic Classes
Imagine you’ve designed a class in object modeling, but later you need to add new attributes. Normally, you’d have to tweak the class definition, risking system issues. Generic classes solve this by combining **data** (the actual info) with **metadata** (data about the data). Metadata stores attribute names and values, letting you extend the class endlessly without changing its core design.

### Why Do We Need Generic Classes?
- The real world evolves fast—today’s attributes might not cut it tomorrow.
- **Benefits**: Flexible, easy to maintain, no major redesigns needed.
- **Downside**: A bit trickier to manage due to metadata.

### Detailed Examples
- **Example 1: Managing Vehicles**:
    - **Basic Design**: The `Vehicle` class starts with fixed attributes: `registration`, `manufacturer`, and `year`.
    - **Future Need**: Add `color` or `engine type` later.
    - **Generic Design**:
        - Use a `Vehicle` class with a basic ID.
        - Add an `Attribute` class (stores names like "manufacturer") and a `Value` class (stores values like "Toyota").
        - Relationship: `Vehicle` "Has" many `Attribute-Value` pairs.
    - **Result**: To add "color," just insert a new `Attribute-Value` instance (e.g., "color" = "Red") via metadata—no need to edit the `Vehicle` class!
    - **Diagram Placeholder**:
        +---------+        +-----------------+
        | Vehicle |<------| Attribute-Value |
        |---------|       |-----------------|
        | ID      |       | name            |
        +---------+       | value           |
        +-----------------+
        (Relationship: "Has", 0..* multiplicity)

- **Example 2: Document Structure**:
    - A document has pages, paragraphs, and sentences, with potential for more levels.
    - **Generic Design**: Use a `Part` class with a "Consists of" relationship.
    - A `Document` is a `Part`, containing `Part` instances (pages), which contain more `Part` instances (paragraphs), and so on.
    - **Result**: Add a new level (e.g., words in sentences) by creating new `Part` instances, no new class needed.
    - **Diagram Placeholder**:
        +---------+        +---------+
        | Document|<-------| Part    |
        |---------|        |---------|
        | ID      |        | ID      |
        +---------+        +---------+
        (Relationship: "Consists of", 0..* multiplicity)

---

## 2. Generic Associations
Not just classes, but the relationships between them need flexibility too. Generic associations use metadata to define relationship types, multiplicity, and roles, allowing changes without altering the original design.

### Why Do We Need Generic Associations?
- Relationships evolve: A one-to-one link might become many-to-many.
- **Benefits**: Perfect for large, dynamic systems like ERPs.
- **Downside**: Queries get more complex due to metadata.

### Detailed Examples
- **Basic Design**: A rigid relationship, e.g., `Employee` "Works in" `Department` with 1..1 multiplicity.
- **Generic Design**:
    - Add an `Association` class (defines relationship type like "Works in").
    - Add a `Role` class (defines multiplicity and role, e.g., "Employee: 1..*", "Department: 1..1").
    - Relationship: Original classes connect via `Association-Role` using metadata.
- **Example**: In a project system, the `Project` to `Team` relationship starts as "Manages." Later, it changes to "Collaborates" with different multiplicity—just update the `Association` metadata, no redesign needed.
- **Diagram Placeholder**:
    +----------+        +-------------+        +----------+
    | Employee |<-------| Association |------->| Department |
    |----------|        |-------------|        |----------|
    | ID       |        | type        |        | ID       |
    +----------+        +-------------+        +----------+
    (Via Role: Employee 1..*, Department 1..1)

---

## 3. Metamodel
Metamodel is the next level up—it’s a "model of a model," describing how elements like classes, attributes, and associations are defined. Think of it as the rulebook for building other models.

### Why Do We Need Metamodel?
- To automate design: Tools like UMLet rely on metamodels to ensure correctness.
- **Benefits**: Enables meta-level systems and tool integration.
- **Downside**: Can be tricky to grasp at first.

### Detailed Examples
- **Metamodel Structure**: Includes metaclasses like:
    - `Class`: Defines a class (name, owned attributes).
    - `Property`: Defines attributes (name, type, multiplicity like [0..1]).
    - `Association`: Defines relationships (member ends, multiplicity).
- **UML Metamodel Example**: In UML, the metamodel states a "Class" must have "ownedAttribute," and an "Association" has "memberEnd."
- **Application**: When drawing in UMLet, the metamodel prevents invalid inputs (e.g., no negative multiplicity).
- **Example**: In a big data system, the metamodel auto-generates generic classes from metadata, like the `Vehicle` example—defining "Attribute" as a `Property` of a `Class`.
- **Diagram Placeholder**:
    +-----------+        +------------+        +-------------+
    | Class     |<-------| Property   |<-------| Association |
    |-----------|        |------------|        |-------------|
    | name      |        | name       |        | type        |
    | ownedAttr |        | type       |        | memberEnd   |
    +-----------+        +------------+        +-------------+
    (Metamodel relationships: defines, connects)


