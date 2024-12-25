import psycopg2

import config

'''
Таблицы должны создаваться в соответствии с предметной областью
'''

def create_table_partners(connection_string):
    '''
    Функция создания таблицы partners
    :param connection_string: Строка подключения к БД на сервере postgresql
    :return: None - Мы ничего не возвращаем из функции
    '''

    # Создание запроса
    query = '''
    -- Партнеры Excel partners_import
    create table partners(
    partner_type nchar(10) not null,
    partner_name nchar(50) primary key not null,
    partner_director nchar(70) not null,
    partner_mail nchar(100) not null,
    partner_phone nchar(13) not null, -- Пример 903 778 48 65 (+7 добавляется в программе)
    partner_ur_addr nchar(200) not null, -- Юрид адрес партнера
    partner_INN nchar(10) not null, -- ИНН партнера (там лучше подойдет bigint, но я решил nchar())
    partner_rate int not null -- Рейтинг партнера от 0 до 10
    );
    '''

    # Создание курсора для работы с БД
    cursor_to_work_with_db = connection_string.cursor()

    # Выполнение запроса
    cursor_to_work_with_db.execute(query)

    cursor_to_work_with_db.close()

    # Сохранение изменений
    connection_string.commit()

def create_table_product_type(connection_string):
    query = '''
    -- Типы продукции Excel product_type_import
    create table product_type(
    product_type_name nchar(50) primary key not null,
    product_index real not null -- Дробное число
    );
    '''
    # Создание курсора для работы с БД
    cursor_to_work_with_db = connection_string.cursor()

    # Выполнение запроса
    cursor_to_work_with_db.execute(query)

    cursor_to_work_with_db.close()

    # Сохранение изменений
    connection_string.commit()

def create_table_products(connection_string):
    query = '''
    -- Продукты Excel products_import
    create table products(
    product_type_name_fk nchar(50) not null, -- Вторичный ключ
    FOREIGN KEY (product_type_name_fk) REFERENCES product_type(product_type_name) on update cascade, -- При обновлении первичного ключа, обновляется вторичный ключ
    product_name nchar(250) primary key not null,
    product_article bigint not null, -- Я не знаю почему это не PK, но в Excel оно негде не используется
    product_min_cost real not null -- Минимальная стоимость для партнера
    );
    '''
    # Создание курсора для работы с БД
    cursor_to_work_with_db = connection_string.cursor()

    # Выполнение запроса
    cursor_to_work_with_db.execute(query)

    cursor_to_work_with_db.close()

    # Сохранение изменений
    connection_string.commit()

def create_table_partner_products(connection_string):
    query = '''
    -- История Excel partner_product_import
    create table history(
    product_name_fk nchar(250) not null,
    FOREIGN KEY (product_name_fk) REFERENCES products (product_name) on update cascade,
    partner_name_fk nchar(50) not null,
    FOREIGN KEY (partner_name_fk) REFERENCES partners (partner_name) on update cascade,
    history_products_count bigint not null,
    history_sale_date date not null
    );
    '''
    # Создание курсора для работы с БД
    cursor_to_work_with_db = connection_string.cursor()

    # Выполнение запроса
    cursor_to_work_with_db.execute(query)

    cursor_to_work_with_db.close()

    # Сохранение изменений
    connection_string.commit()

def create_table_material_type(connection_string):
    query = '''
    -- Тип материала Excel material_type_import
    create table material_type(
    material_type_name nchar(30) primary key not null,
    material_break_percent nchar(7) not null -- Процент брака (я не знаю как процент ЗАПИСАТЬ)
    );
    '''
    # Создание курсора для работы с БД
    cursor_to_work_with_db = connection_string.cursor()

    # Выполнение запроса
    cursor_to_work_with_db.execute(query)

    cursor_to_work_with_db.close()

    # Сохранение изменений
    connection_string.commit()


def start():
    # Создание строки подключения к БД на сервере
    database_connection_string = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )

    # create_table_partners(database_connection_string)
    # create_table_product_type(database_connection_string)
    create_table_products(database_connection_string)
    create_table_partner_products(database_connection_string)
    create_table_material_type(database_connection_string)
    print("DONE")
start()
