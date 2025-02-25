import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.cm import ScalarMappable
from sklearn.cluster import KMeans


class BipartiteGraph:
    GRAPH_WIDTH = 8
    GRAPH_HEIGHT = 25

    def __init__(self, persons, objects, confidence_threshold, k):
        self.person_nodes = []
        self.person_node_labels = {}
        self.object_nodes = []
        self.graph = nx.Graph()

        self.figure = plt.figure(figsize=(self.GRAPH_WIDTH, self.GRAPH_HEIGHT))
        self.ax = plt.subplot(111)
        self.ax.set_aspect("equal")

        self.__addPersonNodes(persons)
        self.__addObjectNodes(objects)
        self.__addRelations(persons, objects, confidence_threshold, k)
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
            self.graph.add_node(
                object.name, filepath=str(filepath), size=1, label=object.name
            )
            self.object_nodes.append(object.name)

    def __addRelations(self, persons, objects, confidence_threshold, k):
        persons_with_total_item_scores = pd.DataFrame(
            0, index=np.arange(40), columns=[obj.name for obj in objects]
        )
        for person in persons:
            for img in person.images:
                for prediction in img.predictions:
                    persons_with_total_item_scores.loc[
                        int(person.id) - 1, prediction.label
                    ] += prediction.score
                    if prediction.score >= confidence_threshold:
                        self.graph.add_edge(
                            person.id, prediction.label, weight=prediction.score
                        )
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(persons_with_total_item_scores)
        self.person_node_colors = kmeans.predict(persons_with_total_item_scores)

    def __drawGraph(self):
        self.__addColorBar()
        self.__formatFigure()

        pos = self.getNodeLayout()

        self.__drawNodes(pos)
        self.__drawEdges(pos)

    def __addColorBar(self):
        cmap = plt.get_cmap("RdYlGn")
        norm = plt.Normalize(0, 1)
        sm = ScalarMappable(norm=norm, cmap=cmap)
        # sm.set_array([])
        cbar = self.figure.colorbar(sm, orientation="horizontal", shrink=0.4, pad=-1)
        cbar.ax.set_title("Prediction score")

    def __formatFigure(self):
        plt.xlim(0, self.GRAPH_WIDTH)
        plt.ylim(0, self.GRAPH_HEIGHT)
        self.ax.axis("off")

    # There is a bipartite layout function in networkx, however, layout is not optimal for image size.
    # Therefore, this is a direct implementation
    def getNodeLayout(self):
        x_left = 0.2
        x_right = self.GRAPH_WIDTH - 0.2

        y_start = 0.2
        y_tick_left = (self.GRAPH_HEIGHT) / (len(self.person_nodes) + 1)
        y_tick_right = (self.GRAPH_HEIGHT) / (len(self.object_nodes) + 1)

        pos = {}

        for i, person_node in enumerate(self.person_nodes):
            pos[person_node] = [x_left, y_start + i * y_tick_left]

        for i, object_node in enumerate(self.object_nodes):
            pos[object_node] = [x_right, y_start + i * y_tick_right]

        return pos

    def __drawEdges(self, pos):
        edges, weights = zip(*nx.get_edge_attributes(self.graph, "weight").items())
        nx.draw_networkx_edges(
            self.graph,
            pos,
            self.graph.edges,
            0.3,
            edge_color=weights,
            edge_cmap=plt.cm.get_cmap("RdYlGn"),
            edge_vmin=0,
            edge_vmax=1,
        )

    def __drawNodes(self, pos):
        nx.draw_networkx_nodes(self.graph, pos, self.object_nodes, 5)
        nx.draw_networkx_nodes(
            self.graph, pos, self.person_nodes, 470, node_color=self.person_node_colors
        )
        nx.draw_networkx_labels(self.graph, pos, self.person_node_labels, font_size=4)
