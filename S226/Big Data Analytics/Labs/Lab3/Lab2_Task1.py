"""
Task 1: Load data and basic evaluation
"""

import pandas as pd

# NOTE: Update this path to match where you saved yearly_sales.csv
FILE_PATH = r"D:\sun\WOLLONGONG\suncancode\S226\Big Data Analytics\Labs\Lab3\yearly_sales.csv"

# ---------------------------------------------------------
# Code 1: Import the CSV file
# ---------------------------------------------------------
# index_col=0 -> use the first column (customer ID) as the row index
sales = pd.read_csv(FILE_PATH, index_col=0)
print('sales:\n', sales)

# ---------------------------------------------------------
# Code 2: Examine the imported dataset
# ---------------------------------------------------------
print('sales head:\n', sales.head())          # first 5 rows -> quick preview
print('sales shape:', sales.shape)             # (rows, columns)
print('sales describe:\n', sales.describe())   # summary statistics (count, mean, std, min, max, quartiles)

# Extra check: is there missing data anywhere?
print('missing values per column:\n', sales.isnull().sum())

# Extra check: data types of each column
print('data types:\n', sales.dtypes)
