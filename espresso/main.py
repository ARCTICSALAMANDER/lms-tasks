from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QWidget, QLabel, QTableView, QVBoxLayout, QApplication, QPushButton
import sys
import sqlite3
from add_coffee import AddCoffee


class Espresso(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Эспрессо")

        self.db_setup()
        self.setupUi()

        self.add_coffee = AddCoffee(self)

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.label = QLabel("Кофе info")
        self.label.setStyleSheet('''
            font-size: 25px;
            font-family: sans-serif;
        ''')
        self.mainLayout.addWidget(self.label)

        self.reload_btn = QPushButton("перезагрузить таблицу")
        self.reload_btn.setFixedWidth(150)
        self.reload_btn.pressed.connect(self.reload_table)
        self.mainLayout.addWidget(self.reload_btn)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.sqlite')
        self.db.open()

        model = QSqlTableModel(self, self.db)
        model.setTable('coffee_info')
        model.select()

        self.table = QTableView()
        self.table.resize(550, 800)
        self.table.setModel(model)
        self.mainLayout.addWidget(self.table)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.pressed.connect(self.add_coffee_pressed)
        self.mainLayout.addWidget(self.add_btn)

        self.setLayout(self.mainLayout)

    def reload_table(self):
        model = QSqlTableModel(self, self.db)
        model.setTable('coffee_info')
        model.select()

        self.table.setModel(model)

    def add_coffee_pressed(self):
        self.hide()
        self.add_coffee.show()

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

        data = self.cur.execute('''
            SELECT * FROM coffee_info
        ''').fetchall()

        if not data:
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
        
