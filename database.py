import sqlite3
from prettytable import PrettyTable as pt


class Database:
    
    # Establish connection to the database
    def __init__(self):
        self.connection = sqlite3.connect("data.db")
        self.cursor = self.connection.cursor()


    # Initialize database
    def initializeDatabase(self):

        # Creates the Tables
        self.cursor.execute("""CREATE TABLE accounts (
            username text,
            website_name text,
            website_url test,
            password text,
            email text
        )""")

        self.cursor.execute("""CREATE TABLE user_data (
            username text,
            master_password text,
            email text
        )""")

        self.commitDatabase()


    # Inserts to the accounts table
    def insertToDatabaseAccounts(self, username, website_name, website_url, password, email):
        
        self.cursor.execute("""INSERT INTO accounts VALUES (:username, :website_name, :website_url, :password, :email)""", {
            "username"    : username,
            "website_name": website_name,
            "website_url" : website_url,
            "password"    : password,
            "email"       : email
        })

        self.notifyUser("inserted data to acccounts table")

        self.commitDatabase()
    

    # Inserts to the user_data table
    def insertToDatabaseUserData(self, username, master_password, email):

        self.cursor.execute("""INSERT INTO user_data VALUES (:username, :master_password, :email)""", {
            "username"       : username,
            "master_password": master_password,
            "email"          : email
        })

        self.notifyUser("inserted data to user_data table")

        self.commitDatabase()


    # Selects from database tables
    def selectFromDatabase(self, database, selection="*", command=None):

        if command != None:
            self.cursor.execute(f"SELECT {selection} FROM {database} {command}")
        else:
            self.cursor.execute(f"SELECT {selection} FROM {database}")

        self.commitDatabase()
    

    # Displays data
    def displayData(self, table_name="accounts"):
        self.selectFromDatabase(table_name, "rowid, *")
        items = self.cursor.fetchall()

        # Makes a table
        table = pt(["ID", "Username", "Website Name", "Website URL", "Password", "Email"])
        for item in items:
            table.add_row([item[i] for i in range(6)])

        print(f"\n{table_name.upper()}") # Prints The Table name
        print(table) # Prints the table


    # Commit connection
    def commitDatabase(self):
        self.connection.commit()


    # Close connection
    def closeDatabase(self):
        self.connection.close()


    # Notifies the user
    def notifyUser(self, notification):
        print(f"<{notification}>")