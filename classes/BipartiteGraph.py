from pathlib import Path

from matplotlib.cm import ScalarMappable
import cv2
from PIL import Image
import classes.DataImage as DataImage
import classes.Person as Person
import classes.Object as Object

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.image as mpimg
import numpy as np
import networkx as nx


class BipartiteGraph:
    GRAPH_WIDTH = 8
    GRAPH_HEIGHT = 25

    def __init__(self, persons, objects, confidence_threshold):
        self.person_nodes = []
        self.person_node_labels = {}
        self.object_nodes = []
        self.graph = nx.Graph()

        self.figure = plt.figure(figsize=(self.GRAPH_WIDTH, self.GRAPH_HEIGHT))
        self.ax = plt.subplot(111)
        self.ax.set_aspect('equal')

        self.__addPersonNodes(persons)
        self.__addObjectNodes(objects)
        self.__addRelations(persons, confidence_threshold)
        self.__drawGraph()

    def getFigure(self):
        return self.figure

    def __addPersonNodes(self, persons):
        for person in persons:
            self.graph.add_node(person.id, size=1)
            self.person_nodes.append(person.id)
            self.person_node_labels[person.id] = person.__str__()

    def __addObjectNodes(self, objects):
        for object in objects:
            filepath = object.images[0].filepath
            self.graph.add_node(object.name, filepath=filepath, size=1, label=object.name)
            self.object_nodes.append(object.name)

    def __addRelations(self, persons, confidence_threshold):
        for person in persons:
            for img in person.images:
                for prediction in img.predictions:
                    if prediction.score >= confidence_threshold:
                        self.graph.add_edge(person.id, prediction.label, weight=prediction.score)

    def __drawGraph(self):
        self.__addColorBar()
        self.__formatFigure()

        pos = self.__getNodeLayout()

        self.__drawNodes(pos)
        self.__drawEdges(pos)
        self.__placeObjectImagesOverCorrespondingNodes(pos)

    def __addColorBar(self):
        cmap = plt.get_cmap("RdYlGn")
        norm = plt.Normalize(0, 1)
        sm = ScalarMappable(norm=norm, cmap=cmap)
        # sm.set_array([])
        cbar = self.figure.colorbar(sm, orientation='horizontal', shrink=0.4, pad=-1)
        cbar.ax.set_title("Prediction score")

    def __formatFigure(self):
        plt.xlim(0, self.GRAPH_WIDTH)
        plt.ylim(0, self.GRAPH_HEIGHT)
        self.ax.axis('off')

    # There is a bipartite layout function in networkx, however, layout is not optimal for image size.
    # Therefore, this is a direct implementation
    def __getNodeLayout(self):
        x_left = 0.2
        x_right = self.GRAPH_WIDTH - 0.2

        y_start = 0.2
        y_tick_left = (self.GRAPH_HEIGHT) / (len(self.person_nodes) + 1)
        y_tick_right = (self.GRAPH_HEIGHT) / (len(self.object_nodes) + 1)

        pos = {}

        for i, person_node in enumerate(self.person_nodes):
            pos[person_node] = [x_left, y_start+i*y_tick_left]

        for i, object_node in enumerate(self.object_nodes):
            pos[object_node] = [x_right, y_start+i*y_tick_right]

        return pos

    def __drawEdges(self, pos):
        edges, weights = zip(*nx.get_edge_attributes(self.graph, 'weight').items())
        nx.draw_networkx_edges(self.graph, pos, self.graph.edges, 0.3, edge_color=weights,
                               edge_cmap=plt.cm.get_cmap('RdYlGn'), edge_vmin=0, edge_vmax=1)

    def __drawNodes(self, pos):
        nx.draw_networkx_nodes(self.graph, pos, self.object_nodes, 5)
        nx.draw_networkx_nodes(self.graph, pos, self.person_nodes, 470)
        nx.draw_networkx_labels(self.graph, pos, self.person_node_labels, font_size=4)

    def __placeObjectImagesOverCorrespondingNodes(self, pos):
        trans = self.ax.transData.transform
        trans2 = self.figure.transFigure.inverted().transform
        piesize = 0.05  # this is the image size
        p2 = piesize / 2.0
        for i, object_node in enumerate(self.object_nodes):
            xx, yy = trans(pos[object_node])  # figure coordinates
            xa, ya = trans2((xx, yy))  # axes coordinates
            # Do not know why, but coordinates of this are very weird, so do not touch
            a = plt.axes([xa - p2 + 0.02, -0.565 + i * 0.0176, piesize, piesize])
            a.set_aspect('equal')
            try:
                img = Image.open(self.graph.nodes[object_node]['filepath'])
                img.thumbnail((64, 64), Image.ANTIALIAS)
                a.imshow(img)
            except Exception as e:
                print(f'Failed to print object {object_node}')
                pass
            a.axis('off')
        self.ax.axis('off')

