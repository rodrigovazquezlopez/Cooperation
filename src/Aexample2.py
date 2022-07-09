
import math

# clase cell
class Cell:
    def __init__(self, coord, father, type):
        self.coord = coord
        self.father = father
        self.type = type
        self.gfunc = 0
        self.hfunc = 0
        self.ffunc = 0

    def calculateFGH(self, start, end):
        self.gfunc = math.dist(self.coord, start)
        self.hfunc = manhattanDistance(self.coord, end)
        self.ffunc = self.gfunc + self.hfunc
        
    def toString(self):
        return "Coord: {}, Father: {}, Type: {}, g(n): {}, h(n):{}, f(n): {}".format(self.coord, self.father, self.type, self.gfunc, self.hfunc, self.ffunc)

def manhattanDistance(p1, p2):
    return math.fabs(p1[0] - p2[0]) + math.fabs(p1[1] - p2[1])

def searchInCellList(list, point):
    if len(list) > 0:
        for element in list:
            if element.coord == point:
                return True
    return False

def getIndex(list, point):
    if len(list) > 0:
        for index, element in enumerate(list):
            if element.coord == point:
                return index
    return -1

def calculateAdyacents(point, index):
    delta = 10
    x = point[0]
    y = point[1]
    if index == 0:
        #x = x
        y += delta
    elif index == 1:
        x += delta
        y += delta
    elif index == 2:
        x += delta
        #y = y
    elif index == 3:
        x += delta
        y -= delta
    elif index == 4:
        #x = x
        y -= delta
    elif index == 5:
        x -= delta
        y -= delta
    elif index == 6:
        x -= delta
        #y = y
    else:
        x -= delta
        y += delta
    adyacentPoint = (x, y)
    return adyacentPoint

def generateAdyacentCells(cell, listTrajectory):   
    adyacents = []
    for i in range(8):
        type = 100
        basePoint = cell.coord
        adyPoint = calculateAdyacents(basePoint, i)
        if adyPoint in listTrajectory:
            type = 0
        adyCell = Cell(adyPoint, "null", type)
        adyacents.append(adyCell)
    return adyacents

def Aasterisk(start, end, obstacleList):
    path = []
    if start == end:
        path.append(start)
    else:
        openList = []
        closedList = []
        ended = False
        step = 0

        actual = Cell(start, "null", 100)
        print("<------------    Inicial    ------------>")
        print(actual.toString())
        openList.append(actual)

        while ended == False:
            print("\n************************* Step: {} *************************\n".format(step))

            actual = openList.pop()
            print("\n----- celda extraida -----")
            print(actual.toString())
            closedList.append(actual)

            print('\ncalculando Adyacentes')
            adyacents = generateAdyacentCells(actual, obstacleList)

            for ady in adyacents:
                ady.calculateFGH(start, end)
                ady.father = actual.coord
                if ady.coord == end:
                    print("llegamos")
                    closedList.append(ady)
                    ended = True
                    break

                elif searchInCellList(closedList, ady.coord) == True:
                    print("Está en lista cerrada")
                elif ady.type < 100:
                    print("es infranqueble")
                elif searchInCellList(openList, ady.coord) == True:
                    index = getIndex(openList, ady.coord)
                    if openList[index].gfunc > ady.gfunc:
                        openList.pop(index)
                        openList.append(ady)
                else:
                    openList.append(ady)

            openList.sort(key=lambda x: x.ffunc, reverse=True)

            print("-----------open list-----------")
            for element in openList:
                print(element.toString())

            print("\n-----------closed list-----------")
            for element in closedList:
                print(element.toString())
            step += 1
            
            #input("wait...")
        
        data = closedList.pop()
        path.insert(0, data.coord)
        while data.father != "null":
            for element in closedList:
                if element.coord == data.father:
                    path.insert(0, element.coord)
                    data = element
                    break
    
    return path


if __name__ == '__main__':
    s = (-0.4, 0.2)
    f = (1.3, 0.4)


    p_i = (s[0] * 100, s[1] * 100)
    p_f = (f[0] * 100, f[1] * 100)

    filename = "./data/twoDim/22 Feb/MovesTwoDim_22Feb2022_11.51_log.txt"
    solution = "solution.txt"

    trajectoryList = []

    # Leyendo archivo con trayectoria
    with open(filename, 'r') as file:
        for linea in file.readlines():
            tokens = linea.rsplit(', ')
            x = float(tokens[1]) * 100
            y = float(tokens[2]) * 100
            res = x % 10
            if res != 0:
                if res > 5:
                    x = x + (10 - res) 
                else:
                    x = x - res
            res = y % 10
            if res != 0:
                if res > 5:
                    y = y + (10 - res)
                else:
                    y = y - res

            points = [(x, y), (x, y + 10), (x, y - 10), (x + 10, y), (x - 10, y)]
            for element in points:
                if not element in trajectoryList:
                    trajectoryList.append(element)
    print("Trayectoria leida...")

    for element in trajectoryList:
        print(element)
    input("esperando")

    pathResult = Aasterisk(p_i, p_f, trajectoryList)

    with open(solution, 'w') as file:
        for element in pathResult:
            text = "{}, {}\n".format(element[0], element[1])
            file.write(text)
