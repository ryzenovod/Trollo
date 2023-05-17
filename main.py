from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3

conn = sqlite3.connect('mylist.db')
c = conn.cursor()

c.execute("""CREATE TABLE if not exists todo_list(
    list_item text)
    """)

conn.commit()

conn.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(521, 365)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.additem_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_it())
        self.additem_pushButton.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.additem_pushButton.setObjectName("additem_pushButton")
        self.deleteitem_pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_it())
        self.deleteitem_pushButton_2.setGeometry(QtCore.QRect(140, 50, 141, 31))
        self.deleteitem_pushButton_2.setObjectName("deleteitem_pushButton_2")
        self.clearall_pushButton_3 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_it())
        self.clearall_pushButton_3.setGeometry(QtCore.QRect(290, 50, 101, 31))
        self.clearall_pushButton_3.setObjectName("clearall_pushButton_3")
        self.additem_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.additem_lineEdit.setGeometry(QtCore.QRect(10, 10, 501, 31))
        self.additem_lineEdit.setObjectName("additem_lineEdit")
        self.mylist_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mylist_listWidget.setGeometry(QtCore.QRect(10, 90, 501, 231))
        self.mylist_listWidget.setObjectName("mylist_listWidget")
        self.savedb_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.save_it())
        self.savedb_pushButton.setGeometry(QtCore.QRect(400, 50, 111, 31))
        self.savedb_pushButton.setObjectName("savedb_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 521, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # захват всех объектов из базы данных
        self.grab_all()

    def grab_all(self):
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()

        c.execute("SELECT * FROM todo_list")
        records = c.fetchall()

        conn.commit()

        conn.close()

        for record in records:
            self.mylist_listWidget.addItem(str(record[0]))

    def add_it(self):
        # Grab the item from the list box
        item = self.additem_lineEdit.text()

        self.mylist_listWidget.addItem(item)

        # очистка строки ввода
        self.additem_lineEdit.setText("")

    def delete_it(self):
        clicked = self.mylist_listWidget.currentRow()

        self.mylist_listWidget.takeItem(clicked)

    def clear_it(self):
        self.mylist_listWidget.clear()

    # сохранение в бд
    def save_it(self):
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()

        c.execute('DELETE FROM todo_list;', )

        # создание списка объектов
        items = []
        # вытягивание
        for index in range(self.mylist_listWidget.count()):
            items.append(self.mylist_listWidget.item(index))

        for item in items:

            c.execute("INSERT INTO todo_list VALUES (:item)",
                      {
                          'item': item.text(),
                      })

        conn.commit()

        conn.close()

        msg = QMessageBox()
        msg.setWindowTitle("Saved To Database!!")
        msg.setText("Your Todo List Has Been Saved!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "To Do List"))
        self.additem_pushButton.setText(_translate("MainWindow", "Add Item To List"))
        self.deleteitem_pushButton_2.setText(_translate("MainWindow", "Delete Item From List"))
        self.clearall_pushButton_3.setText(_translate("MainWindow", "Clear The List"))
        self.savedb_pushButton.setText(_translate("MainWindow", "Save To Database"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())