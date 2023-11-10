from Bio import Phylo
import matplotlib
import matplotlib.pyplot as plt


def visualizeWeightedTree(filename):
    tree = Phylo.read(filename, "newick")

    fig = plt.figure(figsize=(13, 5), dpi=100)
    matplotlib.rc('font', size=12)  # fontsize of leaf and node labels
    matplotlib.rc('xtick', labelsize=10)  # fontsize of the tick labels
    matplotlib.rc('ytick', labelsize=10)  # fontsize of the tick labels
    axes = fig.add_subplot(1, 1, 1)
    Phylo.draw(tree, axes=axes)
    fig.savefig("phylip_visualization")  # save as .png file

    with open("outdrawing.txt", "w") as f:
        Phylo.draw_ascii(tree, f)

    # Tiek vaļā no liekās saknes
    with open("outdrawing.txt", "r") as f:
        lines = f.readlines()
        lines = [line[1:] for line in lines]
    with open("outdrawing.txt", "w") as f:
        f.writelines(lines)
