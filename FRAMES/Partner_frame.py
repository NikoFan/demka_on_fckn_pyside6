# Импорт библиотек
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit)

from FRAMES import MainWindow_frame

from send_message_box import *
from check_input_info import *


class PartnerAddFrame(QFrame):
    ''' Класс добавления партнера '''

    def __init__(self, parent, controller):

        QFrame.__init__(self, parent)
        self.controller = controller
        self.db = controller.db

        self.container = QVBoxLayout()

        self.setLayout(self.container)


    def update_start_values(self):
        ''' Обновление стартовых значений
        Чтобы при открытии окна данные были актуальными '''

        self.title_add_window_name = QLabel(self)
        self.title_add_window_name.setText("Добавить партнера")
        self.title_add_window_name.setObjectName("Title")
        self.container.addWidget(self.title_add_window_name)


        # Добавление объектов на Фрейм
        self.create_text_enter_hint("Имя партнера")
        self.partner_name_entry = self.create_pattern_Qline_edit("Введите имя партнера")


        self.create_text_enter_hint("Юридический адрес партнера")
        self.partner_address_entry = self.create_pattern_Qline_edit("Введите адрес партнера")

        self.create_text_enter_hint("Телефон партнера (формат +7 9хх ххх хх хх)")
        self.partner_phone_entry = self.create_pattern_Qline_edit("")
        self.partner_phone_entry.setMaxLength(12)
        self.partner_phone_entry.setInputMask("+7 000 000 00 00")

        self.create_text_enter_hint("Электронная почта партнера")
        self.partner_mail_entry = self.create_pattern_Qline_edit("Введите электронную почту партнера")

        self.create_text_enter_hint("ИНН партнера")
        self.partner_inn_entry = self.create_pattern_Qline_edit("Введите ИНН партнера")
        self.partner_phone_entry.setMaxLength(10)

        self.create_text_enter_hint("Рейтинг партнера")
        self.partner_rate_entry = self.create_pattern_Qline_edit("Введите рейтинг партнера")

        self.create_text_enter_hint("Тип партнера")
        self.partner_type_entry = self.create_pattern_Qline_edit("Введите тип партнера")

        self.create_text_enter_hint("Директор партнера")
        self.partner_director_entry = self.create_pattern_Qline_edit("Введите ФИО директора партнера")


        # Создание кнопки "Добавить"
        self.add = QPushButton(self)
        self.add.setText("Добавить")
        self.add.setObjectName("add")
        self.add.clicked.connect(self.add_new_partner)
        self.container.addWidget(self.add)

        # Создание кнопки "На главную"
        self.back = QPushButton(self)
        self.back.setText("На главную")
        self.back.setObjectName("back")
        self.back.clicked.connect(self.back_to_later_window)
        self.container.addWidget(self.back)

    # Установка подсказки над полем для ввода
    def create_text_enter_hint(self, hint_message: str):
        ''' Создание подсказки для ввода текста '''
        hint = QLabel(hint_message)
        hint.setObjectName("text_enter_hint")
        self.container.addWidget(hint)

    # Обработчик нажатия на кнопку "Добавить"
    def add_new_partner(self, messageStart: bool=True):
        ''' Метод добавления нового партнера в базу данных
        messageStart - Нужна для тестирования. При передачи в нее значения False - Она запрещает
        вызывать MessageBox, и это позволяет закончить тестирование '''

        """ Словарь с данными из полей для ввода"""
        partner_dict_data: dict = {
            "type":self.partner_type_entry.text(),
            "name":self.partner_name_entry.text(),
            "director":self.partner_director_entry.text(),
            "mail":self.partner_mail_entry.text(),
            "phone":self.partner_phone_entry.text()[3:],
            "ur_addr":self.partner_address_entry.text(),
            "inn":self.partner_inn_entry.text(),
            "rate":self.partner_rate_entry.text(),
        }
        print(self.partner_phone_entry.text()[3:])
        print(check_phone(self.partner_phone_entry.text()[3:]))

        try:
            if self.db.add_partner(partner_dict_data):
                if messageStart:
                    send_information_message_box("Добавлен")
                return
            if messageStart:
                send_discard_message_box("Ошибка")
        except Exception:
            if messageStart:
                send_discard_message_box("Ошибка")

    # Функция для создания поля дла ввода
    def create_pattern_Qline_edit(self, placeholder_message: str):
        ''' Создание шаблона для ввода текста '''

        # Создание поля для ввода
        """
        self, в параметрах при создании, используется,
        чтобы создаваемый объект автоматически помещался на Используемый Фрейм
        """
        entry = QLineEdit(self)

        # Установка исчезающего текста
        entry.setPlaceholderText(placeholder_message)
        self.container.addWidget(entry)


        return entry

    # Функция для возврата на прошлый фрейм
    def back_to_later_window(self):
        ''' Открытие прошлого окна '''
        self.controller.show_arg_frame(MainWindow_frame.MainWindow)


