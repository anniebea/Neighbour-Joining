import pandas as pd
import numpy as np


def getData(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    names = [line.split()[0] for line in lines]
    names.pop(0)
    data = [line.split()[1:] for line in lines]
    for idx, row in enumerate(data):
        data[idx] = [float(x) for x in row]
    return names, data


def main(filename):
    populations, data = getData(filename)
    NJ(populations, data[1:])


def NJ(popNames, data):
    adjacencyList = list()
    distanceList = list()
    newNode = 0
    for idx, i in enumerate(popNames):
        adjacencyList.append(["__central_node__", i])
        for jdx, j in enumerate(popNames):
            if i < j:
                distanceList.append([i, j, data[idx][jdx]])

    while True:
        Q = [[0 for i in range(len(popNames))] for j in range(len(popNames))]
        for idx, i in enumerate(popNames):
            for jdx, j in enumerate(popNames):
                if i != j:
                    Q[idx][jdx] = (len(popNames) - 2) * data[idx][jdx]
                    Qsum = 0
                    for kdx, k in enumerate(popNames):
                        Qsum += data[idx][kdx]
                    Q[idx][jdx] -= Qsum
                    Qsum = 0
                    for kdx, k in enumerate(popNames):
                        Qsum += data[kdx][jdx]
                    Q[idx][jdx] -= Qsum

        npQ = np.array(Q)
        minQ = np.argwhere(npQ == np.min(npQ)).tolist()
        minX, minY = minQ[0]
        minVal = Q[minX][minY]

        newNode += 1
        adjacencyList.append(["__central_node__", str(newNode)])
        adjacencyList.append([str(newNode), popNames[minX]])
        adjacencyList.append([str(newNode), popNames[minY]])
        adjacencyList.remove(["__central_node__", popNames[minX]])
        adjacencyList.remove(["__central_node__", popNames[minY]])

        if len(popNames) == 2:
            distanceList.append([popNames[0], popNames[1], data[0][1]])
            adjacencyList.append([popNames[1], popNames[0]])
            adjacencyList.remove(["__central_node__", str(newNode)])
            adjacencyList.remove([str(newNode), popNames[minX]])
            adjacencyList.remove([str(newNode), popNames[minY]])
            del data[1]
            del data[0]
            del popNames[1]
            del popNames[0]

            deletable = []
            for elem in enumerate(distanceList):
                if [elem[1][0], elem[1][1]] not in adjacencyList and [elem[1][1], elem[1][0]] not in adjacencyList:
                    deletable.append(distanceList[elem[0]])
            distanceList = [elem for elem in distanceList if elem not in deletable]
            deletable = []
            for l1 in distanceList[:-1]:
                for l2 in distanceList[len(l1) - 1:]:
                    if l1[0] == l2[1] and l1[1] == l2[0]:
                        deletable.append(l2)
            distanceList = [elem for elem in distanceList if elem not in deletable]
            break

        sumX = 0
        sumY = 0
        for k in range(len(popNames)):
            sumX += data[minX][k]
            sumY += data[k][minY]
        distance = 0.5 * data[minX][minY] + 0.5 / (len(popNames) - 2) * (sumX - sumY)
        distanceList.append([str(newNode), popNames[minX], distance])
        distanceList.append([str(newNode), popNames[minY], data[minX][minY] - distance])

        for kdx, k in enumerate(popNames):
            if k != popNames[minX] and k != popNames[minY]:
                distance = 0.5 * (data[minX][kdx] + data[minY][kdx] - data[minX][minY])
                distanceList.append([str(newNode), k, distance])

        if minX > minY:
            del data[minX]
            del data[minY]
        else:
            del data[minY]
            del data[minX]

        if minX > minY:
            for idx, row in enumerate(data):
                del row[minX]
                del row[minY]
                row.append(distanceList[-(len(popNames) - 2):][idx][2])
        else:
            for idx, row in enumerate(data):
                del row[minY]
                del row[minX]
                row.append(distanceList[-(len(popNames) - 2):][idx][2])

        newRow = [entry[2] for entry in distanceList[-(len(popNames) - 2):]]
        newRow.append(float(0))
        data.append(newRow)

        popNames.append(str(newNode))
        if minX > minY:
            del popNames[minX]
            del popNames[minY]
        else:
            del popNames[minY]
            del popNames[minX]

    phyOutput = convertToOneLine(distanceList, newNode - 1)
    with open("outtree.txt", 'w') as f:
        f.write(phyOutput)
    return distanceList


def convertToOneLine(distances, number):
    fragments = []
    for i in range(1, number):
        for pop1 in distances:
            if pop1[0] == str(i):
                for pop2 in distances:
                    if pop2 != pop1 and pop2[0] == str(i):
                        fragment = "(" + pop1[1] + ":" + "{:.5f}".format(pop1[2]) + "," + pop2[1] + ":" + "{:.5f}".format(pop2[2]) + ")"
                        distances.remove(pop1)
                        distances.remove(pop2)
        fragments.append(fragment)
    treeString = ("(" + distances[0][1] + ":" + "{:.5f}".format(distances[0][2]) + ","
                  + distances[1][1] + ":" + "{:.5f}".format(distances[1][2]) + ","
                  + distances[2][1] + ":" + "{:.5f}".format(distances[2][2]) + ");")
    for i in range(number - 1, 0, -1):
        treeString = treeString.replace(str(i) + ":", fragments[i - 1] + ":")
    return treeString


def prettyPrintDistanceList(distances):
    s = [[str(e) for e in row] for row in distances]
    s.insert(0, ["-------", "---", "------"])
    s.insert(0, ["Between", "And", "Length"])
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


if __name__ == '__main__':
    main("infile.txt")
