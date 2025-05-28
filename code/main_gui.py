from PySide6 import QtCore, QtWidgets, QtGui
from graph_lib.graph_rnd_erdos_renyi import ErdosRenyiGraph
from graph_lib.graph_visualisation import GraphPlotter
from graph_canvas import GraphCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from erdos_widget import ErdosWidget
from lcd_widget import LCDWidget
from bol_widget import BollobasWidget
from barabashi_widget import BarabashiWidget
from copy_widget import CopyWidget
from search_widgets import BFSWidget, DFSWidget
from chung_widget import ChungLiWidget
from create_graph_widget import CreateGraphWidget
from matplotlib.figure import Figure


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget(self)
        self.crt = CreateGraphWidget()
        self.erd = ErdosWidget()
        self.lcd = LCDWidget()
        self.bar = BarabashiWidget()
        self.bol = BollobasWidget()
        self.copy = CopyWidget()
        self.chungLi = ChungLiWidget()
        self.bfs = BFSWidget()
        self.dfs = DFSWidget()
        self.tabs.addTab(self.crt, "Создание графа")
        self.tabs.addTab(self.erd, "Модель Эрдеша-Ренье")
        self.tabs.addTab(self.lcd, "Модель LCD")
        self.tabs.addTab(self.bar, "Модель Барабаши-Альберт")
        self.tabs.addTab(self.bol, "Модель Болообаша-Риодана")
        self.tabs.addTab(self.copy, "Модель Копирования")
        self.tabs.addTab(self.chungLi, "Модель ЧунгЛи")
        self.tabs.addTab(self.bfs, "Поиск в ширину")
        self.tabs.addTab(self.dfs, "Поиск в глубину")
        self.mainLayout.addWidget(self.tabs)

        for widget in [self.crt, self.erd, self.lcd, self.bar, self.bol, self.copy, self.chungLi, self.bfs, self.dfs]:
            for btn in widget.findChildren(QtWidgets.QPushButton):
                btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                  QtWidgets.QSizePolicy.Fixed)

            for edit in widget.findChildren(QtWidgets.QLineEdit):
                edit.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                   QtWidgets.QSizePolicy.Fixed)
                edit.setMaximumWidth(200)
