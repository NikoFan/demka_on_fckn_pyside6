import pandas as pd
import psycopg2 as pg

from config import *


'''
При выводе строк датафрейма по какой-то причине некоторые столбцы отображались как _1 и _2,
 а некоторые словами по типу Директор
Поэтому при заполнении таблиц используется разное наименование
'''


# Верный код добавления - остальные пока не работают
def Partners_import(table_name: str, database):
    ''' Заполнение '''
    print("excel/" + table_name + ".xlsx")
    df = pd.read_excel("/home/student/IdeaProjects/Demka/excel/"+table_name, engine='openpyxl')
    print(df)
    query = """INSERT INTO partners VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor = database.cursor()
    for stroka in df.itertuples():
        print(stroka)
        print(stroka._1)
        partner_type = stroka._1
        partner_name = stroka._2
        partner_director = stroka.Директор
        partner_mail = stroka._4
        partner_phone = stroka._5
        partner_ur_addr = stroka._6
        partner_INN = stroka.ИНН
        partner_rate = stroka.Рейтинг

        values = (partner_type,
                  partner_name,
                  partner_director,
                  partner_mail,
                  partner_phone,
                  partner_ur_addr,
                  partner_INN,
                  partner_rate)

        cursor.execute(query, values)

    cursor.close()

    database.commit()

def Product_type_import(table_name: str, database):
    ''' Заполнение '''
    query = """INSERT INTO product_type VALUES (%s, %s)"""
    df = pd.read_excel("/home/student/IdeaProjects/Demka/excel/" + table_name, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        product_type_name = r._1
        product_index = r._2

        values = (product_type_name,
                  product_index,)

        cursor.execute(query, values)

    cursor.close()
    database.commit()


def Products_import(table_name: str, database):
    ''' Заполнение '''

    query = """INSERT INTO products VALUES (%s, %s, %s, %s)"""
    df = pd.read_excel("/home/student/IdeaProjects/Demka/excel/" + table_name, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        product_type_name_fk = r._1
        product_name = r._2
        product_article = r.Артикул
        product_min_cost = r._4

        values = (product_type_name_fk,
                  product_name,
                  product_article,
                  product_min_cost)

        cursor.execute(query, values)

    cursor.close()
    database.commit()


def Partner_products_import(table_name: str, database):
    ''' Заполнение '''
    query = """INSERT INTO history VALUES (%s, %s, %s, %s)"""
    df = pd.read_excel("/home/student/IdeaProjects/Demka/excel/" + table_name, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        product_name_fk = r.Продукция
        partner_name_fk = r._2
        history_products_count = r._3
        history_sale_date = r._4

        values = (product_name_fk,
                  partner_name_fk,
                  history_products_count,
                  history_sale_date)

        cursor.execute(query, values)

    cursor.close()
    database.commit()

def Material_type_import(table_name: str, database):
    ''' Заполнение '''
    query = """INSERT INTO material_type VALUES (%s, %s)"""
    df = pd.read_excel("/home/student/IdeaProjects/Demka/excel/" + table_name, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        material_type_name = r._1
        material_break_percent = r._2

        values = (material_type_name,
                  material_break_percent)

        cursor.execute(query, values)

    cursor.close()
    database.commit()


def insert_table():
    ''' Вызов всех файлов для импорта '''

    database = pg.connect(database=db_name,
                          user=user,
                          password=password,
                          host=host,
                          port=port)

    # Partners_import("Partners_import.xlsx", database)
    # Product_type_import("Product_type_import.xlsx", database)
    # Products_import("Products_import.xlsx", database)
    # Partner_products_import("Partner_products_import.xlsx", database)
    # Material_type_import("Material_type_import.xlsx", database)




# Вызов работы функции
insert_table()