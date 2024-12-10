import sys
from multiprocessing.pool import CLOSE

import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QFrame, QMessageBox
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QTimeZone
  # Импортируем класс приложения из основного файла
from FRAMES import MainWindow_frame, Partner_frame
from app import Application

import time


def test_app():
    app = QApplication(sys.argv)
    window = Application()
    window.show()

    # Нажимаем кнопку
    # Имитация нажатия на кнопку add_partner_btn в классе MainWindow()
    q = QTest.mouseClick(MainWindow_frame.MainWindow(window, window).add_partner_btn, Qt.LeftButton)
    add_new_partner(window, app)


    # QTest.mouseClick(window.buttonRead, Qt.LeftButton)
    # Закрываем окно после теста
    window.closeEvent(event=None, param=True)

def add_new_partner(window, app):
    ''' Тестирование функции добавления нового партнера '''
    add_partner_window = Partner_frame.PartnerAddFrame(window, window)
    add_partner_window.update_start_values()

    # Имитация заполнения полей для регистрации нового пользователя
    add_partner_window.partner_name_entry.setText("Тест_строй")
    add_partner_window.partner_address_entry.setText("111333, Москва, ул. Тестовая")
    add_partner_window.partner_phone_entry.setText("--")
    add_partner_window.partner_mail_entry.setText("testDef@mail.ru")
    add_partner_window.partner_inn_entry.setText("9999911111")
    add_partner_window.partner_rate_entry.setText("4")
    add_partner_window.partner_type_entry.setText("ОАО")
    add_partner_window.partner_director_entry.setText("Тестов Тест Тестович")

    # Имитация нажатия левой кнопки мыши

    # QTest.mouseClick(add_partner_window.add, Qt.LeftButton)
    add_partner_window.add_new_partner(messageStart=False)
    # app.aboutToQuit.connect(handle_message_box)
    # QTest.qWait(3000)  # Подождем 100 миллисекунд (можно настроить по необходимости)
    #
    # # Пытаемся найти QMessageBox и нажать кнопку Yes
    # reply = app.activePopupWidget()  # Получаем активное модальное окно
    # if isinstance(reply, QMessageBox):
    #     QTest.mouseClick(reply.button(QMessageBox.Yes), Qt.LeftButton)

def handle_message_box():
    print(123)


if __name__ == "__main__":
    test_app()