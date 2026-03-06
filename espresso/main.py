from PyQt6 import QtCore, QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication
import sys
import sqlite3
from add_coffee import AddCoffee


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 31))
        self.label.setObjectName("label")
        self.tableView = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 50, 781, 461))
        self.tableView.setObjectName("tableView")
        
        self.add_btn = QtWidgets.QPushButton("Добавить", parent=self.centralwidget)
        self.add_btn.setGeometry(QtCore.QRect(10, 520, 100, 30))
        
        self.reload_btn = QtWidgets.QPushButton("Обновить", parent=self.centralwidget)
        self.reload_btn.setGeometry(QtCore.QRect(120, 520, 100, 30))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Эспрессо - Главная"))
        self.label.setText(_translate("MainWindow", "Информация о кофе"))


class Espresso(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db_setup()
        self.init_db_model()

        self.add_coffee_window = AddCoffee(self)

        self.add_btn.clicked.connect(self.add_coffee_pressed)
        self.reload_btn.clicked.connect(self.reload_table)

    def init_db_model(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.sqlite')
        if not self.db.open():
            print("Не удалось открыть базу данных")
            return

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('coffee_info')
        self.model.select()
        
        self.tableView.setModel(self.model)

    def reload_table(self):
        self.model.select()

    def add_coffee_pressed(self):
        self.hide()
        self.add_coffee_window.show()

    def db_setup(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS coffee_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roast TEXT NOT NULL,
                grind TEXT NOT NULL,
                taste TEXT NOT NULL,
                price INT NOT NULL,
                package INT NOT NULL
            )
        ''')

        data = cur.execute('SELECT * FROM coffee_info').fetchone()
        if not data:
            cur.execute('''
                INSERT INTO coffee_info (name, roast, grind, taste, price, package)
                VALUES 
                ("Арабика", "Средняя", "В зернах", "Вкусный", 400, 300),
                ("Робуста", "Темная", "Молотая", "Не очень вкусная", 700, 300),
                ("Арабика", "Венская", "В зернах", "яблоко, лесной орех", 250, 50)
            ''')
            con.commit()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())