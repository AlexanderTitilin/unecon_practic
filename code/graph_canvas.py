from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas
from graph_lib.graph_visualisation import GraphPlotter
from graph_lib.graph import Graph
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import gc


class GraphCanvas(FigureCanvas):
    def __init__(self, gp: GraphPlotter | None):
        if gp is None:
            self.fig = Figure((5, 5))
        else:
            self.fig = gp.gen_fig()
        super().__init__(self.fig)


class GraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.canvas = GraphCanvas(None)
        self.toolbar = NavigationToolbar(self.canvas)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.toolbar)

    def new_plot(self, gp: GraphPlotter):
        self.canvas.fig.clf()
        ax = self.canvas.fig.add_subplot(111)
        gp.draw_on_ax(ax)
        self.canvas.draw()
        gc.collect()


class DistrCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure((5, 5))
        super().__init__(self.fig)


class DistributionWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.canvas = DistrCanvas()
        self.toolbar = NavigationToolbar(self.canvas)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.toolbar)

    def new_plot(self, g: Graph):
        self.canvas.fig.clf()
        ax = self.canvas.fig.add_subplot(111)
        x = []
        y = []
        for e in g.deg_distribution():
            x.append(e.k)
            y.append(e.p)
        ax.bar(x, y)
        ax.set_xlabel("Степень вершины")
        ax.set_ylabel("Доля вершин с этой степенью")
        self.canvas.draw()
