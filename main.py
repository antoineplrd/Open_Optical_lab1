# Lab 3 - Open Optical Network
import networkx as nx
from matplotlib import pyplot as plt

from Network import Network


def main():
    network = Network()
    result = network.find_paths("A", "B")
    #network.draw()
    network.ex5()





if "__main__" == __name__:
    main()
