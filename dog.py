# dog.py
class Dog:
    def __init__(self, name):
        self.name = name
        print("dog initialized!")

my_dog = Dog("Rex")
# Adding the "breed" property on the fly
my_dog.breed = "SuperDog"
# will print "SuperDog"
print(my_dog.breed)
