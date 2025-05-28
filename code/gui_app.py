#!/bin/python
from PySide6 import QtWidgets
from main_gui import MainWindow


def main():
    app = QtWidgets.QApplication()
    w = MainWindow()
    w.show()
    app.exec()


main()
