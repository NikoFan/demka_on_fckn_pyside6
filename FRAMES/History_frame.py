# Импорт библиотек
from PySide6.QtCore import Qt, Slot, QSize, QRect
from PySide6.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem)


from Partner import Partner
from FRAMES import Partner_information_frame
from app import Application

class HistoryFrame(QFrame):
    ''' Класс Истории продаж партнера '''

    def __init__(self, parent, controller):

        QFrame.__init__(self, parent)
        self.controller = controller
        self.db = controller.db
        self.update_start_values()

    def update_start_values(self):
        ''' Обновление стартовых данных о партнере '''

        '''
        Была решена проблема с немасштабируемой таблицей
        для этого достаточно убрать QWidget(self) из скобок в QVBoxLayout()
        и убрать все слова self из скобок
        '''
        self.widgets_container = QVBoxLayout()
        self.tables = QTreeWidget()

        # self.tables.setColumnCount(3)
        self.tables.setHeaderLabels(["Продукт", "Партнер", "Количество", "Дата"])

        self.partner_name = None
        for sales_data in self.db.get_sales_data(Partner.get_name()):
            self.partner_name = sales_data["partner_name"]
            # Установка строк в колонки
            self.table_data = QTreeWidgetItem(self.tables)
            self.table_data.setText(0, sales_data["product_name"])
            self.table_data.setText(1, sales_data["partner_name"])
            self.table_data.setText(2, str(sales_data["quantity"]))
            self.table_data.setText(3, str(sales_data["sale_date"]))

        self.restore_table_button = QPushButton("Перезагрузить таблицу")
        self.restore_table_button.clicked.connect(
            self.restore_frame
        )

        self.back = QPushButton("Назад")
        self.back.clicked.connect(
            self.open_partner_info_frame
        )

        self.widgets_container.addWidget(self.tables)
        self.widgets_container.addWidget(self.restore_table_button)
        self.widgets_container.addWidget(self.back)

        self.setLayout(self.widgets_container)


    def restore_frame(self):
        self.controller.show_arg_frame(HistoryFrame, self.partner_name)

    def open_partner_info_frame(self):
        self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame, self.partner_name)


