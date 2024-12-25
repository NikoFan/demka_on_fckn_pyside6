# Импорт библиотек
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QComboBox)

# Импорт классов
from FRAMES import Partner_information_frame
from send_message_box import *
from check_input_info import *


class PartnerUpdateFrame(QFrame):

    def __init__(self, controller):
        '''
        Конструктор класса обновления партнерской информации
        :param controller: экземпляр класса Application()
        '''
        QFrame.__init__(self)
        # Инициализация переменных
        self.controller = controller
        self.db = controller.db

        self.update_start_values()

    # Обновление информации на фрейме
    def update_start_values(self):
        '''
        Добавление данных на фрейм
        :return: Ничего
        '''
        self.container = QVBoxLayout(self)

        # Получение стартовых данных о партнере
        """
        Полученные данные будут установлены в качестве стартовых в поля для ввода
        """
        partner_late_info = self.db.get_partner_by_name(Partner.get_name())

        # Создание заголовка окна
        title_add_window_name = QLabel()
        title_add_window_name.setText("Обновить партнера")

        # Установка имени объекта, к которому уже есть стиль Заголовка
        title_add_window_name.setObjectName("Title")

        # Добавление заголовка в контейнер
        self.container.addWidget(title_add_window_name)

        # Создание строк для ввода
        """ Строки создаются по единому стандарту в функции self.create_pattern_Qline_edit() """
        self.create_text_enter_hint("Имя партнера")
        self.partner_name_entry = self.create_pattern_Qline_edit(partner_late_info['name'].strip())

        self.create_text_enter_hint("Юридический адрес партнера")
        self.partner_address_entry = self.create_pattern_Qline_edit(partner_late_info['ur_addr'].strip())

        self.create_text_enter_hint("Телефон партнера (формат +7 9хх ххх хх хх)")
        self.partner_phone_entry = self.create_pattern_Qline_edit(partner_late_info['phone'].strip())
        # Установка маски для ввода
        self.partner_phone_entry.setInputMask("+7 000 000 00 00")

        self.create_text_enter_hint("Электронная почта партнера")
        self.partner_mail_entry = self.create_pattern_Qline_edit(partner_late_info['mail'].strip())

        self.create_text_enter_hint("ИНН партнера")
        self.partner_inn_entry = self.create_pattern_Qline_edit(partner_late_info['inn'].strip())
        self.partner_phone_entry.setMaxLength(10)

        self.create_text_enter_hint("Рейтинг партнера")
        self.partner_rate_entry = self.create_pattern_Qline_edit(partner_late_info['rate'])

        self.create_text_enter_hint("Тип партнера")
        self.combobox_type = QComboBox()
        self.combobox_type.addItems(["ЗАО", "ООО", "ПАО", "ОАО"])
        self.container.addWidget(self.combobox_type)

        self.create_text_enter_hint("Директор партнера")
        self.partner_director_entry = self.create_pattern_Qline_edit(partner_late_info['director'].strip())

        # Создание кнопки "Добавить"
        update = QPushButton("Обновить")
        update.clicked.connect(self.update_partner_information)
        self.container.addWidget(update)

        # Создание кнопки "На главную"
        back = QPushButton("Назад")
        back.clicked.connect(self.back_to_later_window)
        self.container.addWidget(back)

    # Установка текста подсказки над полем для ввода
    def create_text_enter_hint(self, hint_message: str):
        '''
        Функция создания текста-подсказки для пользователя
        :param hint_message: текст-подсказка
        :return: Ничего
        '''
        hint = QLabel(hint_message)
        hint.setObjectName("text_enter_hint")
        self.container.addWidget(hint)

    # Обработчик нажатий на кнопку "Обновить"
    def update_partner_information(self, no_message_for_test: bool = False):
        '''
        Функция отправки запроса на обновление пользователя в таблице
        :param no_message_for_test: Заглушка для текстирования
        :return: Ничего
        '''

        partner_dict_data: dict = {
            "type": self.combobox_type.currentText(),
            "name": self.partner_name_entry.text(),
            "director": self.partner_director_entry.text(),
            "mail": self.partner_mail_entry.text(),
            "phone": self.partner_phone_entry.text()[3:],
            "ur_addr": self.partner_address_entry.text(),
            "inn": self.partner_inn_entry.text(),
            "rate": self.partner_rate_entry.text(),
        }
        print(partner_dict_data)
        print(self.partner_phone_entry.text()[3:])
        print(check_phone(self.partner_phone_entry.text()[3:]))

        try:
            print("result: ", self.db.update_partners_data(partner_dict_data))
            if self.db.update_partners_data(partner_dict_data):
                if not no_message_for_test:
                    send_information_message_box("Обновлен")

                # Обновление имени Активного партнера
                """
                На случай того, если обновится имя - мы его поменяем на новое
                В случае, если имя не поменяется - Оно заменится на идентичное
                """
                Partner.set_name(self.partner_name_entry.text())
                return
            if not no_message_for_test:
                send_discard_message_box("Ошибка")
        except Exception:
            print("error")
            if not no_message_for_test:
                send_discard_message_box("Ошибка")

    # Функция создания поля для ввода текста
    def create_pattern_Qline_edit(self, late_message: str):
        '''
        Создание поля для ввода
        :param late_message: исчезающий текст в поле для ввода
        :return: поле для ввода, чтобы привязать его к переменной
        '''
        entry = QLineEdit()

        # Установка текста, который предстоит менять
        entry.setText(late_message)
        self.container.addWidget(entry)

        return entry

    # Функция возврата на прошлое окно
    def back_to_later_window(self):
        '''
        Функция открытия окна с партнерской информацией.
        :return: Ничего
        '''
        self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame, Partner.get_name())
