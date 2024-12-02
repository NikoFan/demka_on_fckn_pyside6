# Импорт библиотек
import sys
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, Slot, QSize, QRect
from PySide6.QtWidgets import (
    QStackedWidget,
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QScrollArea)

# Class
from FRAMES import MainWindow_frame, Partner_frame
from db.database import Database


from Partner import Partner

class Application(QWidget):
    ''' Класс приложения '''

    def __init__(self):
        QWidget.__init__(self)
        # Настройка окна
        self.setWindowTitle("Мастер пол")
        self.resize(QSize(800, 800))
        self.setMaximumSize(QSize(800, 800))
        self.setObjectName("MainWindowWidget")

        # Установка иконки приложения
        icon = QIcon()
        icon.addPixmap(QPixmap(u"res/app_icon_png.png"))
        self.setWindowIcon(icon)

        # Инициализация бд
        self.db = Database()

        # Инициализация фреймов
        ''' 
        Мы вызываем фреймы передавая в аргументы parent / controller значения self / self
        Это позволяет работать с Стартовым классом Application
        не создавая его объект его каждый раз заново
        '''

        self.main_window = MainWindow_frame.MainWindow(self, self)
        # self.partner_add_window = Partner_frame.PartnerAddFrame(self, self)


        # Создание контейнера для Фреймов
        '''
        Доступ к фреймам происходит по индексу
        Для открытия окна необходимо прописать команду .setCurrentIndex(frame_index)
        Фрейм, который добавляется 1м (в данном случае main_window) - открывается при запуске программы
        '''
        self.frames_container = QStackedWidget()


        # Добавление фреймов в контейнер
        self.frames_container.addWidget(self.main_window)
        # self.frames_container.addWidget(self.partner_add_window)

        # Добавлен Фреймов на окно
        layout = QVBoxLayout(self)
        layout.addWidget(self.frames_container)


    @Slot()
    def show_frames(self, frame):
        ''' Переключение фрейма по Имени фрейма '''
        # Обновление информации на фрейме
        current_frame = frame(self, self)
        print("partner name __:", Partner.get_name())
        # Вызов функции для обновлений данных на фрейме
        current_frame.update_start_values()


        # Добавление обновленного фрейма в контейнер
        self.frames_container.addWidget(current_frame)

        # Вызов обновленного фрейма
        self.frames_container.setCurrentWidget(current_frame)


    @Slot()
    def open_partner_frame(self, frame, partner_name: str = None):
        ''' Установка имени обрабатываемого пользователя перед открытием окна '''
        # Удаление окна партнера
        '''
        В данной функции обрабатываются только те фреймы, где требуется Самая новая информация
        Если до этого фрейм был в списке (=> он был уже загружен со старой информацией) -> 
            то его надо удалить и пересоздать
        При вызове метода передается требуемый метод - он удаляется и пересоздается
        '''
        self.frames_container.removeWidget(frame(self, self))
        # Запись нового имени
        print("partner_name", partner_name)
        if partner_name:
            Partner.set_name(partner_name)

        # Вызов функции для открытия окна
        self.show_frames(frame)



# Стили для окон
Style_sheet = '''
#MainWindowWidget {
    background: #FFFFFF;
}

#PartnerCardScrollArea {
    background-color: #F4E8D3;
}

QMessageBox {
    background: #FFFFFF;
}

QVBoxLayout {
    background: #F4E8D3;
}
QLabel {
    color: #000000;
    font-size: 16px;
}

/* Сделать белой подложку в области прокрутки*/
#scroll_area_widgets_container {
    background: #FFFFFF;
}

/* Установка цвета для всех заголовков */
#Title {
    color: #000000;
    font-size: 25px;
    font-weight: bold;
    qproperty-alignment: AlignCenter;
}

/* Установка стиля для полей ввода */
QLineEdit {
    height: 40px;
    color: #000000;
    background: #FFFFFF
}

/* Установка зеленого цвета и черных букв для всех кнопок */
QPushButton {
    background: #67BA80;
    color: #000000;
    height: 30px;
    font-size: 18px;
}

/* Установка Телесного цвета для подложек карточки партнера */
#partner_card, #scroll_widgets_contents{
    background: #F4E8D3;
}

/* Установка стиля для скидки*/
#discount {
    background: #F4E8D3;
    color: #000000;
    qproperty-alignment: AlignRight;
}

/* Установка Телесного цвета для текста карточек партнера */
#Partner_name, #Partner_phone, #partner_information_data{
    background: #F4E8D3;
    color: #000000;
    padding: 0px 0px 0px 10px;
}
'''

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Установка стилей
    app.setStyleSheet(Style_sheet)

    # Инициализация приложения
    main_window = Application()

    # Демонстрация главного окна
    main_window.show()
    sys.exit(app.exec())

