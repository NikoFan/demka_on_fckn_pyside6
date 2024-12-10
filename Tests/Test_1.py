import sys
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
    add_new_partner(window)


    # QTest.mouseClick(window.buttonRead, Qt.LeftButton)
    # Закрываем окно после теста
    window.close()

def add_new_partner(window):
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

    QTest.mouseClick(add_partner_window.add, Qt.LeftButton)
    print("---", Qt.Key.Key_Enter)
    QTest.keyClick(add_partner_window, 16777221)



def keyPressEvent(event):
    key = event.key()
    print("KEY:", key)



if __name__ == "__main__":
    test_app()