
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QTimeZone
# Импортируем класс приложения из основного файла
from FRAMES import MainWindow_frame, Partner_frame
from app import Application

import time


def test_app():
    window = Application()
    window.show()

    # Нажимаем кнопку
    # Имитация нажатия на кнопку add_partner_btn в классе MainWindow()
    q = QTest.mouseClick(MainWindow_frame.MainWindow(window, window).add_partner_btn, Qt.LeftButton)
    print("add new partner\n\t" + add_new_partner_negative(window))
    print("add new partner\n\t" + add_new_partner_positive(window))


    # Закрываем окно после теста
    # Значение True передается, чтобы избежать вывода MessageBox и закрыть приложение
    window.closeEvent(event=None, param=True)

def add_new_partner_negative(window):
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
    add_partner_window.add_new_partner(messageStart=False)
    return "negative test: status __COMPLETED"


def add_new_partner_positive(window):
    ''' Тестирование функции добавления нового партнера '''
    add_partner_window = Partner_frame.PartnerAddFrame(window, window)
    add_partner_window.update_start_values()

    # Имитация заполнения полей для регистрации нового пользователя
    add_partner_window.partner_name_entry.setText("Позитивный_Тест_строй")
    add_partner_window.partner_address_entry.setText("111333, Москва, ул. ТестоваяПозитивная")
    add_partner_window.partner_phone_entry.setText("9003323231")
    add_partner_window.partner_mail_entry.setText("positivetestDef@mail.ru")
    add_partner_window.partner_inn_entry.setText("9999922222")
    add_partner_window.partner_rate_entry.setText("5")
    add_partner_window.partner_type_entry.setText("ООО")
    add_partner_window.partner_director_entry.setText("Позитиный Тест Тестович")

    # Имитация нажатия левой кнопки мыши
    add_partner_window.add_new_partner(messageStart=False)
    return "positive test: status __COMPLETED"




if __name__ == "__main__":
    test_app()