"""
Task 2: Visualization in data evaluation
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# NOTE: Update this path to match where you saved yearly_sales.csv
FILE_PATH = r"D:\sun\WOLLONGONG\suncancode\S226\Big Data Analytics\Labs\Lab3\yearly_sales.csv"

sales = pd.read_csv(FILE_PATH, index_col=0)

# ---------------------------------------------------------
# Code 3: Plot num_of_orders vs. sales_total
# ---------------------------------------------------------
plt.scatter(sales['num_of_orders'], sales['sales_total'])
plt.title('Number of Orders vs. Sales')
plt.xlabel('num_of_orders')
plt.ylabel('sales_total')
plt.show()

# ---------------------------------------------------------
# Code 4: Fit a linear regression model
# ---------------------------------------------------------
# reshape(-1, 1) -> sklearn expects a 2D array of shape (n_samples, n_features)
y = sales['sales_total'].values.reshape(-1, 1)
X = sales['num_of_orders'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

print('linear regression model intercept :', model.intercept_.item())
print('linear regression model coefficients : ', model.coef_.item())
print('linear regression Model score : ', model.score(X, y))  # R^2 score

# ---------------------------------------------------------
# Code 5: Diagnostics - plot histogram of residuals
# ---------------------------------------------------------
y_pred = model.predict(X)
residuals = y - y_pred

plt.hist(residuals, bins=800)
plt.title('Histogram of Residuals')
plt.xlabel('Residual value')
plt.ylabel('Frequency')
plt.show()

# Extra check: try a different bin count for comparison (helps answer Question 5)
plt.hist(residuals, bins=30)
plt.title('Histogram of Residuals (bins=30)')
plt.xlabel('Residual value')
plt.ylabel('Frequency')
plt.show()
