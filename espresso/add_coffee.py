from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QTextEdit, QLineEdit, QPushButton)
import sys
import sqlite3


class AddCoffee(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__()
        self.setGeometry(300, 300, 650, 450)
        self.setWindowTitle("Эспрессо")

        self.main_window = main_window
        self.coffee_data = dict()

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        self.setup_ui()

    def setup_ui(self):
        self.full_layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()

        self.title_label = QLabel("Добавить запись о кофе")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.back_btn = QPushButton("Назад")
        self.back_btn.setFixedWidth(80)
        self.back_btn.pressed.connect(self.go_back)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.back_btn)

        self.full_layout.addLayout(self.header_layout)

        self.content_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()

        self.name_label = QLabel("Название")
        self.name_text = QLineEdit()

        self.roast_label = QLabel("Обжарка")
        self.roast_text = QLineEdit()

        self.type_label = QLabel("Тип (молотый/в зернах)")
        self.type_text = QLineEdit()

        self.price_label = QLabel("Цена за упаковку")
        self.price_text = QLineEdit()

        self.volume_label = QLabel("Объем упаковки")
        self.volume_text = QLineEdit()

        widgets = [
            self.name_label, self.name_text,
            self.roast_label, self.roast_text,
            self.type_label, self.type_text,
            self.price_label, self.price_text,
            self.volume_label, self.volume_text
        ]

        for w in widgets:
            if isinstance(w, QLineEdit):
                w.setFixedHeight(30)
            self.left_layout.addWidget(w)

        self.left_layout.addStretch()

        self.right_layout = QVBoxLayout()

        self.taste_label = QLabel("Вкус")
        self.taste_text = QTextEdit()
        self.taste_text.setMinimumWidth(250)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.setFixedHeight(40)
        self.add_btn.setStyleSheet(
            "font-weight: bold; background-color: #f0f0f0;")
        self.add_btn.pressed.connect(self.add_coffee)

        self.err_label = QLabel("")
        self.err_label.setStyleSheet("color: red;")

        self.right_layout.addWidget(self.taste_label)
        self.right_layout.addWidget(self.taste_text)
        self.right_layout.addWidget(self.add_btn)
        self.right_layout.addWidget(self.err_label)

        self.content_layout.addLayout(self.left_layout, stretch=1)
        self.content_layout.addLayout(self.right_layout, stretch=1)

        self.full_layout.addLayout(self.content_layout)

    def go_back(self):
        self.close()
        self.main_window.show()

    def add_coffee(self):
        name = self.name_text.text()
        roast = self.roast_text.text()
        coffee_type = self.type_text.text()

        try:
            price = int(self.price_text.text())
            volume = int(self.volume_text.text())
        except ValueError:
            self.err_label.setText("не все поля заполнены")
            return

        taste = self.taste_text.toPlainText()

        if not name or not roast or not coffee_type or not taste:
            self.err_label.setText("не все поля заполнены")
            return

        self.coffee_data = {
            'name': name,
            'roast': roast,
            'type': coffee_type,
            'price': price,
            'volume': volume,
            'taste': taste
        }

        self.add_coffee_to_db()

        self.err_label.setText("Добавлено!")

    def add_coffee_to_db(self):
        if self.coffee_data:
            self.cur.execute('''
                INSERT INTO coffee_info (name, roast, grind, taste, price, package)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.coffee_data['name'], 
                  self.coffee_data['roast'], 
                  self.coffee_data['type'], 
                  self.coffee_data['taste'], 
                  self.coffee_data['price'], 
                  self.coffee_data['volume']))
            
            self.con.commit()