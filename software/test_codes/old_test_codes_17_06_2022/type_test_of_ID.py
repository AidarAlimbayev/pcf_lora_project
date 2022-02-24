null_id = "4354000400b01"

cow_id = "b'4354000400b01'"

animal_id = 435400040001


print("Initial variables: Start")
print("-------")
print("cow_id :")
print(cow_id)
print(type(cow_id))

print("-------")
print("null_id :")
print(null_id)
print(type(null_id))

print("-------")
print("animal_id :")
print(animal_id)
print(type(animal_id))


print("Initial variables: End")
print()
print()
print("Encoded variable: Start")

print("-------")
print("cow_id.encode()")
print(cow_id.encode())
print(type(cow_id.encode()))

print("-------")
print("null_id.encode()")
print(null_id.encode())
print(type(null_id.encode()))

# print("-------")
# print("animal_id.encode()")
# print(animal_id.encode())
# print(type(animal_id.encode()))
print("Encoded variable: End")
print()
print()
print("String variable: Start")

print("-------")
print("str(cow_id)")
print(str(cow_id))
print(type(str(cow_id)))

print("-------")
print("str(null_id)")
print(str(null_id))
print(type(str(null_id)))

print("-------")
print("str(animal_id)")
print(str(animal_id))
print(type(str(animal_id)))

print("String variable: End")
print()
print()
print("Intered variable: Start")

print("-------")
# print("str(cow_id)")
# print(int(cow_id))
# print(type(int(cow_id)))

print("-------")
print("str(null_id)")
print(int(null_id))
print(type(int(null_id)))

print("-------")
print("str(animal_id)")
print(int(animal_id))
print(type(int(animal_id)))

print("Integer variable: End")
print()
print()

print("-------")

if (null_id == null_id.encode()):
    print("simpe is equal to encode")

if cow_id == null_id.encode():
    print("only with 'b value is equal to encode")

if cow_id.encode == null_id.encode():
    print("only with 'b value is equal to encode")

if cow_id == str(null_id):
    print("only with string value is equal to string")

if cow_id == null_id:
    print("only with string value is equal to string")

print("-------")

weight_float = 0.0

weight_int = 0

weight_str = '0'





print(0.0)