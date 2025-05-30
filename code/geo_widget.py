from PySide6 import QtWidgets, QtGui, QtCore
from graph_lib.geo_graph_rnd import GeoGraphRndModel
from graph_lib.graph_visualisation import GraphPlotter
from graph_canvas import GraphWidget


class _GeoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self._init_radius()
        self._init_n()
        self._init_btn()
        self.canvas = GraphWidget()
        self.mainLayout.addWidget(self.canvas)

    def _init_radius(self):
        radLayout = QtWidgets.QHBoxLayout()
        self.radius = QtWidgets.QLineEdit()
        validator = QtGui.QDoubleValidator(0.1, 100.0, 1)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        validator.setLocale(QtCore.QLocale(QtCore.QLocale.C))
        self.radius.setValidator(validator)
        radLayout.addWidget(self.radius)
        radLayout.addWidget(QtWidgets.QLabel("Расстояние"))
        self.mainLayout.addLayout(radLayout)

    def _init_n(self):
        nLayout = QtWidgets.QHBoxLayout()
        self.n = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(2, 2**31 - 1)
        self.n.setValidator(validator)
        nLayout.addWidget(self.n)
        nLayout.addWidget(QtWidgets.QLabel("Количество вершин"))
        self.mainLayout.addLayout(nLayout)

    def _init_btn(self):
        layout = QtWidgets.QHBoxLayout()
        self.createButton = QtWidgets.QPushButton("Создать")
        layout.addWidget(self.createButton)
        self.mainLayout.addLayout(layout)


class GeoWidget(_GeoWidget):
    def __init__(self):
        super().__init__()
        self.createButton.clicked.connect(self.create)

    @QtCore.Slot()
    def create(self):
        n = int(self.n.text())
        r = float(self.radius.text())
        m = GeoGraphRndModel(r, n)
        self.canvas.new_plot(GraphPlotter(m.graph))
