# Импорт библиотек
import sys
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Slot, QSize
from PySide6.QtWidgets import (
    QStackedWidget,
    QApplication,
    QVBoxLayout,
    QWidget)

# Class
from FRAMES import MainWindow_frame
from db.database import Database
from send_message_box import *
from Partner import Partner


class Application(QWidget):
    ''' Класс приложения '''

    def __init__(self):
        QWidget.__init__(self)
        """ Настройка параметров приложения """
        # Установка названия окна
        self.setWindowTitle("Мастер пол")

        # Установка стартовых значений Ширина / Высота
        self.resize(QSize(800, 800))

        # Установка максимальных значений для расширения
        # Не дает объектам в окне самим его масштабировать и сохранит возможность уменьшать окно пользователю
        self.setMaximumSize(QSize(800, 800))

        # Установка объектного имени окна
        # Имя используется при установке стилей
        self.setObjectName("MainWindowWidget")

        """ Установки иконки для приложения """
        # Инициализация переменной для хранения иконки
        icon = QIcon()

        # Загрузка иконки из каталога с изображениями
        icon.addPixmap(QPixmap(u"res/app_icon_png.png"))

        # Установка иконки
        self.setWindowIcon(icon)

        """ Инициализация переменных """
        # Инициализация базы данных
        # В дальнейшем пользователь будет взаимодействовать с ней через controller.db
        self.db = Database()

        # Инициализация стартового фрейма
        ''' 
        Мы вызываем фреймы передавая в аргументы parent / controller значения self / self
        Под значение self используется класс Application(), из которого будут браться переменные
        такие как db, или его функции (show_frame() и т.д)
        Это позволяет работать с Стартовым классом Application
        не создавая его объект его каждый раз заново
        '''
        self.main_window = MainWindow_frame.MainWindow(self, self)


        # Создание контейнера для Фреймов
        '''
        Доступ к фреймам происходит по имени класса
        Для открытия окна необходимо прописать команду .setCurrentWidget(current_frame)
        Стартовый фрейм (в данном случае main_window) - открывается при запуске программы
        '''
        self.frames_container = QStackedWidget()


        # Добавление стартового фрейма в контейнер
        self.frames_container.addWidget(self.main_window)

        """ Добавлений фрейма в приложение """
        # Создание макета для расположения фреймов из контейнера
        frames_container_layout = QVBoxLayout(self)

        # Добавление контейнера в планировщик
        frames_container_layout.addWidget(self.frames_container)


    # @Slot()
    # def show_frames(self, frame):
    #     ''' Переключение фрейма по Имени фрейма '''
    #     # Обновление информации на фрейме
    #     current_frame = frame(self, self)
    #     print("partner name __:", Partner.get_name())
    #     # Вызов функции для обновлений данных на фрейме
    #     current_frame.update_start_values()
    #
    #
    #     # Добавление обновленного фрейма в контейнер
    #     self.frames_container.addWidget(current_frame)
    #
    #     # Вызов обновленного фрейма
    #     self.frames_container.setCurrentWidget(current_frame)


    @Slot()
    def show_arg_frame(self, frame, partner_name: str = Partner.get_name()):
        """ Открытие фрейма по нажатию кнопки + установка имени обрабатываемого партнера """

        current_frame = frame(self, self)
        # Удаление старого окна из контейнера фреймов
        '''
        В данной функции обрабатываются только те фреймы, где требуется Самая новая информация
        Если до этого фрейм был в списке (=> он был уже загружен со старой информацией) -> 
            то его надо удалить и пересоздать
        При вызове метода передается требуемый метод - он удаляется и пересоздается
        '''
        self.frames_container.removeWidget(current_frame)

        # Запись нового имени
        print("partner name __:", partner_name)

        """ Установка имени обрабатываемого партнера в Статический Класс """
        # Проверка, что имя не пустышка
        if partner_name:
            # Установка имени
            Partner.set_name(partner_name)

        # Вызов функции для открытия окна
        """ Было принято решение не писать эту функцию, а ее функционал перенести в 1
        Это позволяет сократить объем кода
        Для предотвращения ошибок, в случае если при вызове не передается Новое имя партнера
        В аргументах стоит стартовое значение, которе будет использоваться в случае
        отсутствия имени в передаваемых параметрах
        """
        # self.show_frames(frame)


        # Вызов функции для обновлений данных на фрейме
        """
        В каждом фрейме создана такая функция.
        Это позволит избежать конфликта, когда функция вызывается, а в фрейме ее нет
        """
        current_frame.update_start_values()

        # Добавление обновленного фрейма в контейнер
        self.frames_container.addWidget(current_frame)

        # Вызов обновленного фрейма
        """ Функция отображает выбранные фрейм """
        self.frames_container.setCurrentWidget(current_frame)


    # Обработка закрытия окна
    def closeEvent(self, event, param=False):
        # Пользователь отвечает на сообщение ДА - 16000 НЕТ - 66000 (это код кнопки)
        print(event)
        if param:
            exit()
        if UserMessageBox().send_information_message_box("Выйти из приложения?") < 17000:
            event.accept()
        else:
            event.ignore()



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
/* Установка цвета для всех заголовков */
#Title {
    color: #000000;
    font-size: 25px;
    font-weight: bold;
    qproperty-alignment: AlignCenter;
}

/* Сделать белой подложку в области прокрутки*/
#scroll_area_widgets_container {
    background: #FFFFFF;
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
#Partner_name, #Partner_phone, #partner_information_data, #text_enter_hint{
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

