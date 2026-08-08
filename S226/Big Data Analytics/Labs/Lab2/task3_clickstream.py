"""
Task 3 - Quasi-structured data: web clickstream
CSCI446/946 Big Data Analytics - Lab 1
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# ---- Đường dẫn tới thư mục chứa dataset ----
DATA_DIR = r"D:\sun\WOLLONGONG\S226\CSCI946 - Big Data Analytics\Lab\W2\Lab1-Released\CSCI446_946_Week2_Lab_SP_2026_Datasets"

# 3.1 Display the raw log
with open(os.path.join(DATA_DIR, "clickstream.log"), "r") as f:
    log_lines = f.readlines()

print("Number of records:", len(log_lines))
for line in log_lines:
    print(line.strip())

# 3.2 Parse the log into a DataFrame
pattern = re.compile(
    r'(?P<ip>\S+) \S+ (?P<user>\S+) '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) '
    r'"(?P<referrer>[^"]*)" '
    r'"(?P<user_agent>[^"]*)"'
)

records = []
for line in log_lines:
    m = pattern.match(line)
    if m:
        records.append(m.groupdict())

clicks = pd.DataFrame(records)
clicks["status"] = clicks["status"].astype(int)
print(clicks.head())

# 3.3 Summarise the data
print(clicks["method"].value_counts())
print(clicks["status"].value_counts())
print(clicks["url"].value_counts())

# --- Thông tin hỗ trợ trả lời câu hỏi ---
print("\nTotal requests parsed:", len(clicks))
print("Number of 200 (success) responses:", (clicks["status"] == 200).sum())
print("Status code counts (check for 4xx/5xx = errors):")
print(clicks["status"].value_counts().sort_index())

clicks["status"].value_counts().sort_index().plot(kind="bar")
plt.xlabel("HTTP Status Code")
plt.ylabel("Number of Requests")
plt.show()

"""
Questions to answer:
1. How many requests are recorded in the log?
2. Which HTTP methods appear in the log?
3. Which URL is requested most frequently?
4. How many successful (200) responses are recorded?
5. Which status code indicates an error?
6. Why is this file considered quasi-structured rather than structured?
"""
