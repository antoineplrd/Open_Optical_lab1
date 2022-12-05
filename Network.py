import json
from math import *
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
from Node import Node
from Line import Line
from Signal_information import Signal_information


class Network:
    def __init__(self):
        self._nodes = dict()
        self._lines = dict()
        self.connect()

    def connect(self):
        open_Json = open("nodes.json", "r")
        data = json.loads(open_Json.read())

        for i in data:
            label = i
            connected_nodes = list()
            connected_lines = list()

            for k in data[i]["position"]:
                connected_lines.append(k)
            for j in data[i]["connected_nodes"]:
                # implementation for line between 2 nodes: AB, BA
                connected_nodes.append(j)
            node = Node(label, (connected_lines[0], connected_lines[1]), connected_nodes)
            self._nodes.update({label: node})

        open_Json.close()

        for i in self._nodes:
            # length between 2 nodes
            labelX = self._nodes.get(i).position[0]
            labelY = self._nodes.get(i).position[1]
            for j in self._nodes.get(i).connected_nodes:
                label_lines = i + j
                nextNodeX = self._nodes.get(j).position[0]
                nextNodeY = self._nodes.get(j).position[1]
                Distance_lines = sqrt((nextNodeX - labelX) ** 2 + (nextNodeY - labelY) ** 2)

                line = Line(label_lines, Distance_lines)
                self._lines.update({label_lines: line})

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, lines):
        self._lines = lines

    def find_paths(self, start_node, end_node, path=[]):

        graph_dict = self._nodes.get(start_node).connected_nodes
        path = path + [start_node]
        if start_node == end_node:
            return [path]
        paths = []
        for actual_node in graph_dict:
            if actual_node not in path:
                extended_paths = self.find_paths(actual_node, end_node, path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def propagate(self, signal_information):
        path = signal_information.path
        for i in path:
            self._nodes.get(i).propagate(signal_information)
            #self._lines.get(i).propagate(signal_information)

    def draw(self):
        G = nx.Graph()
        for i in self._nodes:
            G.add_nodes_from(self._nodes.get(i).label, pos=(self._nodes.get(i).position[0],
                                                            self._nodes.get(i).position[1]))
        for j in self._lines:
            G.add_edges_from([(j[0], j[1])])
        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True)
        plt.show()

    def ex5(self):
        var = list()
        path = list()

        for i in self._nodes:
            for j in self._nodes:
                if not (var.__contains__((i, j)) or var.__contains__((j, i)) or i == j):
                    var.append((i, j))
                    path.append(self.find_paths(i, j))

        flat_list = []
        # iterating over the data
        for item in path:
            # appending elements to the flat_list
            flat_list += item
        signal_information = Signal_information(0.001, ['A', 'B'])
        self.propagate(signal_information)

        data = {
            "all paths": flat_list,
           # "latency": signal_information.latency
        }
        df = pd.DataFrame(data)
        print(df)
