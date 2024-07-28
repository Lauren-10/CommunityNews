

class Car(): 
    max_speed = 10
    num_wheels = 4 

    def go(self): 
        print(f"vroom on {self.num_wheels} wheels")

class Convertible(Car): 
    def lower_roof(self): 
        print("root lowering")

my_car = Car()

my_car.go()

my_convertible = Convertible()
my_convertible.lower_roof()
my_convertible.go()
        

