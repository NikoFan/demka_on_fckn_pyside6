# Библиотеки
from math import trunc

import psycopg2

# Классы
from Partner import Partner
from .config import *

# Файл проверки информации
from check_input_info import *

'''
-> Класс Database используется для работы с БД
    В нем осуществляются все взаимодействия с Базой данных
    Это позволяет не терять функции в других классах, а хранить их в одном
'''


class Database:
    def __init__(self):
        self.connection = self.connect_db()

    # Подключение к Базе данных
    def connect_db(self):
        ''' Установка соединения с БД в Postgresql '''

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            print("Соединение с базой данных установлено")
            return connection
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    # Получение суммы продаж от _определенного_ партнера
    def get_sum_sales(self, partner_name: str):
        ''' Полученгие суммы продаж партнера
        partner_name: str -> имя _определенного_ партнера '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return []

        try:
            # Инициализация инструмента для работы с БД
            # cursor -> используется для запуска и обработки запросов
            cursor = self.connection.cursor()

            # Запрос получения СУММЫ продаж из таблицы history
            # Где имя партнера равняется _определенному_
            query = f"""
                SELECT SUM(history_products_count) as result_pr
                FROM history
                WHERE partner_name_fk = '{partner_name}';
            """

            # Исполнение запроса
            cursor.execute(query, (partner_name,))

            # Список со словарем, где хранится результат запроса
            sales_data = [
                {
                    "count": row[0]
                }
                # Перебор кортежа на выходе из запроса
                for row in cursor.fetchall()
            ]

            # Отключение инструмента
            cursor.close()
            return sales_data
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    # Извлечение информации по партнерам
    def get_partners(self):
        ''' Извлечение кортежа с информацией по партнерам '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return []

        try:
            # Инструмент для работы с Запросами БД
            cursor = self.connection.cursor()

            # Запрос
            query = """
                SELECT partner_name, parnter_phone, partner_type, partner_mail, 
                       partner_ur_addr, partner_inn, partner_rate, partner_director 
                FROM partners;
            """

            # Исполнение Запроса
            cursor.execute(query)

            # Список со словарем выходных данных из запроса
            partners = [
                {
                    "name": row[0],
                    "phone": row[1],
                    "type": row[2],
                    "mail": row[3],
                    "ur_addr": row[4],
                    "inn": row[5],
                    "rate": row[6],
                    "director": row[7]
                }
                # Перебор результата работы запроса
                for row in cursor.fetchall()
            ]

            # Закрытие запроса
            cursor.close()
            return partners
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    # Добавление партнера в БД
    def add_partner(self, partner_data: dict):
        ''' Добавление нового партнера в БД
        partner_data: dict -> словарь с данными на регистрацию '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return False

        try:
            # Отправка поступивших данных на проверку в check_input_info.py
            if not route(partner_data):
                # Если проверка не пройдена -> Отклонено в регистрации
                return False

            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос для добавления нового запроса
            query = """
                INSERT INTO partners (partner_type, partner_name, partner_director, partner_mail, 
                                      parnter_phone, partner_ur_addr, partner_inn, partner_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Исполнение запроса
            cursor.execute(query, (
                partner_data['type'],
                partner_data['name'],
                partner_data['director'],
                partner_data['mail'],
                partner_data['phone'],
                partner_data['ur_addr'],
                partner_data['inn'],
                partner_data['rate']
            ))

            # Сохранение изменений в БД
            self.connection.commit()

            # Закрытие инструмента
            cursor.close()
            print(f"Партнер '{partner_data['name']}' успешно добавлен.")
            return True
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return False

    # Извлечение информации по _определенному_ партнеру
    def get_partner_by_name(self, partner_name: str):
        ''' Извлечение информации из БД по имени определенного партнера
        partner_name: str -> имя _определенного_ партнера '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return None

        try:
            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = """
                SELECT partner_name, parnter_phone, partner_type, partner_mail, 
                       partner_ur_addr, partner_inn, partner_rate, partner_director 
                FROM partners
                WHERE partner_name = %s;
            """

            # Исполнение запроса
            cursor.execute(query, (partner_name,))

            # Перебор выходных кортежей функцией python
            row = cursor.fetchone()

            # Отключение инструмента
            cursor.close()

            # Возврат информации про партнера
            if row:
                return {
                    "name": row[0],
                    "phone": row[1],
                    "type": row[2],
                    "mail": row[3],
                    "ur_addr": row[4],
                    "inn": row[5],
                    "rate": str(row[6]),
                    "director": row[7]
                }
            else:
                print(f"Партнер с именем '{partner_name}' не найден.")
                return None
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    # Закрытие соединения с БД
    def close(self):
        ''' Закрытие соединения с базой данных '''

        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")

    # Обновление информации про партнера
    def update_partners_data(self, res: dict):
        ''' Обновление данных _определенного_ партнера в таблицу partners
        res: dict -> ресурсы, которые изменяются '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return False
        try:
            # Отправка поступивших данных на проверку в check_input_info.py
            if not route(res):
                print(9)
                return False

            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = f'''
            UPDATE partners
            SET
            partner_type = '{res['type']}',
            partner_name = '{res['name']}',
            partner_director = '{res['director']}',
            partner_mail = '{res['mail']}',
            parnter_phone = '{res['phone']}',
            partner_ur_addr = '{res['ur_addr']}',
            partner_inn = '{res['inn']}',
            partner_rate = {res['rate']}

            WHERE partner_name = '{Partner.get_name()}';
            '''

            # Исполнение запроса
            cursor.execute(query)

            # Сохранение изменений
            self.connection.commit()

            # Закрытие инструмента
            cursor.close()
            return True

        except Exception:
            return False

    # Получение истории о продажах партнера
    def get_sales_data(self, partner_name: str):
        ''' Получение информации из таблицы history про историю торговли _определенного_ партнера
        partner_name: str -> имя _определенного_ партнера '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return []

        try:
            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = """
                SELECT 
                    p.product_name AS product_name,
                    pr.partner_name AS partner_name,
                    h.history_products_count AS quantity,
                    h.history_sale_date AS sale_date
                FROM 
                    history h
                JOIN 
                    products p ON h.product_name_fk = p.product_name
                JOIN 
                    partners pr ON h.partner_name_fk = pr.partner_name
                WHERE 
                    pr.partner_name = %s;
            """

            # Исполнение запроса
            cursor.execute(query, (partner_name,))

            # Список со словарем, где хранится результат запроса
            sales_data = [
                {
                    "product_name": row[0].strip(),
                    "partner_name": row[1].strip(),
                    "quantity": row[2],
                    "sale_date": row[3]
                }
                # Перебор кортежа от запроса
                for row in cursor.fetchall()
            ]

            # Закрытие инструмента
            cursor.close()
            return sales_data
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    # Проверка дубликата ИНН
    def check_duplicate_inn(self, inn: str):
        ''' Проверка на совпадение ИНН нового партнера
        inn: str -> ИНН партнера '''

        if not self.connection:
            print("Нет соединения с базой данных.")
            return None

        try:
            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = """
                SELECT partner_inn
                FROM partners
                WHERE partner_inn LIKE '%s'
            """

            # Исполнение запроса
            cursor.execute(query, (inn,))

            # Перебор выходных кортежей функцией python
            row = cursor.fetchone()

            # Отключение инструмента
            cursor.close()

            # Возврат информации про партнера
            if row:
                return True
            else:
                return False
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return False