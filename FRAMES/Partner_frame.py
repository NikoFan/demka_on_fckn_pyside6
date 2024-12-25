# Импорт библиотек
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QLineEdit)

from FRAMES import MainWindow_frame

from send_message_box import *
from check_input_info import *


class PartnerAddFrame(QFrame):

    def __init__(self, controller):
        '''
        Конструктор класса добавления партнера
        :param controller: экземпляр класса Application()
        '''
        QFrame.__init__(self)
        self.controller = controller
        self.db = controller.db
        self.update_start_values()

    def update_start_values(self):
        '''
        Добавление данных на фрейм
        :return: Ничего
        '''
        self.container = QVBoxLayout(self)

        title_add_window_name = QLabel(self)
        title_add_window_name.setText("Добавить партнера")
        title_add_window_name.setObjectName("Title")
        self.container.addWidget(title_add_window_name)

        # Добавление объектов на Фрейм
        self.create_text_enter_hint("Имя партнера")
        self.partner_name_entry = self.create_pattern_Qline_edit("Введите имя партнера")

        self.create_text_enter_hint("Юридический адрес партнера")
        self.partner_address_entry = self.create_pattern_Qline_edit("Введите адрес партнера")

        self.create_text_enter_hint("Телефон партнера (формат +7 9хх ххх хх хх)")
        self.partner_phone_entry = self.create_pattern_Qline_edit("")
        self.partner_phone_entry.setInputMask("+7 000 000 00 00")

        self.create_text_enter_hint("Электронная почта партнера")
        self.partner_mail_entry = self.create_pattern_Qline_edit("Введите электронную почту партнера")

        self.create_text_enter_hint("ИНН партнера")
        self.partner_inn_entry = self.create_pattern_Qline_edit("Введите ИНН партнера")
        self.partner_inn_entry.setMaxLength(10)

        self.create_text_enter_hint("Рейтинг партнера")
        self.partner_rate_entry = self.create_pattern_Qline_edit("Введите рейтинг партнера")

        self.create_text_enter_hint("Тип партнера")
        self.partner_type_entry = QComboBox()
        self.partner_type_entry.addItems(["ЗАО", "ПАО", "ОАО", "ООО"])
        self.container.addWidget(self.partner_type_entry)

        self.create_text_enter_hint("Директор партнера")
        self.partner_director_entry = self.create_pattern_Qline_edit("Введите ФИО директора партнера")

        # Создание кнопки "Добавить"
        add = QPushButton("Добавить")
        add.clicked.connect(self.add_new_partner)
        self.container.addWidget(add)

        # Создание кнопки "На главную"
        back = QPushButton("На главную")
        back.clicked.connect(
            lambda: self.controller.show_arg_frame(MainWindow_frame.MainWindow)
        )
        self.container.addWidget(back)

    # Обработчик нажатия на кнопку "Добавить"
    def add_new_partner(self, message_start: bool = False):
        '''
        Функция отправки запроса на добавление партнера в таблицу БД
        :param message_start: заглушка для тестирования
        :return: Ничего
        '''

        """ Словарь с данными из полей для ввода"""
        partner_dict_data: dict = {
            "type": self.partner_type_entry.currentText(),
            "name": self.partner_name_entry.text(),
            "director": self.partner_director_entry.text(),
            "mail": self.partner_mail_entry.text(),
            "phone": self.partner_phone_entry.text()[3:],
            "ur_addr": self.partner_address_entry.text(),
            "inn": self.partner_inn_entry.text(),
            "rate": self.partner_rate_entry.text(),
        }
        print(self.partner_phone_entry.text()[3:])
        print(check_phone(self.partner_phone_entry.text()[3:]))

        try:
            if self.db.add_partner(partner_dict_data):
                if not message_start:
                    send_information_message_box("Добавлен")
                return
            if not message_start:
                send_discard_message_box("Ошибка")
        except Exception as error_string:
            print(f"Ошибка обработки: {error_string}")
            if not message_start:
                send_discard_message_box("Ошибка")

    # Функция для создания поля дла ввода
    def create_pattern_Qline_edit(self, placeholder_message: str):
        '''
        Функция создания поля для ввода информации
        :param placeholder_message: Исчезающий текст на поле для ввода
        :return: объект класса QLineEdit(), чтобы потом из переменной считывать текст
        '''

        # Создание поля для ввода
        entry = QLineEdit()
        # Установка исчезающего текста
        entry.setPlaceholderText(placeholder_message)
        self.container.addWidget(entry)

        return entry

    # Установка подсказки над полем для ввода
    def create_text_enter_hint(self, hint_message: str):
        '''
        Функция создания текстового поля для подсказки пользователю
        :param hint_message: Подсказка пользователю
        :return: Ничего
        '''
        hint = QLabel(hint_message)
        hint.setObjectName("text_enter_hint")
        self.container.addWidget(hint)
