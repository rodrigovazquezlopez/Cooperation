from operator import imod
import random

cntIzq = 0
cntDer = 0
for i in range(100):
    x = random.randint(0, 1)
    random.seed()
    if x == 0:
        print("Moviendo a la derecha")
        cntDer += 1
    else:
        print("Moviendo a la izquierda")
        cntIzq += 1

tot = cntDer - cntIzq
print("Der: {}, Izq: {}, Total: {}".format(cntDer, cntIzq, tot))
