from model import *
from view import View


class Controller:
    def __init__(self):
        self.view_obj = View()

    def menu(self):
        table_num = 0
        while True:
            operation_num = self.view_obj.operations_menu()
            if operation_num == 7:
                break
            if operation_num != 2 and operation_num != 6:
                table_num = self.view_obj.tables_menu()

            if operation_num == 1:
                select_table(table_num)
            elif operation_num == 2:
                select_all_tables()
            elif operation_num == 3:
                insert_data_controller(table_num)
            elif operation_num == 4:
                data = self.view_obj.update_data(table_num)
                update_table_controller(table_num, data)
            elif operation_num == 5:
                id_range = self.view_obj.delete()
                delete_rows_controller(table_num, id_range)
            elif operation_num == 6:
                insert_random_data_packet()
