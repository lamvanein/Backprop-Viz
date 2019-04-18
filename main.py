# Input file
from tree import *
#from parser import variableNameParsing
from app_ui import Ui_MainWindow
from abc import ABC
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import sys
import re


# program running
def variableNameParsing(txt: str):
    ret = list()
    regex = r"[A-Za-z]+"
    matches = re.finditer(regex, txt, re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        ret.append(match.group())

    return ret


class Observer(ABC):
    def notify(self, data):
        pass

# Observe input table


class ObservableTable(Observer):
    def __init__(self, ui: QtWidgets.QTableWidget):
        self.ui = ui
        self.dict = dict()

        # connect event
        self.ui.itemChanged.connect(self.updateDict)

    def notify(self, data):
        variables = variableNameParsing(data)
        self.ui.setRowCount(len(variables))
        for index, variable in enumerate(variables):
            key = QTableWidgetItem(variable)
            value = QTableWidgetItem(
                self.dict[variable] if variable in self.dict else "0")
            self.ui.setItem(index, 0, key)
            self.ui.setItem(index, 1, value)

        # self.ui.resizeColumnsToContents()
        # self.ui.resizeRowsToContents()
        self.ui.show()

    def updateDict(self, item):
        row = item.row()
        col = item.column()
        if col == 1:
            print(item.text())
            key = self.ui.item(row, 0).text()
            value = item.text()
            self.dict[key] = value


# Observe treeview


class ObservableView(Observer):
    def __init__(self, ui: QtWidgets):
        self.ui = ui

    def notify(self, data):
        return data


class ObserversCollection:
    def __init__(self):
        self.collection = list()  # list of observer

    def registerObserver(self, obj: Observer):
        return self.collection.append(obj)

    def unregisterObserver(self, index: int):
        return self.collection.remove(index)  # not running but we assume

    def notifyObservers(self, data):  # trigger when event
        for observer in self.collection:
            observer.notify(data)
        return


class Application:
    def __init__(self, tree: Tensor):
        # can recompile this without changing the code. Can apply Adapter
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # Setup data
        self.observerCollection = self.initObservers()
        self.tree = tree

        # setup connect
        self.ui.textEdit.textChanged.connect(self.inputChange)
        # self.ui.pushButton.clicked.connect()

    def initObservers(self):
        collection = ObserversCollection()
        collection.registerObserver(ObservableTable(self.ui.tableWidget))
        collection.registerObserver(ObservableView(self.ui.treeViewWidget))
        return collection

    def inputChange(self, *args):  # trigger when textinput data changed
        # parse new Tree
        self.tree = "abc"
        # notify
        data = self.ui.textEdit.toPlainText()
        self.observerCollection.notifyObservers(data)

    def render(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    # Setup UI
    App = Application("")
    App.render()