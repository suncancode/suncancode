# Practice with two-dimensional list (Euler’s Magic Square)

# Define Euler’s magic square
euler = [
    [68**2, 29**2, 41**2, 37**2],
    [17**2, 31**2, 79**2, 32**2],
    [59**2, 28**2, 23**2, 61**2],
    [11**2, 77**2, 8**2, 49**2]
]

# Calculate row sums
row1 = euler[0][0] + euler[0][1] + euler[0][2] + euler[0][3]
row2 = euler[1][0] + euler[1][1] + euler[1][2] + euler[1][3]
row3 = euler[2][0] + euler[2][1] + euler[2][2] + euler[2][3]
row4 = euler[3][0] + euler[3][1] + euler[3][2] + euler[3][3]

# Calculate column sums
column1 = euler[0][0] + euler[1][0] + euler[2][0] + euler[3][0]
column2 = euler[0][1] + euler[1][1] + euler[2][1] + euler[3][1]
column3 = euler[0][2] + euler[1][2] + euler[2][2] + euler[3][2]
column4 = euler[0][3] + euler[1][3] + euler[2][3] + euler[3][3]

# Calculate diagonal sums
diagonal1 = euler[0][0] + euler[1][1] + euler[2][2] + euler[3][3]
diagonal2 = euler[0][3] + euler[1][2] + euler[2][1] + euler[3][0]

# Print results
print("row1={0}, row2={1}, row3={2}, row4={3}".format(row1, row2, row3, row4))
print("column1={0}, column2={1}, column3={2}, column4={3}".format(column1, column2, column3, column4))
print("diagonal1={0}, diagonal2={1}".format(diagonal1, diagonal2))
# Output: All sums should be 8515