# Импорт библиотек
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QWidget,
    QPushButton,
    QLabel,
    QScrollArea)

# Импорт классов
from FRAMES import  Partner_frame, Partner_information_frame, USELESS_FRAME_TO_SHOW_INSTRUMENTS
from Partner import Partner


class MainWindow(QFrame):
    ''' Стартовый класс приложения. Отображает список партнеров и предлагает действия:
    - Просмотреть подробнее партнера : self.partner_info
    - Добавить нового партнера : self.add_partner_btn
    '''

    def __init__(self, parent, controller):
        QFrame.__init__(self, parent)
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
    """
    Из-за того, что мы ведем работу непосредственно с фреймами,
    которые загружаются с самого начала работы приложения
    Они имеют устаревшие данные.
    При открытии окна следует обновить все его элементы до новейших
    
    Поэтому - вытащить все действия по созданию объектов в отдельную функцию - это здравое решение,
    оно позволяет избежать конфликтов при генерации окна
    """
    def update_start_values(self):
        ''' Обновление данных до актуальных '''

        # Создание контейнера для виджетов
        """ Контейнеры QVBoxLayout() Позволяют масштабировать виджеты и не париться над их расположением """
        self.widgets_layout_container = QVBoxLayout(QWidget(self))

        # Создание области для карточек партнера
        """ В self.scrollArea располагаются все карточки товара
        Создание вынесено в отдельную функцию, чтобы не засорять функцию обновления
        """
        self.scrollArea = self.create_scroll_area()

        # Создание Заголовка окна
        """ При создании устанавливается объектное имя Title, Которое содержит в себе стили Заголовка """

        # Создание виджета для хранения иконки и заголовка окна
        self.header_widget = QWidget()
        self.header_widget_layout = QHBoxLayout(self.header_widget)

        self.frame_title = QLabel("Список партнеров")
        self.frame_title.setObjectName("Title")

        # Добавление фото
        self.picture = self.create_screen_picture()

        self.header_widget_layout.addWidget(self.frame_title)
        self.header_widget_layout.addWidget(self.picture)

        self.widgets_layout_container.addWidget(self.header_widget)

        # Добавление контейнера в область прокрутки
        """ Создание карточек, их заполнение и настройка происходит в отдельной функции """
        self.scrollArea.setWidget(self.create_partner_cards_for_scroll_area())

        # Добавление кнопки "Добавить"
        self.add_partner_btn = QPushButton(self)

        # Установка текста кнопки
        self.add_partner_btn.setText("Добавить Партнера")

        # Установка объектного имени (можно удалить)
        self.add_partner_btn.setObjectName("Add")


        # Установка действий при нажатии
        self.add_partner_btn.clicked.connect(self.open_partner_add_frame)

        # Добавление кнопки "Добавить"
        self.useless_frame = QPushButton(self)

        # Установка текста кнопки
        self.useless_frame.setText("open_useless_frame")

        # Установка объектного имени (можно удалить)
        self.useless_frame.clicked.connect(
            lambda : self.controller.show_arg_frame(USELESS_FRAME_TO_SHOW_INSTRUMENTS.UselessFrame)
        )

        # Добавление области прокрутки в контейнер виджетов
        self.widgets_layout_container.addWidget(self.scrollArea)

        # Добавление кнопки Добавить в контейнер виджетов
        self.widgets_layout_container.addWidget(self.add_partner_btn)
        self.widgets_layout_container.addWidget(self.useless_frame)

        # Добавление контейнера виджетов на фрейм
        self.setLayout(self.widgets_layout_container)

    def create_screen_picture(self):
        """ Добавление фотографии на фрейм """
        self.picture_socket = QLabel(self)
        self.picture_socket.setObjectName("Image")

        self.pixmap_picture = QPixmap(u'./res/app_icon_png.png')
        self.picture_socket.setScaledContents(True)
        self.picture_socket.setPixmap(self.pixmap_picture)

        self.picture_socket.setFixedSize(52, 52)
        return self.picture_socket

    # Расчет скидки для партнера
    def take_discount(self, partner_name: str):
        ''' Расчет скидки (Это прописано в задании) '''
        # Получение суммы продаж партнера
        count: int = self.db.get_sum_sales(partner_name)[0]['count']
        if (count == None):
            return 0
        if (count > 300000):
            return 15
        elif (count > 50000):
            return 10
        elif (count > 10000):
            return 5
        return 5

    # Создание и заполнение области с партнерами
    def create_partner_cards_for_scroll_area(self):
        ''' Метод создания и заполнения области прокрутки с карточками партнеров '''

        # Создание хранилища для карточек партнера
        self.scroll_area_widgets_container = self.create_scroll_area_widgets_container()

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
        self.vertical_scroll_container = QVBoxLayout(self.scroll_area_widgets_container)

        # Заполнение списка партнеров
        """ Производится запрос к БД, откуда возвращается словарь с данными,
        который мы перебираем в цикле for """
        for partner in self.db.get_partners():
            # Создание виджета для хранения информации по карточке партнера
            self.partner_card = QWidget()
            self.partner_card.setObjectName("partner_card")

            # Установка в self.partner_card вертикальной ориентации
            self.partner_card_info_vbox = QVBoxLayout(self.partner_card)

            # Добавление строк с информацией
            """
            Делается запрос в БД, откуда получается ответ в виде словаря, из которого вычленяются данные
            Пример установки объектного имени при создании QLabel : QLabel(objectName="obj_name")
            """
            self.partner_card_info_vbox.addWidget(QLabel(f"{partner['type'].strip()} | {partner['name'].strip()}"))
            self.partner_card_info_vbox.addWidget(QLabel(f"{self.take_discount(partner['name'])}%",
                                                         objectName="discount"))
            self.partner_card_info_vbox.addWidget(QLabel(f"Директор: {partner['director'].strip()}"))
            self.partner_card_info_vbox.addWidget(QLabel(f"Тел.: +7 {partner['phone'].strip()}"))
            self.partner_card_info_vbox.addWidget(QLabel(f"Рейтинг: {str(partner['rate']).strip()}"))


            # Создание кнопки "Подробнее"
            '''
            Кнопка "Подробнее" находится в карточке товара и ведет в окно 
            '''
            self.partner_info = QPushButton(self)
            self.partner_info.setText(f"Подробнее")

            # Установка имени объекта
            self.partner_info.setObjectName(f"{partner['name'].strip()}")

            # Установка действия при нажатии
            self.partner_info.clicked.connect(self.open_partner_information_frame)

            # Добавление кнопки в карточку
            self.partner_card_info_vbox.addWidget(self.partner_info)

            # Добавление карточки партнера в контейнер
            self.vertical_scroll_container.addWidget(self.partner_card)

        return self.scroll_area_widgets_container

    # Область для карточек партнеров
    def create_scroll_area(self):
        ''' Создание области для размещения карточек партнеров '''
        scroll = QScrollArea(self)

        # Установка имени объекта для назначения стилей
        scroll.setObjectName("PartnerCardScrollArea")

        # Установка разрешения на Растягивание области
        ''' Если будет False -> объекты внутри области будут своего стандартного размера '''
        scroll.setWidgetResizable(True)
        return scroll

    # Создание контейнера для Карточек партнера
    """
    Для отображения карточек партнера используется область ScrollArea, однако в нее следует поместить сами карточки
    Для этого создается контейнер для виджетов, который помещается в ScrollArea
    
    // Пример Кода добавления Контейнера с карточками (Widgets) в Область прокрутки (ScrollArea)
    self.scrollArea.setWidget(self.create_partner_cards_for_scroll_area())
    """
    @Slot()
    def create_scroll_area_widgets_container(self):
        ''' Создание контейнера для виджетов в который будут помещаться картовки товаров '''
        scroll_area_widgets_container = QWidget()
        scroll_area_widgets_container.setObjectName("scroll_area_widgets_container")

        return scroll_area_widgets_container

    # Click Listener Для кнопки перехода в окно Добавления партнера (PartnerAddFrame)
    def open_partner_information_frame(self):
        ''' Отправка запроса на открытие окна информации о партнера '''
        # sender - Кнопка, с которой пришел запрос
        sender = self.sender()
        Partner.set_name(sender.objectName())

        # В ObjectName() кнопки будет записано имя партнера - Так будет проще работать с его информацией
        self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame, sender.objectName())

    def open_partner_add_frame(self):
        """ Открыть окно с добавлением нового партнера """
        self.controller.show_arg_frame(Partner_frame.PartnerAddFrame)

