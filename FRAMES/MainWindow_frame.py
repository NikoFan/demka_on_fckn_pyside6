# Импорт библиотек
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QWidget,
    QPushButton,
    QLabel,
    QScrollArea)

# Импорт классов
from FRAMES import Partner_frame, Partner_information_frame, USELESS_FRAME_TO_SHOW_INSTRUMENTS
from Partner import Partner


class MainWindow(QFrame):

    def __init__(self, controller):
        '''
        Конструктор класса демонстрации карточек партнера
        :param controller: экземпляр класса Application()
        '''
        QFrame.__init__(self)
        self.controller = controller
        self.db = controller.db

        # Вызов функции для заполнения фрейма данными
        '''
        Функция update_start_values() заполняет фрейм минимальными данными
        Стоит понимать, что каждый фрейм является частью одной системы (в том плане, что при запуске приложения
        запускается и загружается каждый фрейм, и он должен быть наделен какими-то кнопками и строками 
        с самого начала работы программы - именно для этого и __init()__ вызывается функция update_start_values()
        Она загружает в него все его строки, НО при целевом открытии (по кнопке) она срабатывает заново и загружает
        АКТУАЛЬНЫЕ ДАННЫЕ
        '''
        self.update_start_values()

    # Обновление стартовых данных на актуальные
    def update_start_values(self):
        '''
        Добавление данных на фрейм
        :return: Ничего
        '''

        # Создание контейнера для виджетов
        """ Контейнеры QVBoxLayout() Позволяют масштабировать виджеты и не париться над их расположением """
        self.widgets_layout_container = QVBoxLayout(self)

        # Создание области для карточек партнера
        """ В self.scrollArea располагаются все карточки товара
        Создание вынесено в отдельную функцию, чтобы не засорять функцию обновления
        """
        scrollArea = self.create_scroll_area()

        # Создание Заголовка окна
        """ При создании устанавливается объектное имя Title, Которое содержит в себе стили Заголовка """

        # Создание виджета для хранения иконки и заголовка окна
        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)

        frame_title = QLabel("Список партнеров")
        frame_title.setObjectName("Title")

        # Добавление фото
        picture = self.create_screen_picture()

        header_widget_layout.addWidget(frame_title)
        header_widget_layout.addWidget(picture)

        self.widgets_layout_container.addWidget(header_widget)

        # Добавление контейнера в область прокрутки
        """ Создание карточек, их заполнение и настройка происходит в отдельной функции """
        scrollArea.setWidget(self.create_partner_cards_for_scroll_area())

        # Добавление кнопки "Добавить"
        add_partner_btn = QPushButton("Добавить Партнера")

        # Установка объектного имени (можно удалить)
        add_partner_btn.setObjectName("Add")

        # Установка действий при нажатии
        add_partner_btn.clicked.connect(
            lambda: self.controller.show_arg_frame(Partner_frame.PartnerAddFrame)
        )

        # Добавление кнопки "Добавить"
        useless_frame = QPushButton()

        # Установка текста кнопки
        useless_frame.setText("open_useless_frame")

        # Установка объектного имени (можно удалить)
        useless_frame.clicked.connect(
            lambda: self.controller.show_arg_frame(USELESS_FRAME_TO_SHOW_INSTRUMENTS.UselessFrame)
        )

        # Добавление области прокрутки в контейнер виджетов
        self.widgets_layout_container.addWidget(scrollArea)

        # Добавление кнопки Добавить в контейнер виджетов
        self.widgets_layout_container.addWidget(add_partner_btn)
        self.widgets_layout_container.addWidget(useless_frame)

    def create_screen_picture(self):
        """
        Создание иконки для помещения на экран
        :return: picture_socket - QLabel с иконкой
        """
        picture_socket = QLabel()
        picture_socket.setObjectName("Image")

        pixmap_picture = QPixmap(u'./res/app_icon_png.png')
        picture_socket.setScaledContents(True)
        picture_socket.setPixmap(pixmap_picture)

        picture_socket.setFixedSize(52, 52)
        return picture_socket

    # Расчет скидки для партнера
    def take_discount(self, partner_name: str):
        '''
        Функция расчета скидки для партнера
        :param partner_name: Имя партнера для которого расчитывается скидка
        :return: Число (%) скидки
        '''
        # Получение суммы продаж партнера
        count: int = self.db.get_sum_sales(partner_name)
        if (count == None):
            return 0
        if (count > 300000):
            return 15
        elif (count > 50000):
            return 10
        elif (count > 10000):
            return 5
        # < 10000
        return 0

    # Создание и заполнение области с партнерами
    def create_partner_cards_for_scroll_area(self):
        '''
        Создание контейнера с виджетами - Карточками партнера
        :return: scroll_area_widgets_container - Контейнер с карточками партнеров
        '''

        # Создание хранилища для карточек партнера
        scroll_area_widgets_container = QWidget()
        scroll_area_widgets_container.setObjectName("scroll_area_widgets_container")

        # Установка в области хранения вертикальной ориентации при выгрузке
        """ Мы создаем вертикальное отображение, которое отображает объекты хранящиеся в scroll_area_widgets_container
        Затем мы scroll_area_widgets_container возвращаем в главную функцию, где она помещается в Область прокрутки
        
        ИТОГО:
        Фрейм MainWindow(QFrame) хранит в себе
            контейнер для виджетов (self.widgets_layout_container), который хранит в себе
                кнопку "Добавить" (self.add_partner_btn) и
                Область прокрутки (self.scrollArea), которая
                    хранит в себе Хранилище с карточками товара (self.scroll_area_widgets_container),
                        где все карточки Расположены пов вертикали (self.vertical_scroll_container)
                        
        Вот такая матрешка позволяет добавлять дофига объектов и не терять разметку
        """
        vertical_scroll_container = QVBoxLayout(scroll_area_widgets_container)

        # Заполнение списка партнеров
        """ Производится запрос к БД, откуда возвращается словарь с данными,
        который мы перебираем в цикле for """
        for partner in self.db.get_partners():
            # Создание виджета для хранения информации по карточке партнера
            partner_card = QWidget()
            partner_card.setObjectName("partner_card")

            # Установка в self.partner_card вертикальной ориентации
            partner_card_info_vbox = QVBoxLayout(partner_card)

            # Добавление строк с информацией
            """
            Делается запрос в БД, откуда получается ответ в виде словаря, из которого вычленяются данные
            Пример установки объектного имени при создании QLabel : QLabel(objectName="obj_name")
            """
            partner_card_info_vbox.addWidget(QLabel(f"{partner['type'].strip()} | {partner['name'].strip()}"))
            partner_card_info_vbox.addWidget(QLabel(f"{self.take_discount(partner['name'])}%",
                                                    objectName="discount"))
            partner_card_info_vbox.addWidget(QLabel(f"Директор: {partner['director'].strip()}"))
            partner_card_info_vbox.addWidget(QLabel(f"Тел.: +7 {partner['phone'].strip()}"))
            partner_card_info_vbox.addWidget(QLabel(f"Рейтинг: {partner['rate']}"))

            # Создание кнопки "Подробнее"
            '''
            Кнопка "Подробнее" находится в карточке товара и ведет в окно 
            '''
            partner_info = QPushButton(f"Подробнее")
            # Установка имени объекта
            partner_info.setObjectName(f"{partner['name'].strip()}")

            # Установка действия при нажатии
            partner_info.clicked.connect(self.open_partner_information_frame)

            # Добавление кнопки в карточку
            partner_card_info_vbox.addWidget(partner_info)

            # Добавление карточки партнера в контейнер
            vertical_scroll_container.addWidget(partner_card)

        return scroll_area_widgets_container

    def create_scroll_area(self):
        '''
        Создание области прокрутки
        :return: scroll - Область прокрутки
        '''
        scroll = QScrollArea()

        # Установка имени объекта для назначения стилей
        scroll.setObjectName("PartnerCardScrollArea")

        # Установка разрешения на Растягивание области
        scroll.setWidgetResizable(True)
        return scroll

    def open_partner_information_frame(self):
        '''
        Переключение между окнами с сохранением имени партнера
        :return: Ничего
        '''
        # sender - Кнопка, с которой пришел запрос
        sender = self.sender()
        Partner.set_name(sender.objectName())

        # В ObjectName() кнопки будет записано имя партнера - Так будет проще работать с его информацией
        self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame, sender.objectName())
