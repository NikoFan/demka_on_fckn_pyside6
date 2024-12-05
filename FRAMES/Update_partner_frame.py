# Импорт библиотек
import sys

from PySide6.QtCore import Qt, Slot, QSize, QRect
from PySide6.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QLabel,
    QTextEdit,
    QFormLayout,
    QVBoxLayout,
    QLineEdit)

from Partner import Partner
from FRAMES import MainWindow_frame, Partner_information_frame
from app import Application
from send_message_box import send_discard_message_box, send_information_message_box
from check_input_info import *


class PartnerUpdateFrame(QFrame):
    ''' Класс добавления партнера '''

    def __init__(self, parent, controller):

        QFrame.__init__(self, parent)
        self.controller = controller
        self.db = controller.db

        self.container = QVBoxLayout()

        self.update_start_values()
        self.setLayout(self.container)

    def clear_layout(self):
        ''' Очистка контейнера с виджетами, чтобы он не хранил в себе старые виджеты'''

        # Очистка
        """
        Проблема вся в том, что если создавать QVBoxLayout() в функции обновления -
        строки для ввода не будут передавать новый текст

        Для этого надо создавать его в __init__() функции
        НО если не очистить его, то каждое упоминание класса будет создавать строки и хранить их в Контекнере
        Для этого контейнер чистится перед запуском файла
        """
        for i in reversed(range(self.container.count())):
            widget = self.container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Удаляем

    def update_start_values(self):
        ''' Обновление стартовых значений
        Чтобы при открытии окна данные были актуальными '''
        # Очистка контейнера от старых данных
        self.clear_layout()

        # Получение стартовых данных о партнере
        """
        Полученные данные будут установлены в качестве стартовых в поля для ввода
        """
        self.partner_late_info = self.db.get_partner_by_name(Partner.get_name())

        self.title_add_window_name = QLabel(self)
        self.title_add_window_name.setText("Добавить партнера")
        self.title_add_window_name.setObjectName("Title")
        self.container.addWidget(self.title_add_window_name)

        '''
        Каждый объект создается по паттерну, где прописываются его координаты и параметры
        Так ка из Layout нельзя получить текст в полях - приходится их размещать вручную

        В паттер передается сообщение и координаты Х и У
        '''
        # Добавление объектов на Фрейм
        self.create_text_enter_hint("Имя партнера")
        self.partner_name_entry = self.create_pattern_Qline_edit(self.partner_late_info['name'].strip())

        self.create_text_enter_hint("Юридический адрес партнера")
        self.partner_address_entry = self.create_pattern_Qline_edit(self.partner_late_info['ur_addr'].strip())

        self.create_text_enter_hint("Телефон партнера (формат +7 9хх ххх хх хх)")
        self.partner_phone_entry = self.create_pattern_Qline_edit(self.partner_late_info['phone'].strip())
        self.partner_phone_entry.setMaxLength(13)
        self.partner_phone_entry.setInputMask("+7 000 000 00 00")

        self.create_text_enter_hint("Электронная почта партнера")
        self.partner_mail_entry = self.create_pattern_Qline_edit(self.partner_late_info['mail'].strip())

        self.create_text_enter_hint("ИНН партнера")
        self.partner_inn_entry = self.create_pattern_Qline_edit(self.partner_late_info['inn'].strip())
        self.partner_phone_entry.setMaxLength(10)

        self.create_text_enter_hint("Рейтинг партнера")
        self.partner_rate_entry = self.create_pattern_Qline_edit(self.partner_late_info['rate'])

        self.create_text_enter_hint("Тип партнера")
        self.partner_type_entry = self.create_pattern_Qline_edit(self.partner_late_info['type'].strip())

        self.create_text_enter_hint("Директор партнера")
        self.partner_director_entry = self.create_pattern_Qline_edit(self.partner_late_info['director'].strip())

        # Создание кнопки "Добавить"
        self.update = QPushButton(self)
        self.update.setText("Обновить")
        self.update.setObjectName("add")
        self.update.clicked.connect(self.update_partner_information)
        self.container.addWidget(self.update)

        # Создание кнопки "На главную"
        self.back = QPushButton(self)
        self.back.setText("Назад")
        self.back.setObjectName("back")
        self.back.clicked.connect(self.back_to_later_window)
        self.container.addWidget(self.back)

        # return self.widgets_layout_container

    def create_text_enter_hint(self, hint_message: str):
        ''' Создание подсказки для ввода текста '''
        hint = QLabel(self)
        hint.setText(hint_message)

        # Размещение строки подсказки на фрейме
        """
        Используется метод аналогичный с QLineEdit
        """
        # hint.setGeometry(20, (40 * index) + (index * 10)  , 600, 20)
        hint.setObjectName("text_enter_hint")
        self.container.addWidget(hint)
        return hint

    def update_partner_information(self):
        ''' Метод добавления нового партнера в базу данных '''

        partner_dict_data: dict = {
            "type": self.partner_type_entry.text(),
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
            if self.db.update_partners_data(partner_dict_data):
                send_information_message_box("Обновлено")

                # Обновление имени Активного партнера
                """
                На случай того, если обновится имя - мы его поменяем на новое
                В случае, если имя не поменяется - Оно заменится на идентичное
                """
                Partner.set_name(self.partner_name_entry.text())
                return
            send_discard_message_box("Ошибка")
        except Exception:
            send_discard_message_box("Ошибка")

    def create_pattern_Qline_edit(self, late_message: str):
        ''' Создание шаблона для ввода текста '''

        # Создание поля для ввода
        """
        self, в параметрах при создании, используется,
        чтобы создаваемый объект автоматически помещался на Используемый Фрейм
        """
        entry = QLineEdit(self)

        # Установка координат и размеров
        """
        В силу того, что объект помещается не в layout, а на голый фрейм,
        он помещается в стартовую позицию (Верхний левый угол), откуда его следует переместить в нужную
        Для этого передается индекс (index), который применяется в формуле расчета У координаты
        С учетом того что высота каждой строки 20 рх, следует просто учитывать их, при разделении
        Поля для ввода и Текста подсказки

        (Устарело)
        """
        # entry.setGeometry(10, 20 + (index * 10) + (40 * index), 750, 20)

        # Установка исчезающего текста
        entry.setText(late_message)
        self.container.addWidget(entry)

        return entry

    def back_to_later_window(self):
        ''' Открытие прошлого окна '''

        self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame, Partner.get_name())


