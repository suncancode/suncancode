###################
# Design Patterns #
###################

---

## 1. Reification Transformation
Picture this: You’ve got some data like skills or degrees listed as plain text, but you want to manage them better. Reification transforms non-object elements (like relationships or attributes) into full-fledged objects, making your model more detailed and flexible.

### Why Do We Need Reification?
- Moves beyond simple attributes to manage complex relationships.
- **Benefits**: More detail, easier to expand.
- **Downside**: Adds complexity to the diagram.

### Detailed Examples
- **Example 1: Employee Skills**:
    - **Basic Design**: `Employee` class with `number`, `name`, `salary`, and a `skills` list (e.g., "Java, Python").
    - **Reified Design**: Create a `Skill` class with `skillName`, and a "Has" relationship from `Employee` to `Skill` (0..* multiplicity).
    - **Result**: Instead of a string, each skill (e.g., "Java") is an object, allowing you to add details like skill level later.
    - **Diagram Placeholder**:
        +-----------+        +-----------+
        | Employee  |<-------| Skill     |
        |-----------|        |-----------|
        | number    |        | skillName |
        | name      |        +-----------+
        | salary    |
        +-----------+
        (Relationship: "Has", 0..* multiplicity)


- **Example 2: Student Degrees**:
    - **Basic Design**: `Student` class with `studentNumber`, `firstName`, `lastName`, `address`, and `degreeName` (e.g., "BSc").
    - **Reified Design**: Create a `Degree` class with `degreeName`, and a "Enrolls in" relationship from `Student` to `Degree` (0..* multiplicity).
    - **Result**: Students can enroll in multiple degrees, and you can add attributes like `graduationDate` to `Degree`.
    - **Diagram Placeholder**:
        +---------------+        +------------+
        | Student       |<-------| Degree     |
        |---------------|        |------------|
        | studentNumber |        | degreeName |
        | firstName     |        +------------+
        | lastName      |
        | address       |
        +---------------+
        (Relationship: "Enrolls in", 0..* multiplicity)

---

## 2. Roles Played by Names
Names in your conceptual schema can play different roles depending on context. This section helps you figure out whether a name is a value, an attribute name, or even a class name, keeping your design consistent.

### Why Do We Need This?
- Ensures names are used wisely, avoiding confusion.
- **Benefits**: Reusable, reduces redundancy.
- **Downside**: Requires careful planning.

### Detailed Examples
- **Example: Stock Items**:
    - **Context**: `StockItem` class with `name`, `currentPrice`, `datePriced`.
    - **Case Study: "Sugar"**:
        - **Role 1: Attribute Value**: "Sugar" is the value of `name` in a `StockItem` instance (e.g., name = "Sugar", price = $2).
        - **Role 2: Attribute Name**: "Sugar" could become a new attribute name (e.g., `sugarQuantity`) if needed.
        - **Role 3: Class Name**: "Sugar" could be a subclass `Sugar` inheriting from `StockItem` (e.g., to manage sugar-specific details).
    - **Result**: Depending on context, "Sugar" adapts, making the design flexible.
    - **Diagram Placeholder**:
        +---------------+
        |   StockItem   |
        +---------------+
        | name          |
        | currentPrice  |
        | datePriced    |
        +---------------+
        "(Note: ""Sugar"" can be value, attribute name, or subclass)"

---

## 3. Patterns
Patterns are proven solutions to common design problems. Though the lecture cuts off here, it likely introduces patterns like reification, generalization, or association classes to optimize your schema.

### Why Do We Need Patterns?
- Speeds up design with best practices.
- **Benefits**: Efficient, reusable.
- **Downside**: Needs experience to apply correctly.

### Simple Tree 
- **Idea**: A linear hierarchy where a parent has multiple children without cross-links.
- **Example**: Family tree with `FamilyMember`. Parent (John) has children (Alice, Bob).
- **Result**: Simple structure: John → Alice, John → Bob.

### Complex Tree Pattern
- **Idea**: A hierarchy with cross-links and multiple levels.
- **Example**: Company structure with `Employee`. Manager (Mary) supervises Tom, who reports to Director (Jane).
- **Result**: Complex links: Mary → Tom ← Jane.
- **Diagram Placeholder**:
    +-----------+        +-----------+
    | Employee  |<-------| Employee  |
    |-----------|        |-----------|
    | name      |        | name      |
    +-----------+        +-----------+
         |                    |
    +----|----+          +----|----+
    |         |          |         |
    Mary      Tom        Jane
    (Relationships: "Reports to" 0..1, "Supervises" 0..*)

### Item Description Pattern
- **Idea**: Describes items with dynamic attributes using reification.
- **Example**: `Product` (Shirt) described by `Description` (color = "Blue", size = "M").
- **Result**: Add new descriptions (e.g., material = "Cotton") easily.
- **Diagram Placeholder**:
    +-----------+        +----------------+
    | Product   |<-------| Description    |
    |-----------|        |----------------|
    | id        |        | attributeName  |
    +-----------+        | attributeValue |
                         +----------------+
    (Relationship: "Described by", 0..* multiplicity)

### Qualification Pattern
- **Idea**: Defines qualifications or states via a related class.
- **Example**: `Employee` (John) qualified in `LanguageSkill` (English, Level 5).
- **Result**: Track and update skills (e.g., add French, Level 4).
- **Diagram Placeholder**:
    +-----------+        +---------------+
    | Employee  |<-------| LanguageSkill |
    |-----------|        |---------------|
    | name      |        | language      |
    +-----------+        | level         |
                         +---------------+
    (Relationship: "Qualified in", 0..* multiplicity)

### Homomorphism Pattern
- **Idea**: Maps one structure to an equivalent structure for data synchronization.
- **Example**: `Customer` (CRM ID 001) maps to `Client` (Sales ID 101) via `Mapping`.
- **Result**: Sync data without altering original structures.
- **Diagram Placeholder**:
    +-----------+        +---------+        +-----------+
    | Customer  |<-------| Mapping |------->| Client    |
    |-----------|        |---------|        |-----------|
    | crmId     |        | crmId   |        | salesId   |
    +-----------+        | salesId |        +-----------+
                         +---------+
    (Relationship: "Maps to", 1..1 multiplicity)