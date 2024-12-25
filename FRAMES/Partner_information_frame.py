# Импорт библиотек
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout)

from Partner import Partner
from FRAMES import MainWindow_frame, History_frame, Update_partner_frame


class PartnerInformationFrame(QFrame):

    def __init__(self, controller):
        '''
        Конструктор класса с партнерской информацией
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

        self.widgets_container = QVBoxLayout(self)

        partner_data = self.db.get_partner_by_name(Partner.get_name())

        # Добавление информации о партнере
        self.widgets_container.addWidget(QLabel(f"{partner_data['name'].strip()}", objectName="Title"))

        self.widgets_container.addWidget(QLabel(f"Имя партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['name'].strip()}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"Телефон партнера:"))
        self.widgets_container.addWidget(QLabel(f"+7 {partner_data['phone'].strip()}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"Тип партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['type'].strip()}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"Почта партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['mail'].strip()}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"Юридический адрес партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['ur_addr'].strip()}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"ИНН партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['inn'].strip()}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"Рейтинг партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['rate']}",
                                                objectName="partner_information_data"))

        self.widgets_container.addWidget(QLabel(f"Директор партнера:"))
        self.widgets_container.addWidget(QLabel(f"{partner_data['director'].strip()}",
                                                objectName="partner_information_data"))

        # Добавление кнопки "История"
        update_partner = QPushButton("Обновить")
        update_partner.clicked.connect(
            lambda: self.controller.show_arg_frame(Update_partner_frame.PartnerUpdateFrame, Partner.get_name())
        )
        self.widgets_container.addWidget(update_partner)

        # Добавление кнопки "История"
        history_btn = QPushButton("История продаж партнера")
        history_btn.clicked.connect(
            lambda: self.controller.show_arg_frame(History_frame.HistoryFrame, Partner.get_name())
        )

        self.widgets_container.addWidget(history_btn)

        # Добавление кнопки "Обратно"
        on_main_btn = QPushButton("На главную")
        on_main_btn.clicked.connect(
            lambda: self.controller.show_arg_frame(MainWindow_frame.MainWindow, Partner.get_name())
        )
        self.widgets_container.addWidget(on_main_btn)
