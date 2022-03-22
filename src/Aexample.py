# https://www.lanshor.com/pathfinding-a-estrella/

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPoint(self):
        return [self.x, self.y]

    def incX(self):
        self.x += 0.1
    
    def decX(self):
        self.x -= 0.1
    
    def incY(self):
        self.y += 0.1

    def decY(self):
        self.y -= 0.1

class Cell:
    def __init__(self, coord, father, type):
        self.coord = coord
        self.father = father
        self.type = type
        self.gfunc = math.dist(coord.getPoint(), father.getPoint())
        self.hfunc = manhattanDistance(coord, father)
        self.ffunc = self.gfunc + self.hfunc

        # falta agregar el tipo de terreno
        
    def toString(self):
        return "Coord: {}, Father: {}, Type: {}, g(n): {}, h(n):{}, f(n): {}".format(self.coord.getPoint(), self.father.getPoint(), self.type, self.gfunc, self.hfunc, self.ffunc)

def manhattanDistance(p1, p2):
    return math.fabs(p1.x - p2.x) + math.fabs(p1.y - p2.y)

def getAdyacentCells(cell):
    
    adyacents = []
    for i in range(8):
        #newPoint = calculateAdyacent(point, i)
        basePoint = cell.coord
        print(basePoint.getPoint())
        if i == 0:
            basePoint.incX()
            basePoint.incY()
        elif i == 1:
            basePoint.incX()
        elif i == 2:
            basePoint.incX()
            basePoint.decY()
        elif i == 3:
            basePoint.decY()
        elif i == 4:
            basePoint.decX()
            basePoint.decY()
        elif i == 5:
            basePoint.decX()
        elif i == 6:
            basePoint.decX()
            basePoint.incY()
        else:
            basePoint.incY()
        print("newpoint: {}".format(basePoint.getPoint()))
        b = Cell(basePoint, cell.coord, 100)
        print(b.toString())
        adyacents.append(b)
    return adyacents

def calculateAdyacent(point, index):
    if index == 0:
        point.incX()
        point.incY()
    elif index == 1:
        point.incX()
    elif index == 2:
        point.incX()
        point.decY()
    elif index == 3:
        point.decY()
    elif index == 4:
        point.decX()
        point.decY()
    elif index == 5:
        point.decX()
    elif index == 6:
        point.decX()
        point.incY()
    else:
        point.incY()
    #print("pinoint: {}".format(point.getPoint()))
    return point


openList = []
closedList = []

p_i = Point(-1.4, -1.4)
p_f = Point(1.4, 1.4)

# paso 0
initialCell = Cell(p_i, p_i, 100)
print(initialCell.toString())
openList.append(initialCell)
print(len(openList))

# paso 1

c1 = openList.pop()
print(c1.toString())

closedList.append(c1)

# paso 2

print('Adyacentes')
ady = getAdyacentCells(c1)
for x in ady:
    print(x.toString())



