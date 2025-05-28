from PySide6 import QtCore, QtWidgets, QtGui
from graph_lib.graph_rnd_erdos_renyi import ErdosRenyiGraph
from graph_lib.graph_visualisation import GraphPlotter
from graph_canvas import GraphCanvas, GraphWidget
from create_graph_widget import GraphInformationWidget
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class ErdosWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.__init_p()
        self.__init_n()
        self.countButton = QtWidgets.QPushButton("Создать")
        self.mainLayout.addWidget(self.countButton)
        self.countButton.clicked.connect(self.__gen_plot)
        self.graph = GraphWidget()
        self.tabs = QtWidgets.QTabWidget(self)
        self.inf = GraphInformationWidget()
        self.tabs.addTab(self.graph, "Диаграмма графа")
        self.tabs.addTab(self.inf, "Характеристики графа")
        self.mainLayout.addWidget(self.tabs)

    def __init_p(self):
        self.pLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.pLayout)
        self.p = QtWidgets.QLineEdit()
        self.p.setText("0.3")
        validator = QtGui.QDoubleValidator(0.1, 1.0, 2)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        validator.setLocale(QtCore.QLocale(QtCore.QLocale.C))
        self.pLayout.addWidget(self.p)
        self.p.setValidator(validator)
        self.pLayout.addWidget(QtWidgets.QLabel("Вероятность выбора ребра"))

    def __init_n(self):
        self.nLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.nLayout)
        validator = QtGui.QIntValidator(1, 2**31-1)
        self.n = QtWidgets.QLineEdit()
        self.n.setText("10")
        self.n.setValidator(validator)
        self.nLayout.addWidget(self.n)
        self.nLayout.addWidget(QtWidgets.QLabel("Количество вершин"))

    @QtCore.Slot()
    def __gen_plot(self):
        p = float(self.p.text())
        n = int(self.n.text())
        g = ErdosRenyiGraph(n, p)
        self.graph.new_plot(g.visualation)
        self.inf.upd(g.graph)
