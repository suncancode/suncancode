# Hive — Overview

**Course:** ISIT312 Big Data Management
**Topic:** Introduction to Apache Hive

---

## 1. What is Hive?

Hive is a software system built on top of Hadoop that provides:

- A **tabular view** of data stored in HDFS (i.e., data that physically lives as files in a distributed filesystem is presented to the user as rows and columns, like a database table).
- **SQL-like methods** for querying and manipulating that data, through a language called **HQL (Hive Query Language)**.

Key facts:

- The Apache Hive project started at **Facebook in 2010**, with the goal of providing a high-level interface to HDFS.
- Unlike **Pig** (a dataflow-scripting tool that also runs on Hadoop), Hive provides **SQL-like abstractions on top of MapReduce**.
- HQL implements the **SQL-92 standard (almost)** — it is close to standard SQL but not a full implementation.
- HQL gives analysts a tabular view of data and lets them access data located in HDFS without writing MapReduce code directly.
- Hive frees data analysts from needing Java/MapReduce programming skills — *not completely*, since some advanced use cases still require custom code (UDFs, custom SerDes, etc.).

### How an HQL statement is actually executed

When a user submits an HQL statement (e.g. `SELECT dname, count(*) FROM EMPLOYEE GROUP BY dname;`), the following happens:

1. The **Hive client parses** the HQL statement.
2. Hive **creates a processing plan** (an execution plan).
3. The plan is **submitted** as a sequence of MapReduce jobs.
4. **Hadoop/MapReduce executes** the jobs, while progress is monitored.
5. Throughout this process, Hive reads/writes metadata to and from the **Hive metastore** (see below).

In short: HQL statements are parsed by the Hive client and translated into a sequence of Java MapReduce operations, which are then processed by Hadoop. Hive itself does not execute queries — it delegates execution to Hadoop.

---

## 2. Deployment and Configuration

- Hive is available on all commercial Hadoop distributions, and on the Hadoop installation used in the course VM.
- To use Hive, **Hadoop and HDFS must already be up and running** — Hive is a layer on top of them, not a replacement for them.
- The **metastore** (see below) is implemented, by default, using the embedded relational database system **Derby**.
- It is possible to substitute other relational database systems for the metastore, e.g. **MySQL**.
- At the top level, the view of data provided by Hive consists of **databases** and **tables**.

---

## 3. Metastore

The metastore is one of the most important architectural concepts in Hive.

- It contains the **mapping of tables to their directory locations in HDFS**.
- It is itself a **relational database**, read and written by the Hive client.
- It also stores:
  - **Input/output format** information represented by table objects (e.g. `CSVInputFormat`, `TextInputFormat`, etc.).
  - **SerDe** (Serializer/Deserializer) functions, which Hive uses to convert raw data in HDFS into structured rows/columns when reading, and back into raw storage format when writing.

### Example

```sql
CREATE TABLE DEPARTMENT (
   dname  string,
   budget bigint,
   cdate  date
);
```

This table definition is **saved into the Hive metastore**. Later, when running:

```sql
SELECT dname FROM DEPARTMENT WHERE budget > 100000;
```

Hive **retrieves** the table's location and structure from the metastore in order to plan and execute the query.

---

## 4. Interfaces

Hive can be accessed through multiple interfaces:

- **Command Line Interface (CLI)** — accepts and parses HQL commands directly.
- **JDBC/ODBC connectors (drivers)**, used to integrate with other tools, such as:
  - **beeline** (a CLI client that talks to Hive over JDBC/Thrift)
  - **Oracle SQL Developer** (GUI)
  - **Talend Open Studio** (data extraction, transformation, loading, and integration tools)
  - **Jasper Reports**, **QlikView** (business intelligence / reporting tools)
  - **Microsoft Excel 2013** (data analysis tools)
  - **Tableau** (data visualization tools)
- A **storage handler mechanism** to integrate with **HBase**.
- **HUE** (Hadoop User Experience) — an interactive environment for working with HDFS and Hive.
- **HCatalog** — provides a metadata management system shared across **Hadoop, Pig, Hive, and MapReduce**.

---

## 5. HQL (Hive Query Language)

HQL consists of several sub-languages:

1. **Data Definition Language (DDL)** — used for creating, deleting, and altering schema objects such as databases, tables, views, partitions, and buckets.
2. **Data Selection and Scope Language** — used for querying data, joining/linking data across tables, and limiting the range/scope of data returned.
3. **Data Manipulation Language (DML)** — used for exchanging, moving, sorting, and transforming data.
4. **Data Aggregation and Sampling Language** — used for aggregating and sampling data (grouping, summarizing, taking samples of large datasets).

---

## 6. Hive vs. Relational DBMSs

### Similarities

- Tabular view of data objects stored in HDFS.
- Support for typed columns in tables.
- Access to tables through HQL, which closely resembles SQL.
- API interface similar to a standard JDBC programming interface.

### Differences

- Hive is fundamentally a **load-and-read-oriented system** built on top of HDFS, rather than a full read/write transactional system.
- It is still possible to access the data visible in Hive's tabular format **directly through HDFS**, bypassing Hive.
- `UPDATE` is supported only as a **coarse-grained transformation** (e.g., overwriting entire partitions/files) rather than fine-grained, row-level updates as in relational DBMSs.
- There is **no full transaction processing system** (no guarantees like atomic multi-row commits/rollbacks as in traditional RDBMSs).
- Weaker support for constraints such as domain constraints, foreign keys, etc., compared to relational DBMSs.

---

## 7. References

- Gross C., Gupta A., Shaw S., Vermeulen A. F., Kjerrumgaard D., *Practical Hive: A Guide to Hadoop's Data Warehouse System*, Apress, 2016, Chapter 4.
- Lee D., *Instant Apache Hive Essentials How-to: Leverage Your Knowledge of SQL to Easily Write Distributed Data Processing Applications on Hadoop Using Apache Hive*, Packt Publishing Ltd., 2013.

---

## 8. Quick Recap

| Concept | Key idea |
|---|---|
| Hive | SQL-like tabular interface over data stored in HDFS |
| HQL | SQL-92-like query language, parsed and translated into MapReduce jobs |
| Metastore | Relational DB storing table-to-HDFS-location mappings, formats, SerDes |
| Interfaces | CLI, JDBC/ODBC (beeline, BI tools), HBase storage handler, HUE, HCatalog |
| Hive vs RDBMS | Similar tabular/SQL access, but load-oriented, coarse-grained updates, no full transactions |
