# Hive Programming

When warehouse data grows too large for a single RDBMS, **Hive** runs on top of Hadoop/HDFS, translating HiveQL into MapReduce jobs. HiveQL looks like the SQL from part 2, but adds many options driven by the fact that execution underneath is distributed MapReduce, not a single centralized engine.

## 1. Data Selection and Scope

- Basic `SELECT ... FROM ... WHERE ... LIMIT` structure matches standard SQL.
- **Nested queries / subqueries**: a `SELECT` can be used wherever a table or scalar value is expected; a subquery used in `FROM` must be given an **alias**.
- **CTEs** (`WITH ... AS (...)`, Common Table Expressions) are an alternative, more readable way to write the same subqueries:

```sql
WITH cord AS (
  SELECT * FROM customer JOIN orders ON c_custkey = o_custkey
)
SELECT c_name, c_phone, o_orderkey, o_orderstatus
FROM cord;
```

- **Inner join**: joining multiple tables spawns **MapReduce jobs**. Put the **largest table last** in the join sequence — the last table is streamed through the reducers, while earlier tables are buffered in reducer memory by default. This can be hinted explicitly: `/*+ STREAMTABLE(lineitem) */`.
- **Map join**: if a table is small enough, Hive can read it entirely into memory and **broadcast** it to all map tasks, performing the join during the map phase — **no reduce phase needed**, which is much faster since the expensive shuffle+reduce step is skipped. Enabled automatically via `hive.auto.convert.join=true`, or forced with `/*+ MAPJOIN(orders) */`.
- **Bucket map join**: a variant of map join that only reads the required **bucket** of a small table instead of the whole table. Requires `hive.optimize.bucketmapjoin=true`.
- **Outer join** (left, right, full) and **cross join** preserve standard HQL semantics.
- **Left semi join**: equivalent to `WHERE EXISTS (subquery)` in standard SQL — the right-hand table may only be referenced in the join condition, never in `SELECT` or `WHERE`.

```sql
SELECT c_name, c_phone
FROM customer LEFT SEMI JOIN orders ON c_custkey = o_custkey;
```

- **Set operations**: Hive supports only `UNION ALL`. It does **not** support `INTERSECT` or `MINUS` — these must be rewritten:
  - `INTERSECT` → rewrite using a `JOIN`.
  - `MINUS` → rewrite using a `LEFT OUTER JOIN` with an `IS NULL` condition in `WHERE`.

## 2. Data Manipulation

Because Hive operates on HDFS files rather than row-by-row inserts like a typical RDBMS, loading and exporting data has its own statements.

### LOAD
```sql
-- From a local file
LOAD DATA LOCAL INPATH '/local/home/janusz/HIVE-EXAMPLES/TPCHR/part.txt'
OVERWRITE INTO TABLE part;

-- Into a specific partition
LOAD DATA LOCAL INPATH '/local/home/janusz/HIVE-EXAMPLES/TPCHR/part.txt'
OVERWRITE INTO TABLE part PARTITION (P_BRAND='GoldenBolts');

-- From HDFS (omit LOCAL): default path, or a full URI
LOAD DATA INPATH '/user/janusz/part.txt' OVERWRITE INTO TABLE part;
```

- The `LOCAL` keyword decides whether the source file is read from the local filesystem or from HDFS (default path, or the URI given after `INPATH`, or the `fs.default` value).
- `OVERWRITE` decides whether to replace or append the existing data in the target table/partition.

### EXPORT / IMPORT
```sql
EXPORT TABLE part TO '/user/tpchr/part';   -- exports data + metadata (a _metadata file)
IMPORT table new_part FROM '/user/tpchr/part';
IMPORT EXTERNAL table new_extpart FROM '/user/tpchr/part';
```

`EXPORT`/`IMPORT` support migrating or backing up/restoring tables between Hive instances or HDFS clusters.

### Sorting and distribution — four related but distinct clauses

| Clause | Global sort? | Distributes rows across reducers? |
|---|---|---|
| `ORDER BY` | Yes | Not by design — but a global sort forces **a single reducer**, which is slow for large data |
| `SORT BY` | No — only sorts locally **within each reducer** | No |
| `DISTRIBUTE BY` | No | **Yes** — rows with matching column values go to the same reducer (similar to `GROUP BY`'s distribution, but without aggregation) |
| `CLUSTER BY` | No (sorts within each group) | Yes — **shorthand** for `DISTRIBUTE BY x SORT BY x` when the distribution and sort columns are the same |

```sql
-- SORT BY: locally sorted per reducer only
SET mapred.reduce.tasks = 2;
SELECT p_partkey, p_name FROM part SORT BY p_name ASC;

-- DISTRIBUTE BY must precede SORT BY when used together
SELECT p_partkey, p_name FROM part
DISTRIBUTE BY p_partkey
SORT BY p_name;

-- CLUSTER BY first (parallel), then ORDER BY (final global sort)
SELECT p_partkey, p_name FROM part
CLUSTER BY p_name
ORDER BY p_name;
```

This distinction is a direct consequence of the MapReduce architecture: a true global `ORDER BY` requires funneling all data to one reducer, which is expensive — the other clauses are compromises that trade strict global ordering for parallelism.

## 3. Data Aggregation and Sampling

Hive supports the same SQL/OLAP concepts from part 2, with Hive-specific syntax.

### GROUP BY, GROUPING SETS, ROLLUP, CUBE
```sql
SELECT p_type, count(*) FROM part GROUP BY p_type;

-- collect_set aggregates values of a group into a set
SELECT p_type, collect_set(p_name), count(*) FROM part GROUP BY p_type;

SELECT p_type, p_name, count(*)
FROM part
GROUP BY p_type, p_name
GROUPING SETS ((p_type), (p_name));

SELECT p_type, p_name, count(*) FROM part GROUP BY p_type, p_name WITH ROLLUP;
SELECT p_type, p_name, count(*) FROM part GROUP BY p_type, p_name WITH CUBE;
```

`GROUPING SETS`, `ROLLUP` and `CUBE` behave exactly as in part 2 — the concepts are identical, only the Hive syntax (`WITH ROLLUP`/`WITH CUBE` appended after `GROUP BY`) differs from standard SQL.

- **`GROUPING__ID`** is a Hive-specific function that distinguishes which aggregation level a result row belongs to — useful because `CUBE`/`ROLLUP` results contain many `NULL`s, and `GROUPING__ID` tells you whether a `NULL` means "not grouped by this column" or an actual `NULL` value in the source data.
- **`HAVING`** filters `GROUP BY` results, same as standard SQL:

```sql
SELECT GROUPING__ID, p_type, p_name, count(*)
FROM part
GROUP BY p_type, p_name WITH CUBE
HAVING count(*) > 1
ORDER BY grouping__id;
```

### Analytic (window) functions
Same syntax as part 2 — `function(...) OVER (PARTITION BY ... ORDER BY ...)`.

```sql
SELECT p_name, COUNT(*) OVER (PARTITION BY p_name) FROM PART;

SELECT l_orderkey, l_partkey, l_quantity,
       RANK() OVER (ORDER BY l_quantity),
       DENSE_RANK() OVER (ORDER BY l_quantity)
FROM lineitem;

SELECT l_orderkey, l_partkey, l_quantity,
       FIRST_VALUE(l_quantity) OVER (PARTITION BY l_orderkey ORDER BY l_quantity),
       LAST_VALUE(l_quantity)  OVER (PARTITION BY l_orderkey ORDER BY l_quantity)
FROM lineitem;

-- window framing
SELECT l_orderkey, l_partkey, l_quantity,
       MAX(l_quantity) OVER (
         PARTITION BY l_orderkey ORDER BY l_partkey
         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
       )
FROM lineitem;
```

### Sampling — a Hive-specific addition
Only relevant at Hive's data scale: sometimes you want to explore or test on a small sample instead of scanning the whole dataset.

```sql
-- Random sampling
SELECT * FROM lineitem DISTRIBUTE BY RAND() SORT BY RAND() LIMIT 5;

-- Bucket table sampling (optimized for tables already bucketed)
SELECT * FROM customer TABLESAMPLE(BUCKET 3 OUT OF 8 ON rand());

-- Block sampling: by row count, percentage, or byte size
SELECT * FROM lineitem TABLESAMPLE(4 ROWS);
SELECT * FROM lineitem TABLESAMPLE(50 PERCENT);
SELECT * FROM lineitem TABLESAMPLE(20B);
```

## References
- Gross C., Gupta A., Shaw S., Vermeulen A. F., Kjerrumgaar D., *Practical Hive: A guide to Hadoop's Data Warehouse System*, Apress 2016, Chapter 4.
- Lee D., *Instant Apache Hive Essentials How-to*, Packt Publishing Ltd. 2013.
- Apache Hive™, https://hive.apache.org
