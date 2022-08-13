import pymssql

from script.sqlbrowser import get_instance_info

import os
import sys

originalOut = sys.stdout

class Database:
    def __init__(self, configuration, connection_failure_callback=None):

        self.configuration = configuration
        self.connection = None
        self.connected = False
        self.connectionFailureCallback = connection_failure_callback

        self.connect()

        if self.connected:
            cursor = self.connection.cursor()
            cursor.execute("SELECT @@version;")
            row = cursor.fetchone()

    def connect(self):
        global originalOut
        try:
            if self.configuration.sql_named_instance:
                #serverport = get_instance_info(self.configuration.sql_server,
                #self.configuration.sql_named_instance_name)
                #serverport = serverport[0]['tcp']

                self.connection = pymssql.connect(
                    host=self.configuration.sql_server + "\\" + self.configuration.sql_named_instance_name,
                    user=self.configuration.sql_user,
                    password=self.configuration.sql_password,
                    database=self.configuration.sql_database, tds_version="8.0")
                self.connected = True
            else:

                self.connection = pymssql.connect(host=self.configuration.sql_server,
                                                  port=self.configuration.sql_port,
                                                  user=self.configuration.sql_user,
                                                  password=self.configuration.sql_password,
                                                  database=self.configuration.sql_database)
                self.connected = True
        except:
            #sys.stdout = open('/home/pi/out.log', 'w')
            #raise
            if self.connectionFailureCallback is not None:
                self.connected = False
                self.connectionFailureCallback()
        finally:
            sys.stdout = originalOut

    def query_number(self, number):
        if not self.connected:
            return True

        try:
            cursor = self.connection.cursor()
        except pymssql.Error as e:
            if pymssql.is_connection_broken_error(e):
                self.connect()
                cursor = self.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM tbLVKopf WHERE LVNr = '" + number + "' AND (ArbeitsbereichNum = 1 OR ArbeitsbereichNum = 3)")
        row = cursor.fetchone()
        return row[0] == 1
