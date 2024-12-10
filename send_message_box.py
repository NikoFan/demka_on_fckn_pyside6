from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSize, QRect



def send_information_message_box(message_text: str):
    ''' Отправка информационного сообщения '''
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Мастер Пол Поддержка")
    msgBox.setText("\t\t"+message_text+"\t\t\t\t")
    msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
    msgBox.setIcon(QMessageBox.Icon.Information)
    result = msgBox.exec()
    print(result)
    return result

def send_discard_message_box(message_text: str):
    ''' Отправка сообщения об ошибке / запрете '''
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Мастер Пол Поддержка")
    msgBox.setText("\t\t"+message_text+"\t\t\t\t")
    msgBox.setIcon(QMessageBox.Icon.Critical)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Yes)
    msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
    result = msgBox.exec()
    return result