"""
Author: Kaindra Djoemena
Github: https://github.com/KaindraDjoemena

"""


import json
import sqlite3
from crypto import Crypto


class Database:

    # Establish connection to the database
    def __init__(self, database_name, table_name):

        self.crypto = Crypto(15)

        with open("config.json") as json_file:
            config_file = json.load(json_file)
        self.have_created_key = config_file["config"]["have_created_key"]
        
        # Make key if havent
        if not self.have_created_key:
            self.key = self.crypto.makeKey() # encryption key

            with open(".key.json", "w") as json_file:
                json.dump(self.key, json_file, indent=2)

            with open("config.json", "w") as json_file:
                config_file["config"]["have_created_key"] = True
                json.dump(config_file, json_file, indent=2)

        self.database_name = database_name
        self.table_name = table_name
        self.connection = sqlite3.connect(f"{database_name}.db")
        self.cursor = self.connection.cursor()


    # Delete table
    def deleteTable(self):
        self.cursor.execute(f"""DROP TABLE {self.table_name}""")

        self.commitDatabase()
        self.notifyUser(f"Deleted {self.table_name}")


    # Make table
    def makeTable(self):
        pass


    # Inserts to the accounts table
    def insertToDatabaseAccounts(self):
        pass


    # Inserts to the user_data table
    def insertToDatabaseUserData(self):
        pass


    # Selects from database tables
    def selectFromDatabase(self, table, selection="rowid, *", command=None):

        self.cursor.execute(f"SELECT {selection} FROM {table}")

        if command != None:
            self.cursor.execute(f"SELECT {selection} FROM {table} {command}")

        self.commitDatabase()


    # Delete from database table
    def deleteFromDatabase(self, table_name, command):

        self.cursor.execute(f"""DELETE from {table_name} {command}""")

        self.commitDatabase()


    # Displays data
    def displayData(self):
        pass


    # Commit connection
    def commitDatabase(self):
        self.connection.commit()


    # Close connection
    def closeDatabase(self):
        self.connection.close()


    # Notifies the user
    def notifyUser(self, notification):
        print(f"<{notification}>")
