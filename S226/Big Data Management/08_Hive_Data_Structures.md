# Hive — Data Structures

**Course:** ISIT312 Big Data Management
**Topic:** Hive Data Types, Databases, Tables, Partitions, Buckets, Views

---

## 1. Primitive Data Types

| Type | Size | Example |
|---|---|---|
| TINYINT | 1 byte | `10Y` |
| SMALLINT | 2 bytes | `10S` |
| INT | 4 bytes | `10` |
| BIGINT | 8 bytes | `10L` |
| FLOAT | 4 bytes | `0.1234567` |
| DOUBLE | 8 bytes | `0.1234567891234` |
| DECIMAL(m,n) | fixed precision | `3.14` |
| BINARY | n bytes | `1011001` |
| BOOLEAN | 1 byte | `TRUE` / `FALSE` |
| STRING | up to ~2 GB | `'Abcdef'` |
| CHAR | fixed length, up to 255 bytes | `'Hello'` |
| VARCHAR | variable length | `'Hive'` |
| DATE | `YYYY-MM-DD` | `'2017-05-03'` |
| TIMESTAMP | `YYYY-MM-DD HH:MM:SS[.fff...]` | `'2017-05-03 15:10:00.345'` |

Notes:
- `DECIMAL(m, n)` provides **fixed precision**, in contrast to `FLOAT`/`DOUBLE`, which are floating-point (approximate) types.
- `CHAR` is **fixed-length**; `VARCHAR` is **variable-length**.

---

## 2. Complex Data Types

Hive supports complex/nested column types, which is a major difference from traditional relational databases:

### ARRAY
A list of values of the same type.

```
example: ['Hadoop', 'Pig', 'Hive']
access:  bigdata[1]      -- access by index
```

### MAP
A set of key-value pairs.

```
example: {'k1':'Hadoop', 'k2':'Pig'}
access:  bigdata['k2']   -- access by key
```

### STRUCT
A collection of named fields, each with its own type (like a nested record).

```
example: {name:'Hadoop', age:24, salary:50000.06}
access:  bigdata.name    -- access by field name (dot notation)
```

### Creating a table with complex types

```sql
CREATE TABLE types(
   array_col  array<string>,
   map_col    map<int,string>,
   struct_col struct<a:string, b:int, c:double>
);
```

### Inserting values into complex-type columns

```sql
INSERT INTO types
SELECT array('bolt', 'nut', 'screw'),
       map(1, 'bolt', 2, 'nut', 3, 'screw'),
       named_struct('a', 'bolt', 'b', 5, 'c', 0.5)
FROM DUAL;
```

- `array(...)` constructs an ARRAY value.
- `map(k1, v1, k2, v2, ...)` constructs a MAP value.
- `named_struct(name1, val1, name2, val2, ...)` constructs a STRUCT value.

---

## 3. Databases

- A **database** is a collection of conceptually related tables — i.e., tables that together implement a conceptual schema.
- Physically, a database is implemented as a **folder/directory in HDFS**.
- The **default database** is located at `/user/hive/warehouse`.
- A new database is created as a subfolder of `/user/hive/warehouse`.
  - Example: a database named `tpchr` is located at `/user/hive/warehouse/tpchr.db`.

---

## 4. Tables: Internal vs. External

### Internal (Managed) Tables

- Created and fully managed by Hive within HDFS.
- Hive manages the **entire lifecycle** of the table and its data: adding/deleting data, creating/dropping the table.
- **Dropping an internal table deletes both the metadata (from the metastore) and the actual data in HDFS.**

```sql
CREATE TABLE IF NOT EXISTS intregion(
   R_REGIONKEY DECIMAL(12),
   R_NAME      VARCHAR(25),
   R_COMMENT   VARCHAR(152)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH 'region.tbl' INTO TABLE intregion;
```

### External Tables

- Used when data **already exists** in HDFS, and you want to provide a tabular view over it without moving/copying it into the default warehouse directory.
- Created with `CREATE EXTERNAL TABLE`, and the data's location is specified with the `LOCATION` clause instead of relying on the default warehouse directory.
- **Dropping an external table deletes only the metadata from the metastore — the underlying data in HDFS is preserved.**

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS extregion(
   R_REGIONKEY DECIMAL(12),
   R_NAME      VARCHAR(25),
   R_COMMENT   VARCHAR(152)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
STORED AS TEXTFILE LOCATION '/user/tpchr/region';

LOAD DATA LOCAL INPATH 'region.tbl' INTO TABLE extregion;
```

### Example: External table over a file already in HDFS

This is the typical use case for external tables — attaching a tabular structure to data that is already sitting in HDFS.

```bash
hadoop fs -mkdir /user/tpchr/nation
hadoop fs -put nation.tbl /user/tpchr/nation
hadoop fs -ls /user/tpchr/nation
# -rw-r--r-- 3 janusz supergroup 401 2017-07-02 10:24 /user/tpchr/nation/nation.tbl
```

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS extnation(
   N_NATIONKEY DECIMAL(12),
   N_NAME      VARCHAR(25),
   N_COMMENT   VARCHAR(152)
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
STORED AS TEXTFILE LOCATION '/user/tpchr/nation';
```

### Internal vs. External — Quick Comparison

| Aspect | Internal (Managed) Table | External Table |
|---|---|---|
| Data location | Default warehouse directory | Specified via `LOCATION` |
| Who manages data lifecycle | Hive fully manages it | Data lifecycle managed outside Hive |
| Effect of `DROP TABLE` | Metadata **and** data deleted | Only metadata deleted; data kept in HDFS |
| Typical use case | Data created/owned by Hive | Data already exists in HDFS from another process |

---

## 5. Partitions

- **Purpose:** avoid scanning the entire table when a query only needs a fragment of the data.
- Physically, a **partition is a subfolder in HDFS**, nested inside the table's directory.
- When a query filters on the partition column, Hive only accesses the relevant partition(s) instead of scanning the whole table.

### Creating a partitioned table

```sql
CREATE TABLE IF NOT EXISTS part(
   P_PARTKEY DECIMAL(12),
   P_NAME    VARCHAR(55),
   P_TYPE    VARCHAR(25),
   P_SIZE    DECIMAL(12),
   P_COMMENT VARCHAR(23)
)
PARTITIONED BY (P_BRAND VARCHAR(20))
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;
```

### Adding a partition (must be done before loading data into it)

```sql
ALTER TABLE part ADD PARTITION (P_BRAND='GoldenBolts');
```

### Listing partitions

```sql
SHOW PARTITIONS part;
-- OK
-- p_brand=GoldenBolts
-- Time taken: 0.072 seconds, Fetched: 1 row(s)
```

### Loading data into a partition

```sql
LOAD DATA LOCAL INPATH '/local/home/janusz/HIVE-EXAMPLES/TPCHR/part.txt'
OVERWRITE INTO TABLE part PARTITION (P_BRAND='GoldenBolts');
```

### A partition as seen in HDFS

```bash
hadoop fs -ls /user/hive/warehouse/part
# Found 1 items
# drwxrwxr-x - janusz supergroup 0 2017-07-01 19:00 /user/hive/warehouse/part/p_brand=GoldenBolts
```

Note the directory naming convention: `column_name=value` (e.g. `p_brand=GoldenBolts`).

---

## 6. Buckets

- Another way to speed up processing of a table by dividing it further.
- A **bucket corresponds to a segment (file) in HDFS**, not a folder.
- Rows are assigned to buckets based on the **hash value** of a specified column.

### Creating a bucketed table

```sql
CREATE TABLE customer(
   C_CUSTKEY  DECIMAL(12),
   C_NAME     VARCHAR(25),
   C_PHONE    CHAR(15),
   C_ACCTBAL  DECIMAL(12,2)
)
CLUSTERED BY (C_CUSTKEY) INTO 2 BUCKETS
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|';
```

### Required MapReduce / Hive settings

```sql
SET map.reduce.tasks = 2;
SET hive.enforce.bucketing = true;
```

### Inserting data into a bucketed table

```sql
INSERT INTO customer VALUES (1, 'Customer#000000001', '25-989-741-2988', 711.56);
INSERT INTO customer VALUES (2, 'Customer#000000002', '23-768-687-3665', 121.65);
INSERT INTO customer VALUES (3, 'Customer#000000003', '11-719-748-3364', 7498.12);
INSERT INTO customer VALUES (4, 'Customer#000000004', '14-128-190-5944', 2866.83);
INSERT INTO customer VALUES (5, 'Customer#000000005', '13-750-942-6364', 794.47);
```

Each row is routed into one of the 2 buckets based on `hash(C_CUSTKEY) mod 2`.

### Partitions vs. Buckets — Quick Comparison

| Aspect | Partition | Bucket |
|---|---|---|
| Physical form in HDFS | Subfolder | File (segment) |
| Assignment rule | Explicit value of the partition column | Hash of the bucketing column |
| Must be created before loading? | Yes (`ALTER TABLE ... ADD PARTITION`) | No — determined automatically on insert |
| Typical use | Coarse-grained pruning (e.g., by date, brand) | Finer, evenly distributed grouping (e.g., for joins, sampling) |

---

## 7. Views

Views are listed in the lecture outline as one of the core Hive data structures (alongside databases, tables, partitions, and buckets). They provide a saved, named query that can be referenced like a table, without physically storing the underlying data separately. *(The detailed slide content on views was not available in the extracted lecture material — see the course slides or ask your instructor for the full definition and example syntax.)*

---

## 8. References

- Gross C., Gupta A., Shaw S., Vermeulen A. F., Kjerrumgaard D., *Practical Hive: A Guide to Hadoop's Data Warehouse System*, Apress, 2016, Chapter 4.
- Lee D., *Instant Apache Hive Essentials How-to: Leverage Your Knowledge of SQL to Easily Write Distributed Data Processing Applications on Hadoop Using Apache Hive*, Packt Publishing Ltd., 2013.

---

## 9. Quick Recap

| Concept | Physical form in HDFS | Key command |
|---|---|---|
| Database | Folder (`db_name.db`) | `CREATE DATABASE` |
| Internal table | Folder under warehouse | `CREATE TABLE` |
| External table | Folder at custom `LOCATION` | `CREATE EXTERNAL TABLE ... LOCATION` |
| Partition | Subfolder (`col=value`) inside table folder | `ALTER TABLE ... ADD PARTITION` |
| Bucket | File segment inside table/partition folder | `CLUSTERED BY (...) INTO n BUCKETS` |
