# https://www.lanshor.com/pathfinding-a-estrella/

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPoint(self):
        return (self.x, self.y)

class Cell:
    def __init__(self, coord, father, type):
        self.coord = coord
        self.father = father
        self.type = type
        self.gfunc = math.dist(coord.getPoint(), father.getPoint())
        self.hfunc = manhattanDistance(coord, father)
        self.ffunc = self.gfunc + self.hfunc
        # falta agregar el tipo de terreno

    def setFather(self, newFather):
        self.father = newFather
        self.gfunc = math.dist(self.coord.getPoint(), newFather.getPoint())
        self.hfunc = manhattanDistance(self.coord, newFather)
        self.ffunc = self.gfunc + self.hfunc
        
    def toString(self):
        return "Coord: {}, Father: {}, Type: {}, g(n): {}, h(n):{}, f(n): {}".format(self.coord.getPoint(), self.father.getPoint(), self.type, self.gfunc, self.hfunc, self.ffunc)

def manhattanDistance(p1, p2):
    return math.fabs(p1.x - p2.x) + math.fabs(p1.y - p2.y)

def getAdyacentCells(cell):   
    adyacents = []
    for i in range(8):
        basePoint = cell.coord.getPoint()
        adyPoint = calculateAdyacent(basePoint, i)
        adyCell = Cell(adyPoint, cell.coord, 100)
        adyacents.append(adyCell)
    return adyacents

def calculateAdyacent(point, index):
    x = point[0]
    y = point[1]
    if index == 0:
        x += 0.1
        y += 0.1
    elif index == 1:
        x += 0.1
    elif index == 2:
        x += 0.1
        y -= 0.1
    elif index == 3:
        y -= 0.1
    elif index == 4:
        x -= 0.1
        y -= 0.1
    elif index == 5:
        x -= 0.1
    elif index == 6:
        x -= 0.1
        y += 0.1
    else:
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
        self.list.sort(key=lambda x: x.ffunc)

    def printList(self):
        for element in self.list:
            print(element.toString())


    

openList = CellList()
closedList = CellList()
ended = False

p_i = Point(0.0, 0.0)
p_f = Point(0.3, 0.3)

# paso 0
initialCell = Cell(p_i, p_i, 100)
print(initialCell.toString())
openList.addCell(initialCell)
print(openList.getLenght())

step = 0

while ended == False:
    # paso 1
    c1 = openList.pop()
    print(c1.toString())
    closedList.addCell(c1)

    # paso 2
    print('Adyacentes')
    adyacents = getAdyacentCells(c1)
    print(len(adyacents))

    # paso 3
    for element in adyacents:
        if element.coord.getPoint() == p_f.getPoint():
            print("llegamos")
            ended = True
        elif element.type < 100:
            print("ignoramos")
        elif closedList.isCellinList(element) == True:
            print("Ignoramos")
        elif openList.isCellinList(element) == True:
            idx = openList.getIndex(element)
            if openList.list[idx].gfunc > element.gfunc:
                openList.list[idx] = element
        else:
            openList.addCell(element)

    # paso 4
    openList.orderByF()

    print("Step: {}\n".format(step))

    print("open list")
    openList.printList()

    print("closed list")
    closedList.printList()
    step += 1
    input("wait...")