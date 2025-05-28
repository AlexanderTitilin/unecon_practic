from PySide6 import QtWidgets, QtGui, QtCore
from graph_canvas import GraphWidget
from create_graph_widget import GraphInformationWidget
from graph_lib.graph_barabashi_albert import BarabashiAlbertModel


class BarabashiWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.__init_n()
        self.__init_m()
        self.__init_buttons()
        self.graphWidget = GraphWidget()
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.graphWidget,"Диаграмма Графа")
        self.inf = GraphInformationWidget()
        self.tabs.addTab(self.inf,"Характеристики Графа")
        self.mainLayout.addWidget(self.tabs)

    def __init_n(self):
        self.n_layout = QtWidgets.QHBoxLayout()
        self.n = QtWidgets.QLineEdit()
        self.n.setText("10")
        validator = QtGui.QIntValidator(0, 2**31 - 1)
        self.n.setValidator(validator)
        self.n_layout.addWidget(self.n)
        self.n_layout.addWidget(QtWidgets.QLabel("Количество вершин"))
        self.mainLayout.addLayout(self.n_layout)
        self.f = False

    def __init_m(self):
        self.m_layout = QtWidgets.QHBoxLayout()
        self.m = QtWidgets.QLineEdit()
        self.m.setText("3")
        validator = QtGui.QIntValidator(0, 2**31 - 1)
        self.m.setValidator(validator)
        self.m_layout.addWidget(self.m)
        self.m_layout.addWidget(QtWidgets.QLabel("Параметр m"))
        self.mainLayout.addLayout(self.m_layout)

    def __init_buttons(self):
        self.button_layout = QtWidgets.QHBoxLayout()
        self.createButton = QtWidgets.QPushButton("создать")
        self.createButton.clicked.connect(self.__new_plot)
        self.addButton = QtWidgets.QPushButton("добавить вершину")
        self.addButton.clicked.connect(self.__add_vertex)
        self.button_layout.addWidget(self.createButton)
        self.button_layout.addWidget(self.addButton)
        self.mainLayout.addLayout(self.button_layout)

    @QtCore.Slot()
    def __new_plot(self):
        n = int(self.n.text())
        m = int(self.m.text())
        self.bar_model = BarabashiAlbertModel(n, m)
        self.f = True
        self.graphWidget.new_plot(self.bar_model.gp)
        self.inf.upd(self.bar_model.graph)

    @QtCore.Slot()
    def __add_vertex(self):
        if self.f:
            self.bar_model.add_nxt()
            self.graphWidget.new_plot(self.bar_model.gp)
            self.inf.upd(self.bar_model.graph)
