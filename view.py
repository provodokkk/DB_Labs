from typing import List, Tuple


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

    @staticmethod
    def menu_parser(func, file_path, end):
        with open(file_path, "r") as file:
            print(file.read())
        param = int(input("Enter choice № "))

        if param < 1 or param > end:
            print(f"Enter the number from 1 to {end} <--------- warning")
            return func()
        else:
            return param

    def operations_menu(self):
        return self.menu_parser(self.operations_menu, "operations_menu.txt", 7)

    def tables_menu(self):
        return self.menu_parser(self.tables_menu, "tables_menu.txt", 7)

    @staticmethod
    def write_data_to_file(file, data, indents: Tuple) -> None:
        for i, item in enumerate(data, start=1):
            file.write(str(i).ljust(8, " "))
            for j, indent in enumerate(indents):
                file.write(str(item[j]).ljust(indent, " "))
            file.write("\n")

    def client_parser(self, data, file):
        file.write("\n" + " Client ".center(75, "=") + "\n")
        file.write("client_id".center(17, " ") + "name".center(15, " ") + "\n")
        indents = (15, 0)
        self.write_data_to_file(file, data, indents)

    def order_parser(self, data, file):
        file.write("\n" + " Order ".center(75, "=") + "\n")
        file.write("order_id".center(17, " ")
                   + "date".center(15, " ")
                   + "category_id".center(15, " ")
                   + "client_id".center(15, " ")
                   + "store_id".center(15, " ") + "\n")

        indents = (12, 18, 15, 15, 0)
        self.write_data_to_file(file, data, indents)

    def product_parser(self, data, file):
        file.write("\n" + " Product ".center(75, "=") + "\n")
        file.write("product_id".center(17, " ")
                   + "name".center(15, " ")
                   + "price".center(25, " ")
                   + "category_id".center(10, " ") + "\n")

        indents = (10, 25, 20, 0)
        self.write_data_to_file(file, data, indents)

    def product_category_parser(self, data, file):
        file.write("\n" + " Product_category ".center(75, "=") + "\n")
        file.write("category_id".center(17, " ")
                   + "name".center(17, " ")
                   + "department_id".center(17, " ") + "\n")

        indents = (15, 20, 0)
        self.write_data_to_file(file, data, indents)

    def store_parser(self, data, file):
        file.write("\n" + " Store ".center(75, "=") + "\n")
        file.write("store_id".center(17, " ")
                   + "name".center(17, " ")
                   + "address".center(17, " ") + "\n")

        indents = (15, 15, 0)
        self.write_data_to_file(file, data, indents)

    def store_department_parser(self, data, file):
        file.write("\n" + " Store_department ".center(75, "=") + "\n")
        file.write("department_id".center(17, " ")
                   + "name".center(17, " ")
                   + "store_id".center(17, " ") + "\n")

        indents = (15, 20, 0)
        self.write_data_to_file(file, data, indents)

    def order_product_parser(self, data, file):
        file.write("\n" + " Order_product ".center(75, "=") + "\n")
        file.write("order_id".center(17, " ")
                   + "product_id".center(17, " ") + "\n")

        indents = (15, 0)
        self.write_data_to_file(file, data, indents)

    @staticmethod
    def input_client() -> List[str]:
        return [input("Enter name: ")]

    @staticmethod
    def input_order() -> List[str]:
        return [
            input("Enter date: "),
            input("Enter category_id: "),
            input("Enter client_id: "),
            input("Enter store_id: "),
            input("Enter product_id: "),
        ]

    @staticmethod
    def input_product() -> List[str]:
        return [
            input("Enter product_name: "),
            input("Enter price: "),
            input("Enter category_id: "),
        ]

    @staticmethod
    def input_product_category() -> List[str]:
        return [
            input("Enter category_name: "),
            input("Enter department_id: "),
        ]

    @staticmethod
    def input_store() -> List[str]:
        return [
            input("Enter store_name: "),
            input("Enter address: "),
        ]

    @staticmethod
    def input_department() -> List[str]:
        return [
            input("Enter department_name: "),
            input("Enter store_id: ")
        ]

    def update_data(self, table_num):
        def _input_new_product_id():
            return [input("Enter product_id: ")]

        updated_data = {
            1: self.input_client,
            2: self.input_order,
            3: self.input_product,
            4: self.input_product_category,
            5: self.input_store,
            6: self.input_department,
            7: _input_new_product_id,
        }

        row_id = input("Enter ID: ")
        print("If you want to skip a column, then enter the character '-'")
        return [row_id, *(updated_data[table_num]())]

    @staticmethod
    def delete():
        id_range = input("Select id range (x y) or just id (x): ").split()
        return [int(i) for i in id_range]
