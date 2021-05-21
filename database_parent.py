import sqlite3


class Database:
    
    # Establish connection to the database
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
        self.connection = sqlite3.connect(f"{database_name}.db")
        self.cursor = self.connection.cursor()


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
    def selectFromDatabase(self, database, command=None):

        if command != None:
            self.cursor.execute(f"SELECT rowid, * FROM {database} {command}")
        else:
            self.cursor.execute(f"SELECT rowid, * FROM {database}")

        self.commitDatabase()
    

    # Delete from database table
    def deleteFromDatabase(self, table_name, command):

        self.cursor.execute(f"""DELETE from {table_name} {command}""")

        self.commitDatabase()

        self.notifyUser(f"deleted element from database with: '{command}'")


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
