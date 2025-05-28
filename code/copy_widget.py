from PySide6 import QtCore, QtWidgets, QtGui
from graph_lib.graph_cop_model import CopyModel
from graph_lib.graph_visualisation import GraphPlotter
from graph_canvas import GraphWidget
from create_graph_widget import GraphInformationWidget


class __CopyWidgetEmpty(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.init_d()
        self.init_alpha()
        self.init_buttons()
        self.canvas = GraphWidget()
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.canvas,"Диаграмма графа")
        self.inf = GraphInformationWidget()
        self.tabs.addTab(self.inf,"Характеристики графа")
        self.mainLayout.addWidget(self.tabs)

    def init_d(self):
        self.d_layout = QtWidgets.QHBoxLayout()
        self.d = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(2, 2**31 - 1)
        self.d.setValidator(validator)
        self.d_layout.addWidget(self.d)
        self.d_layout.addWidget(QtWidgets.QLabel("Введите параметр d"))
        self.mainLayout.addLayout(self.d_layout)

    def init_alpha(self):
        self.alpha_layout = QtWidgets.QHBoxLayout()
        self.alpha = QtWidgets.QLineEdit()
        validator = QtGui.QDoubleValidator(0.1, 1.0, 2)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        validator.setLocale(QtCore.QLocale(QtCore.QLocale.C))
        self.alpha.setValidator(validator)
        self.alpha_layout.addWidget(self.alpha)
        self.alpha_layout.addWidget(QtWidgets.QLabel("Введите параметр α"))
        self.mainLayout.addLayout(self.alpha_layout)

    def init_buttons(self):
        self.createButton = QtWidgets.QPushButton("Создать")
        self.addButton = QtWidgets.QPushButton("Добавить вершину")
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.createButton)
        button_layout.addWidget(self.addButton)
        self.mainLayout.addLayout(button_layout)


class CopyWidget(__CopyWidgetEmpty):
    def __init__(self):
        super().__init__()
        self.f = False
        self.createButton.clicked.connect(self.create)
        self.addButton.clicked.connect(self.add)

    @QtCore.Slot()
    def create(self):
        self.f = True
        d = int(self.d.text())
        alpha = float(self.alpha.text())
        self.model = CopyModel(alpha, d)
        self.canvas.new_plot(GraphPlotter(self.model.graph))
        self.inf.upd(self.model.graph)

    @QtCore.Slot()
    def add(self):
        if self.f:
            self.model.add_vertex()
            self.canvas.new_plot(GraphPlotter(self.model.graph))
            self.inf.upd(self.model.graph)
