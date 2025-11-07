

# class Vehicle:

#     def __init__(self, name, max_speed, mileage):
#         self.name = name
#         self.max_speed = max_speed
#         self.mileage = mileage           

# class Bus(Vehicle):
#     def __init__(self, name, max_speed, mileage):
#         super().__init__(self, name, max_speed, mileage)



# class Vehicle:
#     def __init__(self, name, max_speed, mileage):
#         self.name = name
#         self.max_speed = max_speed
#         self.mileage = mileage

#     def seating_capacity(self, capacity):
#         return f"The seating capacity of a {self.name} is {capacity} passengers"

# class Bus(Vehicle):
    
#     def seating_capacity(self, capacity):
#         capacity = 50
#         return f"The seating capacity of a {self.name} is {capacity} passengers"

# school_bus = Bus("School Volvo", 180, 12)
# print(school_bus.seating_capacity(60))

# class Bus(Vehicle):
    
#     def seating_capacity(self, capacity):
#         capacity = 50
#         super.seating_capacity(capacity)


# class Vehicle:

#     def __init__(self, name, max_speed, mileage):
#         self.name = name
#         self.max_speed = max_speed
#         self.mileage = mileage

# class Bus(Vehicle):
#     def __init__(self, name, max_speed, mileage, color='White'):
#         super().__init__(name, max_speed, mileage)
#         self.color = color
#     def __str__(self):            
#         return f"Color: {self.color}, Vehicle name: {self.name}, Speed: {self.max_speed}, Mileage: {self.mileage}"

# class Car(Vehicle):
#     pass
# print(Bus("School Volvo", 85, 20))