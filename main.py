import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QImage, QKeyEvent
from PyQt6.QtCore import Qt
import requests

class Mapapi(QWidget):
    def __init__(self):
        super().__init__()
        self.lat = 66
        self.long = 66
        self.scale = 15
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Maps")
        latlabel = QLabel("Широта:")
        self.latitude_edit = QLineEdit(str(self.lat))
        lonlabel = QLabel("Долгота:")
        self.longitude_edit = QLineEdit(str(self.long))
        update_button = QPushButton("↺")
        update_button.clicked.connect(self.update_map)
        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hzhz = QHBoxLayout()
        hzhz.addWidget(latlabel)
        hzhz.addWidget(self.latitude_edit)
        hzhz_long = QHBoxLayout()
        hzhz_long.addWidget(lonlabel)
        hzhz_long.addWidget(self.longitude_edit)
        vbox = QVBoxLayout()
        vbox.addLayout(hzhz)
        vbox.addLayout(hzhz_long)
        vbox.addWidget(update_button)
        vbox.addWidget(self.map_label)
        self.setLayout(vbox)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.update_map()
        self.show()

    def update_map(self):
        try:
            self.lat = float(self.latitude_edit.text())
            self.long = float(self.longitude_edit.text())
            map_url = f"https://static-maps.yandex.ru/1.x/?ll={self.long},{self.lat}&z={self.scale}&l=map"
            response = requests.get(map_url)
            response.raise_for_status()
            image = QImage.fromData(response.content)
            pixmap = QPixmap.fromImage(image)
            self.map_label.setPixmap(pixmap)
        except ValueError as e:
            self.map_label.setText(f"Ошибка: {e}")
        except requests.exceptions.RequestException as e:
            self.map_label.setText(f"Ошибка сети: {e}")
        except Exception as e:
            self.map_label.setText(f"Неизвестная ошибка: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mapapi()
    sys.exit(app.exec())
