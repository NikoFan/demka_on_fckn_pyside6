# Импорт библиотек
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit)

# Импорт классов
from FRAMES import Partner_information_frame
from send_message_box import send_discard_message_box, send_information_message_box
from check_input_info import *


class PartnerUpdateFrame(QFrame):
    """ Класс обновления партнера в Базе данных. Действия:
    - Обновление партнера : self.update_partner_information
    - Возврат на окно информации о партнере : self.back_to_later_window

    Класс добавления нового партнера 1 в 1, как и этот.
    там различается только 2 момента:
    1. В строках для ввода нет текста, только подсказки
    2. После нажатия на кнопку срабатывает другой скрипт БД
    """

    def __init__(self, parent, controller):
        QFrame.__init__(self, parent)

        # Инициализация переменных
        """ Все переменные берутся из Главного класса (Application()) 
        Они приходят вместе с controller, который передается как self при переходе в окно """
        self.controller = controller
        self.db = controller.db

        # Создание контейнера для Элементов окна
        self.container = QVBoxLayout()

        # Обновление окна до актуальных данных
        self.update_start_values()

        # Выгрузка контейнера с содержимым на фрейм
        self.setLayout(self.container)

    # Очистка старого контейнера
    def clear_layout(self):
        """ Очистка контейнера с элементами (QLineEdit, QPushButton и т.д.),
        чтобы он не хранил в себе старые виджеты """

        # Очистка контейнера от старых элементов
        """
        Проблема вся в том, что если создавать QVBoxLayout() в функции обновления -
        строки для ввода не будут передавать новый текст

        Для этого надо создавать его в __init__() функции
        НО если не очистить его, то каждое упоминание класса будет создавать строки и хранить их в Контекнере
        Для этого контейнер чистится перед запуском файла
        """
        for i in reversed(range(self.container.count())):

            # Считывается виджет из контейнера по ID
            widget = self.container.itemAt(i).widget()

            # Проверка, что виджет не пустой
            if widget is not None:
                # Удаление виджета
                widget.deleteLater()

    # Обновление информации на фрейме
    def update_start_values(self):
        ''' Обновление стартовых значений
        Чтобы при открытии окна данные были актуальными '''
        # Очистка контейнера от старых элементов
        self.clear_layout()

        # Получение стартовых данных о партнере
        """
        Полученные данные будут установлены в качестве стартовых в поля для ввода
        """
        self.partner_late_info = self.db.get_partner_by_name(Partner.get_name())

        # Создание заголовка окна
        self.title_add_window_name = QLabel(self)
        self.title_add_window_name.setText("Добавить партнера")

        # Установка имени объекта, к которому уже есть стиль Заголовка
        self.title_add_window_name.setObjectName("Title")

        # Добавление заголовка в контейнер
        self.container.addWidget(self.title_add_window_name)


        # Создание строк для ввода
        """ Строки создаются по единому стандарту в функции self.create_pattern_Qline_edit() """
        self.create_text_enter_hint("Имя партнера")
        self.partner_name_entry = self.create_pattern_Qline_edit(self.partner_late_info['name'].strip())

        self.create_text_enter_hint("Юридический адрес партнера")
        self.partner_address_entry = self.create_pattern_Qline_edit(self.partner_late_info['ur_addr'].strip())

        self.create_text_enter_hint("Телефон партнера (формат +7 9хх ххх хх хх)")
        self.partner_phone_entry = self.create_pattern_Qline_edit(self.partner_late_info['phone'].strip())

        # Установка максимальной длины (не знаю почему, но с 12 работает некорректно)
        self.partner_phone_entry.setMaxLength(13)

        # Установка маски для ввода
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
        hint.setObjectName("text_enter_hint")
        self.container.addWidget(hint)

    def update_partner_information(self):
        ''' Метод обновления информации о партнере в БД '''

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

        # Установка исчезающего текста
        entry.setText(late_message)
        self.container.addWidget(entry)

        return entry

    def back_to_later_window(self):
        ''' Открытие прошлого окна '''

        self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame, Partner.get_name())


