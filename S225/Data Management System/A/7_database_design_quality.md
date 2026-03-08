# Database Design Quality 

---

## Why not ONE BIG TABLE?
### What's the idea?
Imagine a database for an online store. Here’s the domain:
- A **customer** has a unique customer number, first name, and last name.
- Customers submit **orders** with a unique order number and order date.
- Each order has **lines** with item name, price per item, and total items.

**One Big Table Idea:** Combine all into one table like this:
| customer_number | first_name | last_name | order_number | order_date | item_name | price_per_item | total_items |
|-----------------|------------|-----------|--------------|------------|-----------|----------------|-------------|
| 101             | John       | Doe       | 1001         | 2023-01-01 | Book      | 10.00          | 2           |
| 101             | John       | Doe       | 1002         | 2023-01-03 | Pen       | 1.50           | 5           |

### Why it's bad?
- **Redundancy**: Name will be repeated for every order.
- **Hard to manage**: Changing customer's name requires updating multiple rows.
- **Limits Flexibility**

---

## Where is a Problem?
- **Data Redundancy**: Repeating customer info `wastes space` and `risks error`.
  - *Example*: John becomes "Johnson," missing one update breaks consistency.

- **Insertion Anomalies**: Can't add a customer without an order.
  - *Example*: New customer Khoi can't be added until she orders.

- **Deletion Anomalies**: Deleting an order might lose customer data.
  - *Example*: Removing order xxx deletes John if it's his last order.

- **Update Anomalies**: Changing data needs multiple updates.
  - *Example*: Forget one row, and prices mismatch.

---

## Insertion Test
### What is this?
`This test checks if you can add new data easily`. A good design lets you insert without needing extra info.

- **With One Big Table:** Can’t add Alice Brown (no order yet).

- **With Split Tables:** Works perfectly!
  - **CUSTOMER:** (customer_number, first_name, last_name)
    | customer_number | first_name | last_name |
    |-----------------|------------|-----------|
    | 103             | Alice      | Brown     |
  - **ORDER:** (order_number, customer_number, order_date)
  - **LINE_ITEM:** (order_number, item_name, price_per_item, total_items)

**Result:** Splitting tables passes the insertion test—Alice can join anytime!

---

## Good Design Guidelines
### How to Design Better
- **Normalization**: Split data into related tables.

- **Use Keys**: Define primary keys (PK), and foreign keys (FK).

- **Avoid Redundancy**: Store data once, link with keys.

- **Ensure Integrity**: Use constraints. (e.g., NOT NULL, CHECK)