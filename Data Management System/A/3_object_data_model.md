#############################
# Object Data Model Summary #
#############################

---

## 1. Graphical Notations for Conceptual Modeling
### Description
The lecture introduces various graphical notations for conceptual modeling, which provide a visual representation of data relationships. These include:
- **Entity-Relationship (ER) Diagrams (1976)**: Pioneered by Peter Chen, used to model entities and their relationships.
- **Object Modelling Technique (OMT) Diagrams (1991)**: Focuses on objects, attributes, and associations, developed by Rumbaugh et al.
- **(Simplified) Unified Modelling Language (UML) Object Class Diagrams (1994)**: A standardized notation by Booch, Rumbaugh, and Jacobson, simplified for conceptual schemas.
- **Object Role Modeling (ORM) Diagrams**: Emphasizes roles and facts, less common but notable.
- Many other notations exist, reflecting diverse approaches to data modeling.

---

## 2. (Simplified) Class of Objects
### Description
A class of objects represents a collection of similar entities with common attributes. In simplified UML, it is depicted as a rectangular box with a header containing the class name.
- Attributes are listed below the header, describing properties of objects.
- This notation supports the foundation of object-oriented design in databases.

### Multiplicity of attribute
- [1..5] (from one to five)
- zero or more ([*] or [0..*])
- one or more ([1..*])
- optional (zero or one, [0..1])
- from "m" to "n" ([m..n]) follows a name of attribute
- Default multiplicity is "one" ([1])

### Example
- Class `Student` with attributes: `studentID`, `name`, `DOB`.

---

## 3. Association
### Description
An association is a relationship between two or more classes, represented by a solid line connecting the classes.
- It indicates how instances of one class relate to instances of another (e.g., "owns" between "Person" and "Car").
- Multiplicity (e.g., 1, *, 0..1) defines the number of instances involved.

### Example
- Association "Enrolls" between "Student" and "Subject":
- Multiplicity: 1 (Student) -- * (Subject).

---

## 4. Link Attribute
### Description
A link attribute is a property attached to an association, describing the relationship itself (e.g., date of enrollment).
- Represented by a dashed line from the association to a class or note.
- Enhances the semantics of the association.

### Example
- Link attribute "EnrollmentDate" for "Student Enrolls Subject":
- Dashed line to a note: "EnrollmentDate".

---

## 5. Association Class
### Description
An association class is a class that combines an association with additional attributes, connected by a dashed line to the association.
- Used when the relationship has its own identity and properties (e.g., an enrollment record).
- Merges association and class concepts.

### Example
- Class "Enrollment" linked to "Student Enrolls Subject" with attributes like "Grade".

---

## 6. Qualification
### Description
A qualification is a property used to distinguish instances of a class within an association, often acting as a partial identifier.
- Depicted as a small box on the association line, containing the qualifying attribute.
- Reduces redundancy in relationships.

### Example
- Qualification "RoomNumber" on "Building Contains Room" to identify specific rooms.

---

## 7. Generalization
### Description
Generalization is a relationship where a subclass (e.g., "Car") inherits from a superclass (e.g., "Vehicle").
- Represented by a line with a triangle pointing to the superclass.
- Supports inheritance and specialization in object modeling.

### Example
- "Car ISA Vehicle" with triangle from "Car" to "Vehicle".
