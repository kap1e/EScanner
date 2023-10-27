import sqlite3
import sys
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox
import cv2
import pyzbar.pyzbar as pyzbar
from udp import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 360, 800)
        self.setFixedSize(360, 800)
        self.setStyleSheet("background-color: rgb(43, 45, 48);")
        self.data = ''
        self.barcode_data = ''

        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 280)

        self.central_widget = QWidget(self)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(40, 205, 280, 277)

        self.imag_label = QLabel(self)
        self.pix = QPixmap('logo.png')
        self.imag_label.setPixmap(self.pix)
        self.imag_label.setGeometry(37, 34, 285, 67)

        self.scan_menu = QPushButton("Сканировать", self)
        self.scan_menu.setGeometry(0, 744, 180, 56)
        self.scan_menu.setIcon(QIcon('sm.png'))
        self.scan_menu.setIconSize(QSize(24, 24))
        self.scan_menu.setStyleSheet("background-color: rgb(45, 59, 137);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 12pt \"Roboto Mono\";\n")

        self.scan_his = QPushButton("История", self)
        self.scan_his.setGeometry(180, 744, 180, 56)
        self.scan_his.setIcon(QIcon('sm.png'))
        self.scan_his.setIconSize(QSize(24, 24))
        self.scan_his.setStyleSheet("background-color: rgb(64, 83, 189);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font: 12pt \"Roboto Mono\";\n")

        self.scan_button = QPushButton("Сканировать", self)
        self.scan_button.setGeometry(40, 586, 280, 63)
        self.scan_button.setStyleSheet("background-color: rgb(64, 83, 189);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "font: 18pt \"Roboto Mono\";\n"
                                       "border-radius: 23px")
        self.scan_button.clicked.connect(self.scan)

        self.setCentralWidget(self.central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 60)

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap)

    def scan(self):
        ret, frame = self.camera.read()
        if ret:
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                self.barcode_data = barcode_data
                self.decode(self.barcode_data)


    def decode(self, barcode_data):
        code = barcode_data.split(':')[2]
        codeTable = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-',
            '.', '~', '(', ')', '!', '*', '@', ',', ';'
        ]
        decBase = len(codeTable)
        j = len(code) - 1
        res = int(0)
        for i in range(0, len(code)):
            num = codeTable.index(code[i])
            res += num * pow(decBase, j)
            j -= 1
        self.data = res
        self.add_to_sql(self.data)

    def add_to_sql(self, data):
        print(data)
        if data != 0:
            adress = ipipi
            con = sqlite3.connect("ip.sqlite")
            cur = con.cursor()
            cur.execute("INSERT INTO IP (serial_number, ip_adress) VALUES (?, ?)", (data, adress))
            con.commit()
        # сюда тоже Messagebox

    def closeEvent(self, event):
        self.camera.release()
        self.timer.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
