# Библиотеки
import re # Регулярка

# Классы
from db.database import *


def routes(partner_info: dict):
    ''' Маршрутизатор проверок '''
    try:
        if (check_name(partner_info['name']) and
            check_type(partner_info['type']) and
            check_dir(partner_info['director']) and
            check_mail(partner_info['mail']) and
            check_ur_addr(partner_info['ur_addr']) and
            check_rate(partner_info['rate']) and
            check_inn(partner_info['inn']) and
            check_phone(partner_info['phone'])):
            return True
        return False
    except Exception:
        return False

def check_name(partner_name: str):
    ''' Проверка имени компании партнера'''
    if (str(partner_name) and len(partner_name) > 0):
        return True
    print("false 1")
    return False

def check_type(partner_type: str):
    ''' Проверка типа партнера '''
    if (partner_type in ["ЗАО", "ООО", "ПАО", "ОАО"] and
    len(partner_type) == 3):
        return True
    print("false 2")
    return False

def check_dir(partner_dir_name: str):
    ''' Проверка ФИО директора '''
    if (len(partner_dir_name.split(' ')) == 3 and
    str(partner_dir_name)):
        return True
    print("false 3")
    return False

def check_mail(partner_mail: str):
    ''' Проверка почты партнера '''
    # Регулярное выражение для проверки почты
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, partner_mail):
        return True
    print("false 4")
    return False

def check_ur_addr(partner_ur_addr: str):
    ''' Проверка Юрид адреса '''
    if (len(partner_ur_addr.split(',')[0]) == 6 and
    partner_ur_addr.split(',')[0].isdigit() and
    len(partner_ur_addr[6:]) > 1):
        return True
    print("false 5")
    return False

def check_rate(partner_rate):
    ''' Проверка рейтинга от 1 до 10 '''
    try:
        if (int(partner_rate) in range(1, 11)):
            return True
        print("false 6")
        return False
    except Exception:
        print("false 66")
        return False

def check_inn(partner_inn: str):
    try:

        if (partner_inn.isdigit() and
        len(partner_inn) == 10):
            return True
        print("false 7")
        return False
    except Exception:
        print("false 77")
        return False

def check_phone(partner_phone: str):
    ''' Проверка номера телефона (он должен быть 999 999 99 99) '''
    try:
        regex = re.compile(r'[94][0-9][0-9] [0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]')
        if re.fullmatch(regex, partner_phone):
            return True
        print("false 8")
        return False
    except Exception:
        print("false 88")
        return False