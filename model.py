from view import View

from random import choice
from datetime import datetime

import psycopg2
import psycopg2.extras
from psycopg2.extras import DictCursor


class Model:
    def __init__(self):
        self.view_obj = View()

    def connect(self):
        return psycopg2.connect(dbname='lab1', user='postgres', password='Sqlpr0v0d0k', host='localhost')

    def generate_random_data(self, cursor, length):
        uppercase_letter = "chr(ascii('A') + (random() * 25)::int)"
        lowercase_letter = "chr(ascii('a') + (random() * 25)::int)"
        cursor.execute(f"""SELECT ({uppercase_letter}{(" || " + lowercase_letter) * (length - 1)})""")

        return cursor.fetchone()[0]

    def get_last_entry_from_column(self, table_name, column_name, cursor):
        cursor.execute(f"""SELECT {column_name} FROM \"{table_name}\"
        ORDER BY {column_name} DESC LIMIT 1""")
        return cursor.fetchone()[0]

    def get_column_names(self, cursor, table_name):
        cursor.execute(f"SELECT * FROM \"{table_name}\"")
        return [item[0] for item in cursor.description]

    def get_list_from_column(self, cursor):
        # converting [(item, ), (item, ), ...] to [item, item, ...]
        return [item[0] for item in cursor.fetchall()]

    def get_column_names_to_view(self, table_num):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                table_name = self.view_obj.tables[table_num]
                return self.get_column_names(cursor, table_name)

    def insert_data_controller(self, table_num):
        if table_num == 1:
            data = self.view_obj.input_client()
            self.insert_into_client(*data)
        elif table_num == 2:
            print("You can pass date column, Enter ' - '")
            data = self.view_obj.input_order()
            self.insert_into_order(*data)
        elif table_num == 3:
            data = self.view_obj.input_product()
            self.insert_into_product(*data)
        elif table_num == 4:
            data = self.view_obj.input_product_category()
            self.insert_into_product_category(*data)
        elif table_num == 5:
            data = self.view_obj.input_store()
            self.insert_into_store(*data)
        elif table_num == 6:
            data = self.view_obj.input_department()
            self.insert_into_store_department(*data)
        elif table_num == 7:
            print("You cannot insert data into this table")

    def tables_parser_controller(self, table_num, data, mode):
        with open("table.txt", mode) as file:
            if table_num == 1:
                self.view_obj.client_parser(data, file)
            elif table_num == 2:
                self.view_obj.order_parser(data, file)
            elif table_num == 3:
                self.view_obj.product_parser(data, file)
            elif table_num == 4:
                self.view_obj.product_category_parser(data, file)
            elif table_num == 5:
                self.view_obj.store_parser(data, file)
            elif table_num == 6:
                self.view_obj.store_department_parser(data, file)
            elif table_num == 7:
                self.view_obj.order_product_parser(data, file)

    def select_table(self, table_num, file_open_mode):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM \"{self.view_obj.tables[table_num]}\"")
                self.tables_parser_controller(table_num, cursor.fetchall(), file_open_mode)

    def select_all_tables(self):
        with open("table.txt", "w"):  # clear file
            pass
        for i in range(1, 8):
            self.select_table(i, "a")

    def insert_into_client(self, name):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO \"Client\" (name)
                VALUES('{name}');""")

    def insert_into_order(self, date, category_id, client_id, store_id, product_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                if date == "-":
                    date = datetime.now().strftime("%H:%M:%S")
                cursor.execute(f"""INSERT INTO \"Order\" (date, category_id, store_id, client_id)
                VALUES('{date}', {category_id}, {store_id}, {client_id});""")

        self.insert_into_order_product(product_id)

    def insert_into_order_product(self, product_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                last_order_id = self.get_last_entry_from_column("Order", "order_id", cursor)

                cursor.execute(f"""INSERT INTO \"order_product\" (order_id, product_id)
                VALUES({last_order_id}, {product_id});""")

    def insert_into_product(self, name, price, category_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO \"Product\" (name, price, category_id)
                VALUES('{name}', {price}, {category_id});""")

    def insert_into_product_category(self, name, department_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO \"Product_category\" (name, department_id)
                VALUES('{name}', {department_id});""")

    def insert_into_store(self, name, address):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO \"Store\" (name, address)
                VALUES('{name}', '{address}');""")

    def insert_into_store_department(self, name, store_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO \"Store_department\" (name, store_id)
                VALUES('{name}', {store_id})""")

    def insert_random_data_packet(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                # INSERT INTO "Client"
                self.insert_into_client(self.generate_random_data(cursor, 5))

                # INSERT INTO "Product"
                product_name = self.generate_random_data(cursor, 7)
                cursor.execute(f"""SELECT category_id FROM \"Product_category\"""")
                category = choice(self.get_list_from_column(cursor))
                self.insert_into_product(product_name, '(random() * 3000)::int', category)

                # INSERT INTO "Order" and "order_product"
                cursor.execute(f"""SELECT client_id FROM \"Client\"""")
                client_id = choice(self.get_list_from_column(cursor))
                new_product_id = self.get_last_entry_from_column("Product", "product_id", cursor)
                self.insert_into_order('-', category, client_id, 1, new_product_id)

                # INSERT INTO "Product_category"
                self.insert_into_product_category(self.generate_random_data(cursor, 7), 14)

                # INSERT INTO "Store"
                store_name = self.generate_random_data(cursor, 5)
                city = self.generate_random_data(cursor, 5)
                street = self.generate_random_data(cursor, 8)
                self.insert_into_store(store_name, city + ", " + street)

                # INSERT INTO "Store_department"
                cursor.execute("SELECT store_id FROM \"Store\"")
                store_id = choice(self.get_list_from_column(cursor))
                self.insert_into_store_department(self.generate_random_data(cursor, 5), store_id)

    def update_table(self, table_num, data):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                table_name = self.view_obj.tables[table_num]
                column_names = self.get_column_names(cursor, table_name)
                id_name = column_names[0]

                for i, column in enumerate(column_names[1:], start=1):
                    if data[i] != '-':
                        cursor.execute(f"""UPDATE \"{table_name}\"
                        SET {column} = '{data[i]}' WHERE {id_name} = {data[0]}""")

                if table_num == 2:
                    if data[1] == '-':  # update order time
                        cursor.execute(f"""UPDATE \"{table_name}\"
                        SET date = '{datetime.now().strftime("%H:%M:%S")}' WHERE {id_name} = {data[0]}""")
                    self.update_table(7, [data[0], data[-1]])

    def delete_data(self, table_num, id_to_delete):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                table_name = self.view_obj.tables[table_num]
                cursor.execute(f"SELECT * FROM \"{table_name}\"")
                id_column_name = cursor.description[0][0]

                # begin == first value, end == second value (if it exists)
                # if there is no second value end == begin
                begin, end = id_to_delete[0], id_to_delete[-(len(id_to_delete) - 1)] + 1

                for i in range(begin, end):
                    cursor.execute(f"DELETE FROM \"{table_name}\" WHERE {id_column_name} = {i};")

    def string_search(self, cursor, table_names_list, column_name, data):
        for table in table_names_list:
            cursor.execute(f"""SELECT * FROM \"{table}\" WHERE {column_name} LIKE '{data}'""")
            print("---------------------------------------------------------")
            for i in cursor:
                print(table + ": " + str(i))

    def integer_search(self, cursor, table_names_list, column_name, min_value, max_value):
        for table in table_names_list:
            cursor.execute(f"""SELECT * FROM \"{table}\"
            WHERE {min_value} <= {column_name} AND {column_name} <= {max_value};""")
            print("---------------------------------------------------------")
            for i in cursor:
                print(table + ": " + str(i))

    def date_search(self, cursor, table_names_list, column_name, min_value, max_value):
        for table in table_names_list:
            cursor.execute(f"""SELECT * FROM \"{table}\"
            WHERE {column_name} BETWEEN '{min_value}' AND '{max_value}'""")
            print("---------------------------------------------------------")
            for i in cursor:
                print(table + ": " + str(i))

    def search_controller(self, cursor, table_names_list, column_name, data_type, data):
        print("\n#########################################################")
        print(f"#########\tSearch by '{column_name}' column with {data}")
        if data_type == 'integer':
            self.integer_search(cursor, table_names_list, column_name, *data)
        elif data_type == 'character varying':
            self.string_search(cursor, table_names_list, column_name, data)
        elif data_type == 'time without time zone':
            self.date_search(cursor, table_names_list, column_name, *data)
        print("#########################################################\n\n")


    def search_into_table(self, table_num, search_param):
        with self.connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                table_name = self.view_obj.tables[table_num]
                column_names = self.get_column_names(cursor, table_name)
                column = column_names[search_param]

                cursor.execute(f"""SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE COLUMN_NAME = '{column}'""")
                table_names_list = self.get_list_from_column(cursor)

                cursor.execute(f"""SELECT * FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME  = '{column}'""")
                data_type = cursor.fetchone()['data_type']

                data_to_search = self.view_obj.input_data_to_search(data_type)
                self.search_controller(cursor, table_names_list, column, data_type, data_to_search)
