from PySide6 import QtWidgets, QtCore
from graph_canvas import GraphWidget
from graph_lib.graph_chung_li_model import ChungLiModel
from graph_lib.graph_visualisation import GraphPlotter


class _ChungLiWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self._init_d()
        self._init_button()
        self.canvas = GraphWidget()
        self.mainLayout.addWidget(self.canvas)

    def _init_d(self):
        self.d = QtWidgets.QLineEdit()
        dLayout = QtWidgets.QHBoxLayout()
        dLayout.addWidget(self.d)
        dLayout.addWidget(QtWidgets.QLabel("Введите степени вершин"))
        self.mainLayout.addLayout(dLayout)

    def _init_button(self):
        self.button = QtWidgets.QPushButton("Создать")
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.addWidget(self.button)
        self.mainLayout.addLayout(btnLayout)


class ChungLiWidget(_ChungLiWidget):
    def __init__(self):
        super().__init__()
        self.button.clicked.connect(self.generate)

    @QtCore.Slot()
    def generate(self):
        d = list(map(int, self.d.text().split(",")))
        m = ChungLiModel(d)
        gp = GraphPlotter(m.graph)
        self.canvas.new_plot(gp)
