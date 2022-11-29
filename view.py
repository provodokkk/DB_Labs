import psycopg2


class View:
    def __init__(self):
        self.tables = {
                1: 'Client',
                2: 'Order',
                3: 'Product',
                4: 'Product_category',
                5: 'Store',
                6: 'Store_department',
                7: 'order_product',
                8: 'Exit the program',
        }

    def menu_parser(self, func, file_path, end):
        with open(file_path, "r") as file:
            print(file.read())
        param = int(input("Enter choice № "))

        if param < 1 or param > end:
            print(f"Enter the number from 1 to {end} <--------- warning")
            return func()
        else:
            return param

    def operations_menu(self):
        return self.menu_parser(self.operations_menu, "operations_menu.txt", 8)

    def tables_menu(self):
        return self.menu_parser(self.tables_menu, "tables_menu.txt", 7)

    def client_parser(self, data, file):
        file.write("\n" + " Client ".center(75, "=") + "\n")
        file.write("client_id".center(17, " ") + "name".center(15, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(15, " ")
                       + str(item[1]) + "\n")

    def order_parser(self, data, file):
        file.write("\n" + " Order ".center(75, "=") + "\n")
        file.write("order_id".center(17, " ")
                   + "date".center(15, " ")
                   + "category_id".center(15, " ")
                   + "client_id".center(15, " ")
                   + "store_id".center(15, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(12, " ")
                       + str(item[1]).ljust(18, " ")
                       + str(item[2]).ljust(15, " ")
                       + str(item[3]).ljust(15, " ")
                       + str(item[4]) + "\n")

    def product_parser(self, data, file):
        file.write("\n" + " Product ".center(75, "=") + "\n")
        file.write("product_id".center(17, " ")
                   + "name".center(15, " ")
                   + "price".center(25, " ")
                   + "category_id".center(10, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(10, " ")
                       + str(item[1]).ljust(25, " ")
                       + str(item[2]).ljust(20, " ")
                       + str(item[3]) + "\n")

    def product_category_parser(self, data, file):
        file.write("\n" + " Product_category ".center(75, "=") + "\n")
        file.write("category_id".center(17, " ")
                   + "name".center(17, " ")
                   + "department_id".center(17, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(15, " ")
                       + str(item[1]).ljust(20, " ")
                       + str(item[2]) + "\n")

    def store_parser(self, data, file):
        file.write("\n" + " Store ".center(75, "=") + "\n")
        file.write("store_id".center(17, " ")
                   + "name".center(17, " ")
                   + "address".center(17, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(15, " ")
                       + str(item[1]).ljust(15, " ")
                       + str(item[2]) + "\n")

    def store_department_parser(self, data, file):
        file.write("\n" + " Store_department ".center(75, "=") + "\n")
        file.write("department_id".center(17, " ")
                   + "name".center(17, " ")
                   + "store_id".center(17, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(15, " ")
                       + str(item[1]).ljust(20, " ")
                       + str(item[2]) + "\n")

    def order_product_parser(self, data, file):
        file.write("\n" + " Order_product ".center(75, "=") + "\n")
        file.write("order_id".center(17, " ")
                   + "product_id".center(17, " ") + "\n")

        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " ")
                       + str(item[0]).ljust(15, " ")
                       + str(item[1]) + "\n")

    def input_client(self):
        return input("Enter name: ")

    def input_order(self):
        date = input("Enter date: ")
        category_id = input("Enter category_id: ")
        client_id = input("Enter client_id: ")
        store_id = input("Enter store_id: ")
        product_id = input("Enter product_id: ")
        return [date, category_id, client_id, store_id, product_id]

    def input_product(self):
        product_name = input("Enter product_name: ")
        price = input("Enter price: ")
        category_id = input("Enter category_id: ")
        return [product_name, price, category_id]

    def input_product_category(self):
        category_name = input("Enter category_name: ")
        department_id = input("Enter department_id: ")
        return [category_name, department_id]

    def input_store(self):
        store_name = input("Enter store_name: ")
        address = input("Enter address: ")
        return [store_name, address]

    def input_department(self):
        department_name = input("Enter department_name: ")
        store_id = input("Enter store_id: ")
        return [department_name, store_id]

    def update_data(self, table_num):
        updated_data = {
            1: self.input_client,
            2: self.input_order,
            3: self.input_product,
            4: self.input_product_category,
            5: self.input_store,
            6: self.input_department,
        }
        row_id = input("Enter ID: ")
        print("If you want to skip a column, then enter the character '-'")
        return [row_id, *(updated_data[table_num]())]

    def delete(self):
        id_range = input("Select id range (x y) or just id (x): ").split()
        return [int(i) for i in id_range]

    def search(self, column_names):
        for i, column in enumerate(column_names):
            print(str(i) + ": " + column)

        return int(input("\nEnter choice № "))

    def input_data_to_search(self, data_type):
        if data_type == 'integer':
            min_value = input("Enter min value: ")
            max_value = input("Enter max value: ")
            return [min_value, max_value]
        elif data_type == 'character varying':
            return input("Enter data: ")
        elif data_type == 'time without time zone':
            min_value = input("Enter HH:MM:SS min date: ")
            max_value = input("Enter HH:MM:SS max date: ")
            return [min_value, max_value]
        else:
            print(f"Cannot find data with '{data_type}' type")

