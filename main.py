import io
import sys
import sqlite3

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

from udp import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon, QMovie
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, \
    QTableView
import cv2
import pyzbar.pyzbar as pyzbar

ad = ''
num = 0

t1 = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>360</width>
    <height>800</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>360</width>
    <height>0</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(43, 45, 48);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="load">
    <property name="geometry">
     <rect>
      <x>105</x>
      <y>280</y>
      <width>150</width>
      <height>50</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(255, 255, 255);
font: 75 18pt &quot;MS Shell Dlg 2&quot;;</string>
    </property>
    <property name="text">
     <string>Загрузка</string>
    </property>
   </widget>
   <widget class="QLabel" name="gif">
    <property name="geometry">
     <rect>
      <x>55</x>
      <y>338</y>
      <width>251</width>
      <height>163</height>
     </rect>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

t2 = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>360</width>
    <height>800</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>360</width>
    <height>0</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(43, 45, 48);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="ser">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>403</y>
      <width>148</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(52, 64, 130);
border: 10px;
border-color: rgb(255, 255, 255);
</string>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLabel" name="ip">
    <property name="geometry">
     <rect>
      <x>170</x>
      <y>402</y>
      <width>148</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(52, 64, 130);</string>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLabel" name="hip">
    <property name="geometry">
     <rect>
      <x>171</x>
      <y>359</y>
      <width>148</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(52, 64, 130);
color: rgb(255, 255, 255);
border-color: rgb(255, 255, 255);
font: 10pt &quot;MS Shell Dlg 2&quot;;
</string>
    </property>
    <property name="text">
     <string>IP-адрес</string>
    </property>
   </widget>
   <widget class="QLabel" name="hser">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>360</y>
      <width>148</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(52, 64, 130);
color: rgb(255, 255, 255);
font: 10pt &quot;MS Shell Dlg 2&quot;;
</string>
    </property>
    <property name="text">
     <string>Серийный №</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>220</y>
      <width>181</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">
color: rgb(255, 255, 255);
font: 15pt &quot;MS Shell Dlg 2&quot;;</string>
    </property>
    <property name="text">
     <string>Устройство</string>
    </property>
   </widget>
   <widget class="QLabel" name="back">
    <property name="geometry">
     <rect>
      <x>29</x>
      <y>360</y>
      <width>301</width>
      <height>91</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(255, 255, 255);</string>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <zorder>back</zorder>
   <zorder>ser</zorder>
   <zorder>ip</zorder>
   <zorder>hip</zorder>
   <zorder>hser</zorder>
   <zorder>label_5</zorder>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

t3 = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>360</width>
    <height>800</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>360</width>
    <height>0</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(43, 45, 48);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>130</y>
      <width>291</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">
color: rgb(255, 255, 255);
font: 15pt &quot;MS Shell Dlg 2&quot;;</string>
    </property>
    <property name="text">
     <string>История запросов</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>190</y>
      <width>321</width>
      <height>501</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(45, 59, 137)</string>
    </property>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(360, 800)
        self.setStyleSheet("background-color: rgb(43, 45, 48);")

        self.barcode_data = ''
        self.adress = ''

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

        self.scan_his.clicked.connect(self.to_his)

    def to_his(self):
        self.window = History()
        self.hide()
        self.window.show()

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
        global ad
        global num
        print(data)
        if data != 0:
            self.adress = ipipi
            num = data
            ad = self.adress
            con = sqlite3.connect("ip.sqlite")
            cur = con.cursor()
            cur.execute("INSERT INTO IP (serial_number, ip_adress) VALUES (?, ?)", (data, self.adress))
            con.commit()
        else:
            error = QMessageBox()
            error.setWindowTitle('Ошибка!')
            error.setText('Ошибка распознавания QR-кода')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec()
        self.load()

    def load(self):
        self.window = LoadScreen()
        self.hide()
        self.window.show()

    def closeEvent(self, event):
        self.camera.release()
        self.timer.stop()
        super().closeEvent(event)


class LoadScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(t1)
        uic.loadUi(f, self)
        self.pix = QPixmap('gif.png')
        self.gif.setPixmap(self.pix)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.switch_window)
        self.timer.start(3000)

    def switch_window(self):
        self.window = Device()
        self.hide()
        self.window.show()


class Device(QMainWindow):
    def __init__(self):
        global ad
        global num
        super().__init__()
        f = io.StringIO(t2)
        uic.loadUi(f, self)
        self.scan_menu = QPushButton("Сканировать", self)
        self.scan_menu.setGeometry(0, 744, 180, 56)
        self.scan_menu.setIcon(QIcon('sm.png'))
        self.scan_menu.setIconSize(QSize(24, 24))
        self.scan_menu.setStyleSheet("background-color: rgb(64, 83, 189);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 12pt \"Roboto Mono\";\n")

        self.scan_his = QPushButton("История", self)
        self.scan_his.setGeometry(180, 744, 180, 56)
        self.scan_his.setIcon(QIcon('sm.png'))
        self.scan_his.setIconSize(QSize(24, 24))
        self.scan_his.setStyleSheet("background-color: rgb(64, 83, 189);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font: 12pt \"Roboto Mono\";\n")
        self.imag_label = QLabel(self)
        self.pix = QPixmap('logo.png')
        self.imag_label.setPixmap(self.pix)
        self.imag_label.setGeometry(37, 34, 285, 67)

        self.ip.setStyleSheet("background-color: rgb(45, 59, 137);\n"
                              "color: rgb(255, 255, 255);\n"
                              "font: 10pt \"Roboto Mono\";\n")
        self.ser.setStyleSheet("background-color: rgb(45, 59, 137);\n"
                               "color: rgb(255, 255, 255);\n"
                               "font: 10pt \"Roboto Mono\";\n")
        self.ip.setText(ad)
        self.ser.setText(str(num))

        self.scan_menu.clicked.connect(self.to_main)
        self.scan_his.clicked.connect(self.to_his)

    def to_main(self):
        self.window = MainWindow()
        self.hide()
        self.window.show()

    def to_his(self):
        self.window = History()
        self.hide()
        self.window.show()


class History(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(t3)
        uic.loadUi(f, self)
        self.scan_menu = QPushButton("Сканировать", self)
        self.scan_menu.setGeometry(0, 744, 180, 56)
        self.scan_menu.setIcon(QIcon('sm.png'))
        self.scan_menu.setIconSize(QSize(24, 24))
        self.scan_menu.setStyleSheet("background-color: rgb(64, 83, 189);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 12pt \"Roboto Mono\";\n")

        self.scan_his = QPushButton("История", self)
        self.scan_his.setGeometry(180, 744, 180, 56)
        self.scan_his.setIcon(QIcon('sm.png'))
        self.scan_his.setIconSize(QSize(24, 24))
        self.scan_his.setStyleSheet("background-color: rgb(45, 59, 137);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font: 12pt \"Roboto Mono\";\n")
        self.imag_label = QLabel(self)
        self.pix = QPixmap('logo.png')
        self.imag_label.setPixmap(self.pix)
        self.imag_label.setGeometry(37, 34, 285, 67)
        self.scan_menu.clicked.connect(self.to_main)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('ip.sqlite')
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('IP')
        model.select()
        view.setModel(model)
        view.move(20, 190)
        view.resize(321, 501)
        view.setStyleSheet("background-color: rgb(52, 64, 130);"
                           "color: rgb(255, 255, 255);")

    def to_main(self):
        self.window = MainWindow()
        self.hide()
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
