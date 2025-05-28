from PySide6 import QtCore, QtWidgets, QtGui
from graph_canvas import GraphWidget
from graph_lib.graph_lcd import LCDModel
from create_graph_widget import GraphInformationWidget

class LCDWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayot = QtWidgets.QVBoxLayout(self)
        self.__init_n()
        self.createButton = QtWidgets.QPushButton("Создать")
        self.mainLayot.addWidget(self.createButton)
        self.graph = GraphWidget()
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.graph,"Диаграмма графа")
        self.inf = GraphInformationWidget()
        self.tabs.addTab(self.inf,"Характеристики графа")
        self.mainLayot.addWidget(self.tabs)
        self.createButton.clicked.connect(self.__gen_plot)

    def __init_n(self):
        self.n_layout = QtWidgets.QHBoxLayout()
        self.n = QtWidgets.QLineEdit()
        self.n.setText("10")
        validator = QtGui.QIntValidator(0, 2**31 - 1)
        self.n_layout.addWidget(self.n)
        self.n_layout.addWidget(QtWidgets.QLabel("Количество вершин"))
        self.n.setValidator(validator)
        self.mainLayot.addLayout(self.n_layout)

    @QtCore.Slot()
    def __gen_plot(self):
        n = int(self.n.text())
        model = LCDModel(n)
        self.graph.new_plot(model.gp)
        self.inf.upd(model.graph)
