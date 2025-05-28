from PySide6 import QtWidgets, QtCore, QtGui
from graph_lib.graph import Graph
from graph_lib.graph_visualisation import GraphPlotter
from graph_canvas import GraphWidget, DistributionWidget


class _CreateGraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget(self)
        self._init_in()
        self._init_out()
        self._init_buttons()
        self.mainLayout.addWidget(self.tabs)
        self._init_canvas()
        self.graph_inf = GraphInformationWidget()
        self.tabs.addTab(self.graph_inf, "Характеристики графа")

    def _init_in(self):
        in_layout = QtWidgets.QHBoxLayout()
        self.in_input = QtWidgets.QLineEdit()
        validador = QtGui.QIntValidator(1, 2**31 - 1)
        self.in_input.setValidator(validador)
        in_layout.addWidget(self.in_input)
        in_layout.addWidget(QtWidgets.QLabel("Введите номер вершины"))
        self.mainLayout.addLayout(in_layout)

    def _init_out(self):
        out_layout = QtWidgets.QHBoxLayout()
        self.out_input = QtWidgets.QLineEdit()
        validador = QtGui.QIntValidator(1, 2**31 - 1)
        self.out_input.setValidator(validador)
        out_layout.addWidget(self.out_input)
        out_layout.addWidget(QtWidgets.QLabel("Введите номер вершины"))
        self.mainLayout.addLayout(out_layout)

    def _init_buttons(self):
        self.addButton = QtWidgets.QPushButton("Добавить ребро")
        self.removeButtton = QtWidgets.QPushButton("Удалить ребро")
        self.clearButton = QtWidgets.QPushButton("Очистить")
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.addWidget(self.addButton)
        btnLayout.addWidget(self.removeButtton)
        btnLayout.addWidget(self.clearButton)
        self.mainLayout.addLayout(btnLayout)

    def _init_canvas(self):
        self.canvas = GraphWidget()
        self.plot = DistributionWidget()
        self.tabs.addTab(self.canvas, "Диаграмма графа")
        self.tabs.addTab(self.plot, "Диграмма Распределения")


class GraphInformationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.infoWidget = QtWidgets.QWidget()
        self.infoLayout = QtWidgets.QVBoxLayout(self.infoWidget)

        self.diameter = QtWidgets.QLabel()
        self.mean_dist = QtWidgets.QLabel()
        self.cluster_k = QtWidgets.QLabel()
        self.cluster_local = QtWidgets.QLabel()
        self.cluster_mean = QtWidgets.QLabel()
        self.connection_components = QtWidgets.QLabel()
        self.closeness = QtWidgets.QLabel()

        self.inf = [self.diameter, self.mean_dist, self.cluster_k,
                    self.cluster_mean, self.connection_components, self.cluster_local, self.closeness]

        for w in self.inf:
            w.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                            QtWidgets.QSizePolicy.Fixed)
            self.infoLayout.addWidget(w)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.infoWidget)

        self.mainLayout.addWidget(self.scroll)

    def upd(self, g: Graph):
        self.diameter.setText(f"Диаметр графа -- {g.diameter()}")
        self.mean_dist.setText(
            f"Среднее кратчайшее расстояние -- {g.mean_dist()}")
        self.cluster_k.setText(f"Коэффициент кластеризации -- {g.cluster_k()}")
        self.cluster_mean.setText(
            f"Средний коэффициент кластеризации -- {g.mean_cluster_k()}")
        self.connection_components.setText(
            f"Компоненент связности -- {len(g.connected_components())}")
        self.cluster_local.setText(self._gen_cluster_local(g))
        self.closeness.setText(self._gen_clossenses(g))

    def _gen_cluster_local(self, g: Graph):
        return "\n".join([f"Локальный коэффициент кластеризации v={v} C={g.local_cluster_k(v)}" for v in g.verticies()])

    def _gen_clossenses(self, g: Graph):
        return "\n".join([f"Степень посредничества v={v} C={g.closeness(v)}" for v in g.verticies()])

    def clear(self):
        for w in self.inf:
            w.clear()


class CreateGraphWidget(_CreateGraphWidget):
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.addButton.clicked.connect(self.add_edge)
        self.clearButton.clicked.connect(self.clear)
        self.removeButtton.clicked.connect(self.remove_edge)

    @QtCore.Slot()
    def add_edge(self):
        a = int(self.in_input.text())
        b = int(self.out_input.text())
        self.graph.add_edge(a, b)
        bridges = self.graph.find_bridges()
        self.canvas.new_plot(GraphPlotter(self.graph, orange_edges=bridges))
        self.plot.new_plot(self.graph)
        self.graph_inf.upd(self.graph)

    @QtCore.Slot()
    def remove_edge(self):
        a = int(self.in_input.text())
        b = int(self.out_input.text())
        self.graph.remove_edge(a, b)
        bridges = self.graph.find_bridges()
        self.canvas.new_plot(GraphPlotter(self.graph, orange_edges=bridges))
        self.plot.new_plot(self.graph)
        self.graph_inf.upd(self.graph)

    @QtCore.Slot()
    def clear(self):
        self.graph = Graph()
        self.canvas.new_plot(GraphPlotter(self.graph))
        self.plot.new_plot(self.graph)
        self.graph_inf.clear()
