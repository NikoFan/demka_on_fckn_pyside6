from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSize, QRect

def send_information_message_box(message_text: str):
    ''' Отправка информационного сообщения '''
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Мастер Пол Поддержка")
    msgBox.setText("\t\t"+message_text+"\t\t\t\t")
    msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Close)
    msgBox.setIcon(QMessageBox.Icon.Information)
    result = msgBox.exec()
    return result

def send_discard_message_box(message_text: str):
    ''' Отправка сообщения об ошибке / запрете '''
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Мастер Пол Поддержка")
    msgBox.setText("\t\t"+message_text+"\t\t\t\t")
    msgBox.setIcon(QMessageBox.Icon.Critical)
    result = msgBox.exec()
    return result