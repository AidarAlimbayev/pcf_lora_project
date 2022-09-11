class Animal:
    def __init__(self, animal_id, pin, spray_duration, server_time, task_id):
        self.animal_id = animal_id
        self.pin = pin
        self.spray_duration = spray_duration
        self.server_time = server_time
        self.task_id = task_id

task_id, spraying_type, volume, server_time = 1, 2, 3, 4
cow_id = "01010101012222"
pin = 40
spray_duration = 
cow = Animal(cow_id, task_id, spraying_type, volume, server_time)

#  class Person:
#   def __init__(mysillyobject, name, age):
#     mysillyobject.name = name
#     mysillyobject.age = age

#   def myfunc(abc):
#     print("Hello my name is " + abc.name)

# p1 = Person("John", 36)
# p1.myfunc()
# print(p1)
# i = 0


# while i<10:
#     p1.age = i
#     print(p1.age)
#     print("-")
#     i+=1

# print(p1.age)
# del p1

# print(p1)