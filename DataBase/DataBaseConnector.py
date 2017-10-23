from mysql.connector import MySQLConnection, Error

class DataBaseCommunicator(object):
    def __init__(self,
                 host = 'localhost',
                 user = 'admin',
                 password = '123'):

        self.HOST = host
        self.DATA_BASE = None
        self.USER = user
        self.PASSWORD = password

        self.CONNECTOR = None
        self.CURSOR = None


    def open_connection_to_db(self, data_base):
        self.DATA_BASE = data_base
        if self.CONNECTOR is not None:
            self.CONNECTOR.close()

        try:
            self.CONNECTOR = MySQLConnection(
                host = self.HOST,
                database = self.DATA_BASE,
                user = self.USER,
                password = self.PASSWORD
            )

        except Error as error:
            print(error)


    def close_connection_to_db(self):
        if self.CONNECTOR is not None:
            if self.CONNECTOR.is_connected():

                try:
                    self.CONNECTOR.close()

                except Error as error:
                    print(error)
            else:
                print('Connection is already lost')
        else:
            print('Connector das not exists!')

    def check_if_table_exists(self, table_name):
        if self.CONNECTOR is not None:
            if self.CONNECTOR.is_connected:
                self.close_connection_to_db()

        self.open_connection_to_db(data_base='information_schema')

        if self.CONNECTOR is not None:

            if self.CONNECTOR.is_connected():
                try:
                    self.CURSOR = self.CONNECTOR.cursor()
                    self.CURSOR.execute("""
                        SELECT COUNT(*)
                        from  information_schema.TABLES
                        WHERE TABLE_NAME = '{0}'
                        """.format(table_name.replace('\'', '\'\'')))

                    if self.CURSOR.fetchone()[0] == 1:
                        state = True
                    else:
                        state = False

                    self.CURSOR.close()
                    self.close_connection_to_db()
                    return state

                except Error as error:
                  print(error)
            else:
                print('Connection lost')
        else:
            print('Connector das not exists!')

    def cursor_create(self):
        try:
            if self.CONNECTOR is not None:
                if self.CONNECTOR.is_connected():
                    self.CURSOR = self.CONNECTOR.cursor()
        except Error as error:
            print(error)

    def cursor_kill(self):
        try:
            if self.CONNECTOR is not None:
                if self.CONNECTOR.is_connected():
                    self.CURSOR.close()
        except Error as error:
            print(error)