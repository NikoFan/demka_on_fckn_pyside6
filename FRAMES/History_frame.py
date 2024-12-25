# Импорт библиотек
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem)

from Partner import Partner
from FRAMES import Partner_information_frame


class HistoryFrame(QFrame):

    def __init__(self, controller):
        '''
        Конструктор класса истории продаж партнера
        :param controller: экземпляр класса Application()
        '''
        QFrame.__init__(self)
        self.controller = controller
        self.db = controller.db
        self.update_start_values()

    def update_start_values(self):
        '''
        Загрузка элементов на фрейм
        :return: Ничего
        '''

        self.widgets_container = QVBoxLayout(self)
        tables = QTreeWidget()

        # self.tables.setColumnCount(3)
        tables.setHeaderLabels(["Продукт", "Партнер", "Количество", "Дата"])

        for sales_data in self.db.get_sales_data(Partner.get_name()):
            partner_name = sales_data["partner_name"]
            # Установка строк в колонки
            table_data = QTreeWidgetItem(tables)
            table_data.setText(0, sales_data["product_name"])
            table_data.setText(1, sales_data["partner_name"])
            table_data.setText(2, sales_data["quantity"])
            table_data.setText(3, sales_data["sale_date"])

        restore_table_button = QPushButton("Перезагрузить таблицу")
        restore_table_button.clicked.connect(
            lambda: self.controller.show_arg_frame(HistoryFrame)
        )

        back = QPushButton("Назад")
        back.clicked.connect(
            lambda: self.controller.show_arg_frame(Partner_information_frame.PartnerInformationFrame)
        )

        self.widgets_container.addWidget(tables)
        self.widgets_container.addWidget(restore_table_button)
        self.widgets_container.addWidget(back)
