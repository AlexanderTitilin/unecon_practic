from PySide6 import QtWidgets, QtGui, QtCore
from graph_lib.graph import Graph
from graph_lib.graph_rnd_erdos_renyi import ErdosRenyiGraph
from graph_lib.graph_visualisation import GraphPlotter
from graph_canvas import GraphWidget


class _SearchWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self._init_n()
        self._init_start()
        self._init_buttons()
        self.canvas = GraphWidget()
        self.mainLayout.addWidget(self.canvas)

    def _init_start(self):
        startLayout = QtWidgets.QHBoxLayout()
        self.start = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(1, 2**31 - 1)
        self.start.setValidator(validator)
        startLayout.addWidget(self.start)
        startLayout.addWidget(QtWidgets.QLabel("Начальная вершина"))
        self.mainLayout.addLayout(startLayout)

    def _init_n(self):
        nLayout = QtWidgets.QHBoxLayout()
        self.n = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(1, 2**31 - 1)
        nLayout.addWidget(self.n)
        nLayout.addWidget(QtWidgets.QLabel("Количество вершин"))
        self.mainLayout.addLayout(nLayout)

    def _init_buttons(self):
        buttonLayout = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton("Старт")
        self.nextButton = QtWidgets.QPushButton("Дальше")
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.nextButton)
        self.mainLayout.addLayout(buttonLayout)


class BFSWidget(_SearchWidget):
    def __init__(self):
        super().__init__()
        self.f = True
        self.startButton.clicked.connect(self.run)
        self.nextButton.clicked.connect(self.next_state)

    @QtCore.Slot()
    def run(self):
        n = int(self.n.text())
        self.graph = ErdosRenyiGraph(n, 0.3).graph
        start = int(self.start.text())
        self.bfs = self.graph.bfs_edges(start)
        self.visited_edges = []
        self.canvas.new_plot(GraphPlotter(
            self.graph,  orange_edges=[]))

    @QtCore.Slot()
    def next_state(self):
        try:
            r = next(self.bfs)
            self.visited_edges.append(r)
            self.canvas.new_plot(GraphPlotter(
                self.graph,  orange_edges=self.visited_edges))
        except:
            pass


class DFSWidget(_SearchWidget):
    def __init__(self):
        super().__init__()
        self.f = True
        self.startButton.clicked.connect(self.run)
        self.nextButton.clicked.connect(self.next_state)


    @QtCore.Slot()
    def run(self):
        n = int(self.n.text())
        self.graph = ErdosRenyiGraph(n, 0.3).graph
        start = int(self.start.text())
        self.dfs = self.graph.dfs_edges(start)
        self.visited_edges = []
        self.canvas.new_plot(GraphPlotter(
            self.graph,  orange_edges=[]))

    @QtCore.Slot()
    def next_state(self):
        try:
            r = next(self.dfs)
            self.visited_edges.append(r)
            self.canvas.new_plot(GraphPlotter(
                self.graph,  orange_edges=self.visited_edges))
        except:
            pass
