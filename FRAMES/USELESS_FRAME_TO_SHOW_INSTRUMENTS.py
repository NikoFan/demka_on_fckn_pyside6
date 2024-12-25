from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QWidget)

from FRAMES import MainWindow_frame



""" Класс для демонстрации тех инструментов, которые мы не затронули
НО они могут быть на самом экзамене """

class UselessFrame(QFrame):
    def __init__(self, parent, controller):
        QFrame.__init__(self, parent)
        self.controller = controller
        self.widgets_container = QVBoxLayout(self)

        self.update_start_values()




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

        self.picture_socket.setFixedSize(100, 100)
        return self.picture_socket



    # Очистка старого контейнера
    # def clear_layout(self):
    #     """ Очистка контейнера с элементами (QLineEdit, QPushButton и т.д.),
    #     чтобы он не хранил в себе старые виджеты """
    #
    #     # Очистка контейнера от старых элементов
    #     """
    #     Проблема вся в том, что если создавать QVBoxLayout() в функции обновления -
    #     строки для ввода не будут передавать новый текст
    #
    #     Для этого надо создавать его в __init__() функции
    #     НО если не очистить его, то каждое упоминание класса будет создавать строки и хранить их в Контекнере
    #     Для этого контейнер чистится перед запуском файла
    #     """
    #     for i in reversed(range(self.container.count())):
    #
    #         # Считывается виджет из контейнера по ID
    #         widget = self.container.itemAt(i).widget()
    #
    #         # Проверка, что виджет не пустой
    #         if widget is not None:
    #             # Удаление виджета
    #             widget.deleteLater()
