class Sensor:
    def __init__(self, name, readings):
        self.name = name
        self.readings = readings
    
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

    @staticmethod
    def list_sum(values):
        total = 0
        for item in values:
            total += item
        return total

    def average(self):
        if len(self.readings) == 0:
            return 0.0
        average = self.list_sum(self.readings) / len(self.readings)
        return float(average)

    def trimmed_average(self):
        if len(self.readings) < 3:
            return self.average()
        # Manually copy the list
        copied_readings = []
        for value in self.readings:
            copied_readings.append(value)
        # Sort the readings list in ascending order
        sorted_readings = self.insertion_sort(copied_readings)
        trimmed_readings = sorted_readings[1:-1] # Remove the smallest and the largest

        trimmed_average_number = self.list_sum(trimmed_readings) / len(trimmed_readings)
        return float(trimmed_average_number)

    def is_alert(self, threshold):
        return self.trimmed_average() >= threshold

class Network():
    def __init__(self):
        self.sensors = []

    @staticmethod
    def list_sum(list):
        sum = 0
        for item in list:
            sum += item
        return sum

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def overall_average(self):
        all_readings = []
        for sensor in self.sensors:
            for reading in sensor.readings:
                all_readings.append(reading)
        
        if len(all_readings) == 0:
            return 0.0

        overall_average_number = self.list_sum(all_readings) / len(all_readings)
        return float(overall_average_number)
    
# main program
# Create network object
network = Network()

# Get user input of sensors
num_sensors = float(input("Enter number of sensors: "))
sensor_count = 0

while sensor_count < num_sensors:
    name = input("Enter name: ")
    readings = []
    num_readings = float(input("Enter number of readings: "))
    reading_count = 0
    
    while reading_count < num_readings:
        reading = float(input("Enter reading: "))
        readings.append(reading)
        reading_count += 1 # Reading count increament
    
    sensor = Sensor(name, readings)
    network.add_sensor(sensor)
    sensor_count +=1 # Sensor count increament

# Get input for threshold
threshold = float(input("Enter alert threshold: "))
print()

# Display overall information
print("Overall average: {0:.1f}".format(network.overall_average()))
# Display sensors above threshold list
print("Sensors above threshold (trimmed avg >= {0:.1f}):".format(threshold))
for sensor in network.sensors:
    if sensor.is_alert(threshold):
        print("{0} - {1:.1f}".format(sensor.name, sensor.trimmed_average()))




