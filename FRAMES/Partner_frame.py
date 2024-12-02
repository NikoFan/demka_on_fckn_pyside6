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
from FRAMES import MainWindow_frame
from app import Application


class PartnerAddFrame(QFrame):
    ''' Класс добавления партнера '''

    def __init__(self, parent, controller):

        QFrame.__init__(self, parent)
        self.controller = controller
        self.container = QVBoxLayout()



        # self.setLayout(self.update_start_values())
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
        self.partner_name_entry = self.create_pattern_Qline_edit("Введите имя партнера")


        self.create_text_enter_hint("Юридический адрес партнера")
        self.partner_address_entry = self.create_pattern_Qline_edit("Введите адрес партнера")

        self.create_text_enter_hint("Телефон партнера")
        self.partner_phone_entry = self.create_pattern_Qline_edit("Введите телефон партнера формат +79ххххххххх")

        self.create_text_enter_hint("Электронная почта партнера")
        self.partner_email_entry = self.create_pattern_Qline_edit("Введите электронную почту партнера")

        self.create_text_enter_hint("ИНН партнера")
        self.partner_inn_entry = self.create_pattern_Qline_edit("Введите ИНН партнера")

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
        self.add.clicked.connect(self.pr)
        self.container.addWidget(self.add)

        # Создание кнопки "На главную"
        self.back = QPushButton(self)
        self.back.setText("На главную")
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



    def pr(self):

        print("layout:", self.container.widget())
        inp = self.partner_name_entry.text()
        print("Current text", inp, "--")
        print("Current text", self.partner_name_entry.text(), "--")


        print(f'''----------------------
{self.partner_name_entry.text()}
{self.partner_type_entry.text()}
{self.partner_director_entry.text()}
{self.partner_rate_entry.text()}
{self.partner_inn_entry.text()}
{self.partner_email_entry.text()}
{self.partner_address_entry.text()}
{self.partner_phone_entry.text()}
-----------------------
''')


    def create_pattern_Qline_edit(self, placeholder_message: str):
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
        entry.setPlaceholderText(placeholder_message)
        self.container.addWidget(entry)


        return entry

    def back_to_later_window(self):
        ''' Открытие прошлого окна '''

        self.controller.show_frames(MainWindow_frame.MainWindow)


