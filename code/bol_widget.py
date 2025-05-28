from PySide6 import QtCore
from lcd_widget import LCDWidget
from graph_lib.graph_bollobas_riordan import BolobasRiodanModel

class BollobasWidget(LCDWidget):
    def __init__(self):
        super().__init__()
        self.createButton.clicked.disconnect()
        self.createButton.clicked.connect(self.__gen_plot)
    @QtCore.Slot()
    def __gen_plot(self):
        n =  int(self.n.text())
        bol = BolobasRiodanModel(n)
        self.graph.new_plot(bol.gp)
        self.inf.upd(bol.graph)
