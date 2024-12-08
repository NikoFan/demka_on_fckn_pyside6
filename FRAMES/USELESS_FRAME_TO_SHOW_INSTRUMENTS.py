from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Slot, QSize
from PySide6.QtWidgets import (
    QFrame,
    QStackedWidget,
    QPushButton,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QWidget)

from FRAMES import MainWindow_frame
from app import Application


class UselessFrame(QFrame):
    def __init__(self, parent, controller):
        QFrame.__init__(self, parent)
        self.controller = controller
        self.widgets_container = QVBoxLayout(QWidget(self))

        # self.update_start_values()



    def update_start_values(self):
        """ Обновление окна """


        self.cmbBox = self.create_combobox()

        # Создание Комбобокса (Выпадающего списка)

        self.widgets_container.addWidget(self.cmbBox)

        # Создание фотографии на экране
        self.picture = self.create_screen_picture()
        self.widgets_container.addWidget(self.picture)

        self.read_btn = QPushButton("Считать данные")
        self.read_btn.clicked.connect(
            lambda : print("Combobox: ", self.cmbBox.currentText())
        )

        self.back = QPushButton("Back")
        self.back.clicked.connect(
            lambda: self.controller.show_arg_frame(MainWindow_frame.MainWindow)
        )

        self.widgets_container.addWidget(self.read_btn)
        self.widgets_container.addWidget(self.back)
        self.setLayout(self.widgets_container)





    def create_combobox(self):
        """ Создание выпадающего списка """
        self.combBox = QComboBox()
        self.combBox.addItems(["Строка 1", "Строка 2", "Строка 3"])
        # self.widgets_container.addWidget(self.combBox)
        return self.combBox

    def create_screen_picture(self):
        """ Добавление фотографии на фрейм """
        self.picture_socket = QLabel(self)

        self.pixmap_picture = QPixmap(u'./res/app_icon_png.png')
        self.picture_socket.setScaledContents(True)
        self.picture_socket.setPixmap(self.pixmap_picture)
        return self.picture_socket

