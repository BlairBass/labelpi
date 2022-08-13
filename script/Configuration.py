import os
import configparser


class Configuration:
    def __init__(self):
        self.sql_server = ""
        self.sql_port = 0
        self.sql_user = ""
        self.sql_password = ""
        self.sql_database = ""
        self.sql_named_instance = False
        self.sql_named_instance_name = ""

        self.style_active_style = ""

        self.printer_name = ""
        self.printer_page_width = 0.0
        self.printer_page_height = 0.0

    def read_config_from_file(self, filename):
        # Reads the configuration from an ini file
        if os.path.exists(filename):
            config = configparser.RawConfigParser()
            config.read(filename)

            db_config = config["mssql"]
            self.sql_server = db_config["server"]
            self.sql_port = db_config["port"]
            self.sql_user = db_config["port"]
            self.sql_password = db_config["password"]
            self.sql_database = db_config["database"]
            self.sql_named_instance = db_config.getboolean("named_instance")
            self.sql_named_instance_name = db_config["named_instance_name"]

            style_config = config["style"]
            self.style_active_style = style_config["active_style"]

            printer_config = config["printer"]
            self.printer_name = printer_config.get("printer_name")
            self.printer_page_height = printer_config.getfloat("page_height")
            self.printer_page_width = printer_config.getfloat("page_width")
