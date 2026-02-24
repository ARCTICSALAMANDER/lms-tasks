import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton


class Apimap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 0, 700, 400)
        self.setWindowTitle('Отображение картинки')
        self.setFixedSize(700, 600)

        self.shirota_input = QLineEdit(self)
        self.shirota_input.move(100, 550)
        
        ## Изображение
        self.pixmap = QPixmap()
        # Если картинки нет, то QPixmap будет пустым, 
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(80, 60)
        self.image.resize(250, 250)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)
        self.set_button = QPushButton(self)
        self.set_button.move(500, 550)
        self.set_button.resize(50, 30)
        self.set_button.setText("KEBAB")
        self.set_button.clicked.connect(self.set_shirota)

    def set_shirota(self):
        self.shirota = self.shirota_input.text()
        print(self.shirota)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Apimap()
    ex.show()
    sys.exit(app.exec())
