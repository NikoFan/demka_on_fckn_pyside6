import pandas as pd

# Классы
from database import Database

'''
При выводе строк датафрейма по какой-то причине некоторые столбцы отображались как _1 и _2,
 а некоторые словами по типу Директор
Поэтому при заполнении таблиц используется разное наименование
'''

def Partners_import(table_name: str):
    ''' Заполнение '''
    print("excel_files/" + table_name + ".xlsx")
    df = pd.read_excel("./excel_files/" + table_name + ".xlsx", engine='openpyxl')
    query = """INSERT INTO partners VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    # cursor = Database.cursor()
    for r in df.itertuples():
        print("-------")
        print(r)
        print(r._1)
        partner_type = r._1
        partner_name = r._2
        partner_director = r.Директор
        partner_mail = r._4
        partner_phone = r._5
        partner_ur_addr = r._6
        partner_INN = r.ИНН
        partner_rate = r.Рейтинг

        values = (partner_type,
                  partner_name,
                  partner_director,
                  partner_mail,
                  partner_phone,
                  partner_ur_addr,
                  partner_INN,
                  partner_rate)

        # cursor.execute(query, values)

    # cursor.close()
    # .commit

def Product_type_import(table_name: str):
    ''' Заполнение '''
    query = """INSERT INTO product_type VALUES (%s, %s)"""
    df = pd.read_excel("./excel_files/" + table_name + ".xlsx", engine='openpyxl')
    # cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        product_type_name = r._1
        product_index = r._2

        values = (product_type_name,
                  product_index,)

        # cursor.execute(query, values)

        # cursor.close()
    # .commit


def Products_import(table_name: str):
    ''' Заполнение '''

    query = """INSERT INTO products VALUES (%s, %s, %s, %s)"""
    df = pd.read_excel("./excel_files/" + table_name + ".xlsx", engine='openpyxl')
    # cursor = database.cursor()
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

        # cursor.execute(query, values)

    # cursor.close()

    # database.commit()


def Partner_products_import(table_name: str):
    ''' Заполнение '''
    query = """INSERT INTO history VALUES (%s, %s, %s, %s)"""
    df = pd.read_excel("./excel_files/" + table_name + ".xlsx", engine='openpyxl')
    # cursor = database.cursor()
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

        # cursor.execute(query, values)

    # cursor.close()

    # database.commit()


def Material_type_import(table_name: str):
    ''' Заполнение '''
    query = """INSERT INTO material_type VALUES (%s, %s)"""
    df = pd.read_excel("./excel_files/" + table_name + ".xlsx", engine='openpyxl')
    # cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        material_type_name = r._1
        material_break_percent = r._2

        values = (material_type_name,
                  material_break_percent)

        # cursor.execute(query, values)

    # cursor.close()

    # database.commit()


def insert_table():
    ''' Вызов всех файлов для импорта '''



    # Partners_import("Partners_import")
    #Product_type_import("Product_type_import")
    # Products_import("Products_import")
    # Partner_products_import("Partner_products_import")
    # Material_type_import("Material_type_import")




# Вызов файлов

insert_table()