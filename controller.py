from model import Model
from view import View


class Controller:
    def __init__(self):
        self.view_obj = View()
        self.model_obj = Model()

    def menu(self):
        table_num = 0
        while True:
            operation_num = self.view_obj.operations_menu()
            if operation_num == 8:
                break
            if operation_num != 2 and operation_num != 6:
                table_num = self.view_obj.tables_menu()

            if operation_num == 1:
                self.model_obj.select_table(table_num, "w")
            elif operation_num == 2:
                self.model_obj.select_all_tables()
            elif operation_num == 3:
                self.model_obj.insert_data_controller(table_num)
            elif operation_num == 4:
                data = self.view_obj.update_data(table_num)
                self.model_obj.update_table(table_num, data)
            elif operation_num == 5:
                id_num = self.view_obj.delete()
                self.model_obj.delete_data(table_num, id_num)
            elif operation_num == 6:
                self.model_obj.insert_random_data_packet()
            elif operation_num == 7:
                column_names = self.model_obj.get_column_names_to_view(table_num)
                search_param = self.view_obj.search(column_names)
                self.model_obj.search_into_table(table_num, search_param)
