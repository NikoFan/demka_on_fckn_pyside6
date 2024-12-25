import psycopg2

# Классы
from Partner import Partner
from .config import *

# Файл проверки информации
import check_input_info

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
        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return None

    # Получение суммы продаж от _определенного_ партнера
    def get_sum_sales(self, partner_name: str):
        '''
        Функция получения суммы продаж
        :param partner_name: Имя партнера для которого ищется сумма продаж
        :return: Цифра продаж
        '''
        try:
            cursor = self.connection.cursor()

            query = f"""
                SELECT SUM(history_products_count) as sale_result
                FROM history
                WHERE partner_name_fk = '{partner_name}';
            """

            # Исполнение запроса
            cursor.execute(query)

            # В ответ приходит 1 строка с 1 значением
            answer = cursor.fetchone()

            # Список со словарем, где хранится результат запроса
            if answer:
                cursor.close()
                # Возвращаем то значение из строки
                return answer[0]

            return None
        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return None

    # Извлечение информации по партнерам
    def get_partners(self):
        '''
        Функция получения информации о пользователе
        :return: Список с словарями, в которых хранится вся информация о партнерах
        '''
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

            partners_data_list = []
            for row in cursor.fetchall():
                partners_data_list.append({
                    "name": row[0],
                    "phone": row[1],
                    "type": row[2],
                    "mail": row[3],
                    "ur_addr": row[4],
                    "inn": row[5],
                    "rate": row[6],
                    "director": row[7]
                })


            # Закрытие запроса
            cursor.close()
            return partners_data_list
        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return []

    # Добавление партнера в БД
    def add_partner(self, partner_data: dict):
        '''
        Функция добавления нового партнера в таблицу partners
        :param partner_data: Словарь с данными на добавление
        :return: True / False : Успешно / Ошибка
        '''
        try:
            # Отправка поступивших данных на проверку в check_input_info.py
            if not check_input_info.routes(partner_data):
                # Если проверка не пройдена -> Отклонено в регистрации
                print("Проверка данных выявила ошибку")
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
        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return False

    # Извлечение информации по _определенному_ партнеру
    def get_partner_by_name(self, partner_name: str):
        '''
        Получение информации о партнере по имени
        :param partner_name: Имя партнера, чья информация нужна для работы
        :return: словарь с данными о партнере
        '''
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
        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return None

    # Закрытие соединения с БД
    def close(self):
        ''' Закрытие соединения с базой данных '''

        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")

    # Обновление информации про партнера
    def update_partners_data(self, new_partner_data_to_update: dict):
        '''
        Функция обновления информации о партнере
        :param new_partner_data_to_update: Словарь с данными для обновления
        :return: True - Обновилось / False - Ошибка работы
        '''
        try:
            # Отправка поступивших данных на проверку в check_input_info.py
            if not check_input_info.routes(new_partner_data_to_update):
                print("Проверка данных выявила ошибку")
                return False

            print("complete")

            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = f'''
            UPDATE partners
            SET
            partner_type = '{new_partner_data_to_update['type']}',
            partner_name = '{new_partner_data_to_update['name']}',
            partner_director = '{new_partner_data_to_update['director']}',
            partner_mail = '{new_partner_data_to_update['mail']}',
            parnter_phone = '{new_partner_data_to_update['phone']}',
            partner_ur_addr = '{new_partner_data_to_update['ur_addr']}',
            partner_inn = '{new_partner_data_to_update['inn']}',
            partner_rate = {new_partner_data_to_update['rate']}

            WHERE partner_name = '{Partner.get_name()}';
            '''

            # Исполнение запроса
            cursor.execute(query)

            # Сохранение изменений
            self.connection.commit()

            # Закрытие инструмента
            cursor.close()
            return True

        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return False

    # Получение истории о продажах партнера
    def get_sales_data(self, partner_name: str):
        '''
        Функция получения истории продаж партнера
        :param partner_name: Имя партнера, для которого собирается история
        :return: sales_history - Список с данными для таблицы истории
        '''
        try:
            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = f"""
                SELECT product_name_fk, partner_name_fk, history_products_count, history_sale_date
                FROM history
                WHERE partner_name_fk = '{partner_name}'
            """

            # Исполнение запроса
            cursor.execute(query)

            # Список со словарем, где хранится результат запроса
            sales_history = []
            for row in cursor.fetchall():
                sales_history.append({
                    "product_name": row[0].strip(),
                    "partner_name": row[1].strip(),
                    "quantity": str(row[2]),
                    "sale_date": str(row[3])
                })

            # Закрытие инструмента
            cursor.close()
            return sales_history
        except Exception as error_string:
            print(f"Ошибка выполнения запроса: {error_string}")
            return []

