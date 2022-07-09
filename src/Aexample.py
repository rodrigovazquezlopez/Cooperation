# https://www.lanshor.com/pathfinding-a-estrella/

import math
from re import L

# Clase punto
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPoint(self):
        return (self.x, self.y)

# clase cell
class Cell:
    def __init__(self, coord, father, type, origin, target):
        self.coord = coord
        self.father = father
        self.type = type
        self.origin = origin
        self.target = target
        self.gfunc = math.dist(coord.getPoint(), origin.getPoint())
        self.hfunc = manhattanDistance(coord, target)
        self.ffunc = self.gfunc + self.hfunc

    def setFather(self, newFather):
        self.father = newFather
        self.gfunc = math.dist(self.coord.getPoint(), self.origin.getPoint())
        self.ffunc = self.gfunc + self.hfunc
        
    def toString(self):
        return "Coord: {}, Father: {}, Type: {}, g(n): {}, h(n):{}, f(n): {}".format(self.coord.getPoint(), self.father.getPoint(), self.type, self.gfunc, self.hfunc, self.ffunc)

def manhattanDistance(p1, p2):
    return math.fabs(p1.x - p2.x) + math.fabs(p1.y - p2.y)

def getAdyacentCells(cell, listTrajectory):   
    adyacents = []
    for i in range(8):
        type = 100
        basePoint = cell.coord.getPoint()
        adyPoint = calculateAdyacent(basePoint, i)
        if adyPoint.getPoint() in listTrajectory:
            type = 0
        adyCell = Cell(adyPoint, father, type, cell.origin, cell.target)
        adyacents.append(adyCell)
    return adyacents

def calculateAdyacent(point, index):
    x = point[0]
    y = point[1]
    if index == 0:
        #x = x
        y += 0.1
    elif index == 1:
        x += 0.1
        y += 0.1
    elif index == 2:
        x += 0.1
        #y = y
    elif index == 3:
        x += 0.1
        y -= 0.1
    elif index == 4:
        #x = x
        y -= 0.1
    elif index == 5:
        x -= 0.1
        y -= 0.1
    elif index == 6:
        x -= 0.1
        #y = y
    else:
        x -= 0.1
        y += 0.1
    res = Point(x, y)
    return res


class CellList:
    def __init__(self):
        self.list = []
    
    def addCell(self, cell):
        self.list.append(cell)

    def pop(self):
        return self.list.pop()

    def getLenght(self):
        return len(self.list)

    def isCellinList(self, cell):
        if len(self.list) != 0:
            for element in self.list:
                if element.coord.getPoint() == cell.coord.getPoint():
                    return True
            return False

    def getIndex(self, cell):
        i = 0
        if len(self.list) != 0:
            for element in self.list:
                if element.coord.getPoint() == cell.coord.getPoint():
                    return i
                i += 1
        return -1

    def orderByF(self):
        self.list.sort(key=lambda x: x.ffunc, reverse=True)

    def printList(self):
        for element in self.list:
            print(element.toString())


    

openList = CellList()
closedList = CellList()
resultList = []
ended = False

p_i = Point(-0.4, 0.2)
p_f = Point(1.3, 0.4)

filename = "./data/twoDim/22 Feb/MovesTwoDim_22Feb2022_11.51_log.txt"
solution = "solution.txt"

trajectoryList = []

# Leyendo archivo con trayectoria
with open(filename, 'r') as file:
    for linea in file.readlines():
        tokens = linea.rsplit(', ')
        p = (float(tokens[1]), float(tokens[2]))
        trajectoryList.append(p)
print("Trayectoria leida...")
#print(trajectoryList)
#input("wait...")

# paso 0
initialCell = Cell(p_i, p_i, 100, p_i, p_f)
#print(initialCell.toString())
openList.addCell(initialCell)
#print(openList.getLenght())


step = 0
father = ''

while ended == False:
    print("************************* Step: {} *************************\n".format(step))
    # paso 1
    cell = openList.pop()
    print("----- celda extraida -----")
    print(cell.toString())
    closedList.addCell(cell)

    # paso 2
    print('\ncalculando Adyacentes')
    adyacents = getAdyacentCells(cell, trajectoryList)
    print(len(adyacents))

    # paso 3
    i = 1
    for element in adyacents:
        if element.coord.getPoint() == p_f.getPoint():
            print("llegamos")
            resultList.append(element)
            father = element.father
            ended = True
            
        elif element.type < 100:
            print("Adyacente {}: infranqueable".format(i))
        elif closedList.isCellinList(element) == True:
            print("Adyacente {}: esta en lista cerrada".format(i))
        elif openList.isCellinList(element) == True:
            print("Adyacente {}: recalculando g".format(i))
            idx = openList.getIndex(element)
            if openList.list[idx].gfunc > element.gfunc:
                openList.list[idx] = element
                #openList.list[idx].setFather(cell.coord)
        else:
            #print
            element.setFather(cell.father) # revisar si es necesario
            openList.addCell(element)
        i += 1

    # paso 4
    openList.orderByF()

    print("-----------open list-----------")
    openList.printList()

    print("\n-----------closed list-----------")
    closedList.printList()
    step += 1
    
    input("wait...")

while father != p_i:
    for element in closedList.list:
        if element.coord.getPoint() == father.getPoint():
            resultList.insert(0, element)
            father = element.father
            break
resultList.insert(0, initialCell)   


# with open(solution, 'w') as file:
#     for element in closedList.list:
#         data = element.coord.getPoint()
#         text = "{}, {}\n".format(data[0], data[1])
#         file.write(text)

with open(solution, 'w') as file:
    for element in resultList:
        data = element.coord.getPoint()
        text = "{}, {}\n".format(data[0], data[1])
        file.write(text)