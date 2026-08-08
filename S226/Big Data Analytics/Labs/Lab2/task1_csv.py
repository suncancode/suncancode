"""
Task 1 - Structured data: yearly sales in CSV format
CSCI446/946 Big Data Analytics - Lab 1
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---- Đường dẫn tới thư mục chứa dataset ----
DATA_DIR = r"D:\sun\WOLLONGONG\S226\CSCI946 - Big Data Analytics\Lab\W2\Lab1-Released\CSCI446_946_Week2_Lab_SP_2026_Datasets"

# 1.1 Load and examine the data
sales = pd.read_csv(os.path.join(DATA_DIR, "yearly_sales.csv"))

print(sales.head())
print(sales.describe())

# --- Thông tin hỗ trợ trả lời câu hỏi ---
print("\nShape (rows, columns):", sales.shape)
print("\nsales_total stats:")
print("  min :", sales["sales_total"].min())
print("  mean:", sales["sales_total"].mean())
print("  max :", sales["sales_total"].max())

# 1.2 Visualise orders and sales
sales.plot(
    x="num_of_orders",
    y="sales_total",
    style="o",
    title="Number of Orders versus Total Sales"
)
plt.xlabel("Number of orders")
plt.ylabel("Total sales")
plt.show()

"""
Questions to answer:
1. How many rows and columns are in the dataset?
2. What are the minimum, mean and maximum values of sales_total?
3. What does the plot suggest about the relationship between the number
   of orders and total sales?
"""
