#from asyncio.windows_events import NULL
#from re import A

def void_main(a, b):
    c = a + 5
    #v = b * a 
    c = None
    v = None
    weight_finall = None

    weight_to_return = (float("{0:.2f}".format(weight_finall)))
    return [c, v, weight_to_return]

a = 5
b = 7

x, n, weight_after_return = void_main(a, b)

print("x:", x)
print("n:", n)
print("weight_after_return:", weight_after_return)