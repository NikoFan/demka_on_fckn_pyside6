# Импорт библиотек
import sys
from linecache import updatecache

from PySide6.QtCore import Qt, Slot, QSize, QRect
from PySide6.QtWidgets import (
    QStackedWidget,
    QApplication,
    QVBoxLayout,
    QFrame,
    QWidget,
    QPushButton,
    QLabel,
    QScrollArea)

# Class
from FRAMES import  Partner_frame, Partner_information_frame
from Partner import Partner
from db.database import Database


class MainWindow(QFrame):
    ''' Класс приложения '''

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
        self.widgets_layout_container = QVBoxLayout(QWidget(self))

        # Создание области для карточек партнера
        self.scrollArea = self.create_scroll_area()

        self.scrollArea.setObjectName("PartnerCardScrollArea")

        self.widgets_layout_container.addWidget(QLabel("Список партнеров",
                                                       objectName="Title"))

        # Добавление контейнера в область прокрутки
        self.scrollArea.setWidget(self.create_partner_cards_for_scroll_area())

        # Добавление кнопки "Добавить"
        self.add_partner_btn = QPushButton(self)
        self.add_partner_btn.setText("Добавить Партнера")
        self.add_partner_btn.setObjectName("Add")
        self.add_partner_btn.clicked.connect(self.open_partner_add_frame)

        self.widgets_layout_container.addWidget(self.scrollArea)
        self.widgets_layout_container.addWidget(self.add_partner_btn)

        self.setLayout(self.widgets_layout_container)

    # Расчет скидки для партнера
    def take_discount(self, partner_name: str):
        ''' Расчет скидки '''
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
    @Slot()
    def create_partner_cards_for_scroll_area(self):
        ''' Метод создания и заполнения области прокрутки с карточками партнеров '''

        # Создание хранилища для карточек партнера
        self.scroll_area_widgets_container = self.create_scroll_area_widgets_container()
        # Установка в области хранения вертикальной ориентации при выгрузке
        self.vertical_scroll_container = QVBoxLayout(self.scroll_area_widgets_container)
        # Заполнение списка партнеров
        for partner in Database().get_partners():
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
            self.partner_info.setObjectName(f"{partner['name'].strip()}")

            # Установка действия при нажатии
            self.partner_info.clicked.connect(self.open_partner_information_frame)

            # Добавление кнопки в карточку
            self.partner_card_info_vbox.addWidget(self.partner_info)

            # Добавление карточки партнера в контейнер
            self.vertical_scroll_container.addWidget(self.partner_card)

        return self.scroll_area_widgets_container

    # Область для карточек партнеров
    @Slot()
    def create_scroll_area(self):
        ''' Создание области для размещения карточек партнеров '''
        scroll = QScrollArea(self)
        scroll.setObjectName("scroll")

        # Установка размеров области


        # Установка разрешения на Растягивание области
        '''
        Если будет стоять False -> объекты внутри области будут своего стандартного размера
        '''
        scroll.setWidgetResizable(True)
        return scroll

    # Создание контейнера для Карточек партнера
    """
    Для отображения карточек пар нера используется область ScrollArea, однако в нее следует поместить сами карточки
    Для этого создается контейнер для виджетов, который помещается в ScrollArea
    
    // Пример Кода добавления Контейнера с карточками (Widgets) в Область прокрутки (ScrollArea)
    self.scrollArea.setWidget(self.create_partner_cards_for_scroll_area())
    """
    @Slot()
    def create_scroll_area_widgets_container(self):
        ''' Создание контейнера для виджетов '''
        scroll_area_widgets_container = QWidget()
        scroll_area_widgets_container.setObjectName("scroll_area_widgets_container")
        scroll_area_widgets_container.setContentsMargins(10, 10, 10, 10)

        return scroll_area_widgets_container

    # Click Listener Для кнопки перехода в окно Добавления партнера (PartnerAddFrame)
    def open_partner_information_frame(self):
        ''' Отправка запроса на открытие окна информации о партнера '''
        # sender - Кнопка, с которой пришел запрос
        sender = self.sender()
        print("sender: ", sender.objectName())
        Partner.set_name(sender.objectName())
        print("partner name __:", Partner.get_name())

        # В ObjectName() кнопки будет записано имя партнера - Так будет проще работать с его информацией
        self.controller.open_partner_frame(Partner_information_frame.PartnerInformationFrame, sender.objectName())

    def open_partner_add_frame(self):
        """ Открыть окно с добавлением нового партнера """
        self.controller.show_frames(Partner_frame.PartnerAddFrame)

