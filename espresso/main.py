from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QWidget, QLabel, QTableView, QVBoxLayout, QApplication
import sys
import sqlite3


class Espresso(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Эспрессо")

        self.db_setup()
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.label = QLabel("Кофе info")
        self.label.setStyleSheet('''
            font-size: 25px;
            font-family: sans-serif;
        ''')
        self.mainLayout.addWidget(self.label)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffee_info')
        model.select()

        self.table = QTableView()
        self.table.resize(550, 800)
        self.table.setModel(model)
        self.mainLayout.addWidget(self.table)

        self.setLayout(self.mainLayout)

    def db_setup(self):
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        self.cur.execute('''
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

        self.cur.execute('''
            INSERT INTO coffee_info (name, roast, grind, taste, price, package)
            VALUES ("Арабика", "Средняя", "В зернах", "Вкусный", 400, 300)
        ''')

        self.cur.execute('''
            INSERT INTO coffee_info (name, roast, grind, taste, price, package)
            VALUES ("Робуста", "Темная", "Молотая", "Не очень вкусная", 700, 300)
        ''')

        self.cur.execute('''
            INSERT INTO coffee_info (name, roast, grind, taste, price, package)
            VALUES ("Арабика", "Венская", "В зернах", "яблоко, лесной орех", 250, 50)
        ''')

        self.con.commit()
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
        
