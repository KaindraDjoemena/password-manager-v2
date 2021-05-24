import json
from prettytable import PrettyTable as pt
from database_parent import Database



"""
Child classes of the parent Database

"""

class Accounts_database(Database):
    def __init__(self, database_name, table_name):
        super().__init__(database_name, table_name)

        with open(".key.json") as json_file:
            self.enc_key = json.load(json_file)

        # Makes a table if havent by looking up the config.json file
        with open("config.json", "r") as json_file:
            config_file = json.load(json_file)
        self.have_created_table = config_file["config"]["have_created_accounts_table"]
        if not self.have_created_table:
            self.makeTable()


    # Make Table
    def makeTable(self):

        # Creates the Tables
        self.cursor.execute(f"""CREATE TABLE {self.table_name} (
            username text,
            website_name text,
            website_url test,
            password text,
            email text
        )""")

        self.commitDatabase()

        # Changes the config file to have made the accounts table
        with open("config.json") as json_file:
            config_file = json.load(json_file)

        config_file["config"]["have_created_accounts_table"] = True

        with open("config.json", "w") as json_file:
            json.dump(config_file, json_file, indent=2)

        self.notifyUser(f"made {self.table_name} table")


    # Insert data to table
    def insertToDatabase(self, username, website_name, website_url, password, email):
        
        self.cursor.execute(f"""INSERT INTO {self.table_name} VALUES (:username, :website_name, :website_url, :password, :email)""", {
            "username"    : username,
            "website_name": website_name,
            "website_url" : website_url,
            "password"    : password,
            "email"       : email
        })

        self.commitDatabase()

        self.notifyUser(f"inserted data to {self.table_name} table")


    # Delete from database table
    def deleteFromDatabase(self, command):

        self.cursor.execute(f"""DELETE from {self.table_name} {command}""")

        self.commitDatabase()

        self.notifyUser(f"deleted element from database with: '{command}'")


    # Displays data
    def displayData(self, database_selection="*"):
        self.selectFromDatabase(self.table_name, database_selection)
        items = self.cursor.fetchall()
        range_val = 5 if database_selection == "*" else 6

        # Formats data with a table
        if database_selection == "*":
            table = pt(["Username", "Website Name", "Website URL", "Password", "Email"])
        else:
            table = pt(["ID", "Username", "Website Name", "Website URL", "Password", "Email"])
        for item in items:
            table.add_row([self.crypto.decrypt(item[i], self.enc_key) for i in range(range_val)])

        print(f"\n{self.table_name.upper()}: {len(items)}") # Prints The Table name
        print(table) # Prints the table



class Master_database(Database):
    def __init__(self, database_name, table_name):
        super().__init__(database_name, table_name)

        with open(".key.json") as json_file:
            self.enc_key = json.load(json_file)

        # Makes a table if havent by looking up the config.json file
        with open("config.json", "r") as json_file:
            config_file = json.load(json_file)
        self.have_created_table = config_file["config"]["have_created_master_table"]
        if not self.have_created_table:
            self.makeTable()


    # Make table
    def makeTable(self):
        
        self.cursor.execute(f"""CREATE TABLE {self.table_name} (
            username text,
            salt text,
            master_password_hash text,
            email text
        )""")

        self.commitDatabase()

        # Changes the config file to have made the accounts table
        with open("config.json") as json_file:
            config_file = json.load(json_file)
        
        config_file["config"]["have_created_master_table"] = True

        with open("config.json", "w") as json_file:
            json.dump(config_file, json_file, indent=2)

        self.notifyUser(f"made {self.table_name} table")


    # Insert data to table
    def insertToDatabase(self, username, salt, master_password_hash, email):
        
        self.cursor.execute(f"""INSERT INTO {self.table_name} VALUES (:username, :salt, :master_password_hash, :email)""", {
            "username"            : username,
            "salt"                : salt,
            "master_password_hash": master_password_hash,
            "email"               : email
        })

        self.notifyUser(f"inserted data to {self.table_name} table")

        self.commitDatabase()


    # Displays data
    def displayData(self, database_selection):
        self.selectFromDatabase(self.table_name, database_selection)
        items = self.cursor.fetchall()
        range_val = 4 if database_selection == "*" else 5


        # Formats data with a table
        if database_selection == "*":
            table = pt(["Username", "Password Salt", "Master Password Hash", "Email"])
        else:
            table = pt(["ID", "Username", "Password Salt", "Master Password Hash", "Email"])
        for item in items:
            table.add_row([self.crypto.decrypt(item[i], self.enc_key) for i in range(range_val)])

        print(f"\n{self.table_name.upper()}: {len(items)}") # Prints The Table name
        print(table) # Prints the table



if __name__ == "__main__":
    pass
