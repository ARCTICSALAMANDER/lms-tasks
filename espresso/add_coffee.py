from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import sys


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(30, 10, 210, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 47, 13))
        self.label_2.setObjectName("label_2")
        self.name_text = QtWidgets.QLineEdit(parent=Form)
        self.name_text.setGeometry(QtCore.QRect(30, 60, 113, 20))
        self.name_text.setObjectName("name_text")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(30, 90, 51, 16))
        self.label_3.setObjectName("label_3")
        self.roast_text = QtWidgets.QLineEdit(parent=Form)
        self.roast_text.setGeometry(QtCore.QRect(30, 110, 113, 20))
        self.roast_text.setObjectName("roast_text")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 141, 16))
        self.label_4.setObjectName("label_4")
        self.grind_text = QtWidgets.QLineEdit(parent=Form)
        self.grind_text.setGeometry(QtCore.QRect(30, 160, 113, 20))
        self.grind_text.setObjectName("grind_text")
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setGeometry(QtCore.QRect(200, 40, 47, 13))
        self.label_5.setObjectName("label_5")
        self.taste_text = QtWidgets.QTextEdit(parent=Form)
        self.taste_text.setGeometry(QtCore.QRect(200, 60, 191, 121))
        self.taste_text.setObjectName("taste_text")
        self.label_6 = QtWidgets.QLabel(parent=Form)
        self.label_6.setGeometry(QtCore.QRect(30, 190, 81, 16))
        self.label_6.setObjectName("label_6")
        self.package_text = QtWidgets.QLineEdit(parent=Form)
        self.package_text.setGeometry(QtCore.QRect(30, 210, 113, 20))
        self.package_text.setObjectName("package_text")
        self.label_7 = QtWidgets.QLabel(parent=Form)
        self.label_7.setGeometry(QtCore.QRect(30, 240, 91, 16))
        self.label_7.setObjectName("label_7")
        self.price_text = QtWidgets.QLineEdit(parent=Form)
        self.price_text.setGeometry(QtCore.QRect(30, 260, 113, 20))
        self.price_text.setObjectName("price_text")
        self.add_btn = QtWidgets.QPushButton(parent=Form)
        self.add_btn.setGeometry(QtCore.QRect(200, 190, 75, 23))
        self.add_btn.setObjectName("add_btn")
        self.back_btn = QtWidgets.QPushButton(parent=Form)
        self.back_btn.setGeometry(QtCore.QRect(320, 10, 75, 23))
        self.back_btn.setObjectName("back_btn")
        
        self.err_label = QtWidgets.QLabel(parent=Form)
        self.err_label.setGeometry(QtCore.QRect(200, 220, 180, 20))
        self.err_label.setStyleSheet("color: red;")
        self.err_label.setText("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить/Изменить кофе"))
        self.label.setText(_translate("Form", "Добавить информацию о сорте кофе"))
        self.label_2.setText(_translate("Form", "название"))
        self.label_3.setText(_translate("Form", "прожарка"))
        self.label_4.setText(_translate("Form", "тип (молотый/в зернах)"))
        self.label_5.setText(_translate("Form", "вкус"))
        self.label_6.setText(_translate("Form", "объем пачки"))
        self.label_7.setText(_translate("Form", "цена за пачку"))
        self.add_btn.setText(_translate("Form", "Добавить"))
        self.back_btn.setText(_translate("Form", "Назад"))


class AddCoffee(QtWidgets.QWidget, Ui_Form):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        
        self.main_window = main_window
        self.coffee_data = dict()

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        self.back_btn.clicked.connect(self.go_back)
        self.add_btn.clicked.connect(self.add_coffee)

    def go_back(self):
        self.close()
        self.main_window.show()

    def add_coffee(self):
        name = self.name_text.text()
        roast = self.roast_text.text()
        coffee_type = self.grind_text.text()
        taste = self.taste_text.toPlainText()

        try:
            price = int(self.price_text.text())
            volume = int(self.package_text.text())
        except ValueError:
            self.err_label.setText("Цена и объем — числа!")
            return

        if not name or not roast or not coffee_type or not taste:
            self.err_label.setText("Не все поля заполнены")
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
        self.err_label.setStyleSheet("color: green;")
        self.err_label.setText("Успешно добавлено!")

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