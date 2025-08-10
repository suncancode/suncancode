###########################
# Database Design Summary #
###########################

---

## 1. Database Design Process
### Desciption
The database design process involves 3 main stages to transform a real-world problem into a functional database:
- **Conceptual Modeling**: Converts a real-world description into a conceptual schema using diagrams.

- **Logical Design**:  Transform the conceptual schema into a logical schema.

- **Physical Design**: Adds implementation details (e.g., indexes, partitions) to optimize performance.

### Example
**Scenario**: A school wants to manage student enrollment.

- **Conceptual modeling**: Draw a diagram with classes `Student` and `Course`, linked by an `Enrolls` association.

- **Logical Design**: Create tables:
    + `Student` (StudentID, Name, DOB)
    + `Course` (CourseID, Name)
    + `Enrollments` (StudentID, CourseID, EnrollmentDate)

- **Physical Design**: Add an index on `StudentID` for faster student lookups.

---

## 2. Database Domain
### Desciption
A database domain is a specific part of the real world selected for stotage in a database. It defines what data to manage based on real-world requirements.

### Example
- **Scenario**: A small business tracks supplies and parts.
    + **Details**:
        ++ **Supplier**: Identified by `SupplierNumber` (Name, DOB, Salary, City).
        ++ **Parts**: Identified by `PartNumber` (PartName, Quantity).
        ++ **Shipments**: Defined by `SupplierNumber`, `PartName`, `Quantity`.
    + This domain outlines the data to be stored.

---

## 3. Database Schema
### Desciption
A database schema describes stored data at different abstraction levels:
- **Conceptual Schema**: Uses classes, objects, associations, and hierarchies.

- **Logical Schema**: Uses tables, attributes, and rows.

- **Physical Schema**: Includes files, indexes, and storage structures.

### Example
**Scenario**: Managing a supplier-part relationship.

- **Conceptual Schema**: Class `Supplier` (`Name`, `City`) linked to `Part` via `Supplier` association.

- **Logical Schema**: Tables:
    + `Supplier` (SupplierID, Name, City).
    + `Part` (PartID, Name, Price).
    + `Shipments` (SupplierID, PartID, Quantity).

- **Physical Schema**: Add an index on `SupplierID` for efficient queries.

---

## 4. Object Modeling
### Description
Object modeling is a conceptual modeling technique using class diagrams to represent objects, attributes, and relationships. Key principles include:
- Data is divided into discrete objects (e.g., student).

- Object have attributes and are identified by unique attributes.

- Classes group similar objects (e.g., all student in `STUDENT`).

- Associations linked classes (e.g., `STUDENT` to `COURSE` via `Attends`).

- Generalization hierarchies show "is-a" relationships (e.g., `UNDERGRADUATE` is a `STUDENT`).

### Example
- **Objects**: Student *Sun* (StudentID: 8389, Name: Sun).

- **Classes**: `STUDENT` (`StudentID`, `Name`, `DOB`).

- **Association**: `STUDENT` `Attends` `COURSE`.

- **Generalization**:
    + `STUDENT` includes `UNDERGRADUATE` and `POSTGRADUATE`.