from NeighborJoining import NJ
from visualization import visualizeWeightedTree


def getData(filename):
    """
    Gets all data from file.
    :param filename: name of file.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    names = [line.split()[0] for line in lines]
    names.pop(0)
    data = [line.split()[1:] for line in lines]

    for idx, row in enumerate(data):
        data[idx] = [float(x) for x in row]

    return names, data


def printInput(names, data):
    print(f"{len(names)} populations:", names)
    print("Input data:")
    for i in range(len(names)):
        data[i].insert(0, names[i])
    names.insert(0, " ")
    data.insert(0, names)
    s = [[str(e) for e in row] for row in data]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def main(filename):
    # Datu izgūšana
    populations, data = getData(filename)
    # printInput(populations, data[1:])
    NJ(populations, data[1:])


if __name__ == '__main__':
    main("Tests/test1.txt")
