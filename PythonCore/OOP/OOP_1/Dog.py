class Dog:
    def __init__(self, breed, age, color):
        self.legs = 4
        self.ears = 2
        self.breed = breed
        self.age = age
        self.color = color

    def bark(self):
        print("Woof!")

    def sleep(self):
        print("The dog is sleeping")
