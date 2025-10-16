class Catalog:
    def __init__(self):
        self.items = {} # Dictionary to store items' names and prices

    @staticmethod
    def insertion_sort(intList):
        n = len(intList)
        for i in range(1, n):
            j = i
            while j > 0 and intList[j] < intList[j - 1]:
                # Swap
                temp = intList[j]
                intList[j] = intList[j - 1]
                intList[j - 1] = temp 
                j -= 1
        return intList

    def add_item(self, name, price):
        # Add item name with its price
        self.items[name] = price

    def get_price(self, name):
        # Return name if exists, otherwise None
        if name in self.items:
            return name
        else:
            return None
        
    def count(self):
        # Return total number of items
        return len(self.items)

    def average_price(self):
        # Return average price of items
        if len(self.items) == 0:
            return 0
        total = 0
        for item in self.items:
            total += self.items[item]
        return total / len(self.items)
    
    def median_price(self):
        # Return median price of items
        if len(self.items) == 0:
            return 0
        
        unsorted_prices = []
        for item in self.items:
            unsorted_prices.append(self.items[item])
        sorted_prices = self.insertion_sort(unsorted_prices)
        n = len(sorted_prices)
        mid = n // 2
        if n % 2 == 1:
            return float(sorted_prices[mid])
        else:
            return (sorted_prices[mid - 1] + sorted_prices[mid]) / 2
        
# Main program
catalog = Catalog()

# Get input for number of items
n = int(input("Enter number of items: "))
item_count = 0
# Get item name and price
while item_count < n:
    name = input("Enter name: ")
    price = float(input("Enter price: "))
    catalog.add_item(name, price)
    item_count += 1

# Get input for number of queries
q = int(input("Enter number of queries: "))
query_count = 0
# Process query
while query_count < q:
    name = input("Query name: ")
    
    if name in catalog.items:
        print("{0}: {1:.2f}".format(name, catalog.items[name]))
    else:
        print("{0}: NA".format(name))    
    query_count += 1

# Display overall information
print("Total items:", catalog.count())
print("Average price: {0:.2f}".format(catalog.average_price()))
print("Median price: {0:.2f}".format(catalog.median_price()))



        
