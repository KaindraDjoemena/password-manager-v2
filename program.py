"""
Author: Kaindra Djoemena
Github: https://github.com/KaindraDjoemena

"""


from database_parent import Database
import json
import os
import random
from random import choices
import time
from time import sleep
import hashlib
from crypto import Crypto
from database import Master_database
from database import Accounts_database
from prettytable import PrettyTable as pt


class Program:
    
    def __init__(self):

        # Databases
        self.accounts_database = Accounts_database("accounts_database", "accounts_table")
        self.master_database = Master_database("master_database", "master_table")

        self.crypto = Crypto(15)
        with open(".key.json") as json_file:
            self.enc_key = json.load(json_file)

        with open("config.json") as json_file:
            self.config_file = json.load(json_file)

        # User signs up if havent, otherwise login
        self.have_signed_up = self.config_file["config"]["have_signed_up"]
        if not self.have_signed_up:
            self.signUpPage()

        if self.have_signed_up:
            self.loginPage()


    # Notifies the user
    def notifyUser(self, notification):
        print(f" {notification}")


    # Handles all basic input
    def handleBasicInput(self, user_input):
        if self.validInput(user_input):
            if user_input == "clear":
                os.system("cls")
            elif user_input == "exit":
                quit()
            else:
                self.notifyUser("unknown command")


    # A valid user input cant have a space and have to be a string
    def validInput(self, user_input):
        if type(user_input) == str:
            if " " not in user_input:
                return True
        return False


    # Delete all saved data
    def deleteData(self):
        print("reseting data...")

        # Open json file
        with open("config.json") as json_file:
            config_file = json.load(json_file)
        
        # Reset all json data
        for key, value in config_file["config"].items():
            if type(config_file["config"][key]) == bool:
                config_file["config"][key] = False
            else:
                config_file["config"][key] = None

        with open("config.json", "w") as json_file:
            json.dump(config_file, json_file, indent=2)

        print("removing files...")
        os.remove(".key.json")

        # Remove database
        # Delete tables
        print("removing database...")

        self.accounts_database.deleteTable()
        self.master_database.deleteTable()

        del self.accounts_database
        del self.master_database

        os.remove("accounts_database.db")
        os.remove("master_database.db")

        quit()


    """
    SIGN UP PAGE

    """



    # Sign up page
    def signUpPage(self):
        run = True
        while run:
            print("\n<<make account>>")

            username_input = input(">>username\t\t: ").strip()
            while not self.validInput(username_input):
                self.notifyUser("  invalid input")
                username_input = input(">>username\t\t: ").strip()
                if self.validInput(username_input):
                    break

            master_password_input = input(">>master password\t: ").strip()
            while not self.validInput(master_password_input):
                self.notifyUser("  invalid input")
                master_password_input = input(">>master password\t: ").strip()
                if self.validInput(master_password_input):
                    break

            email_input = input(">>email\t\t\t: ").strip()
            while not self.validInput(email_input):
                self.notifyUser("  invalid input")
                email_input = input(">>email\t\t\t: ").strip()
                if self.validInput(email_input):
                    break
            
            while True:
                user_confirmation = input("\ncontinue?(Y/N): ")
                if user_confirmation.strip().lower() == "y":

                    salt = ""
                    i = 0
                    while i < random.randint(5, 16):
                        salt += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-_=+[]|;:,<.>/?")
                        i += 1

                    # Storing the salt
                    with open("config.json") as json_file:
                        config_file = json.load(json_file)

                    config_file["config"]["salt"] = salt

                    with open("config.json", "w") as json_file:
                        json.dump(config_file, json_file, indent=2)

                    # Hashed master password + salt
                    hashed_master_password_salt = hashlib.sha256((master_password_input + salt).encode()).hexdigest()

                    # Insert data
                    try:
                        self.master_database.insertToDatabase(
                            self.crypto.encrypt(username_input, self.enc_key),
                            self.crypto.encrypt(salt, self.enc_key),
                            self.crypto.encrypt(hashed_master_password_salt, self.enc_key),
                            self.crypto.encrypt(email_input, self.enc_key)
                        )

                        with open("config.json") as json_file:
                            config_file = json.load(json_file)

                        config_file["config"]["have_signed_up"] = True

                        with open("config.json", "w") as json_file:
                            json.dump(config_file, json_file, indent=2)

                    except:
                        self.notifyUser("invalid input")

                    quit()

                elif user_confirmation.strip().lower() == "n":
                    quit()


    """
    LOGIN PAGE
    
    """



    # Login page
    def loginPage(self):
        run = True
        while run:
            user_input = input("master password: ").strip()

            self.master_database.selectFromDatabase(self.master_database.table_name, "*")
            items = self.master_database.cursor.fetchall()

            # Get salt
            with open("config.json") as json_file:
                config_file = json.load(json_file)

            salt = config_file["config"]["salt"]

            salted_user_input = user_input + salt

            # Getting the input password and the master password
            hashed_salted_user_input = hashlib.sha256(salted_user_input.encode()).hexdigest()
            hashed_master_password = self.crypto.decrypt(items[0][2], self.enc_key)

            # User gets access if the hashes match
            if hashed_master_password == hashed_salted_user_input:
                os.system("cls")
                self.mainPage()

            else:
                quit()



    """
    MAIN PAGE

    """ 



    # Main page of the program
    def mainPage(self):
        print("['help'] for help")

        run = True
        while run:
            print("\n<main>")
            user_input = input(">>").strip()
            if user_input == "help":
                self.helpPanel()
            elif self.validInput(user_input):
                self.handleBasicInput(user_input)
            else:
                if user_input == "p display":
                    self.displayPage()
                    print()
                elif user_input == "p add":
                    self.addPage()
                elif user_input == "p delete":
                    self.deletePage()
                elif user_input == "p search":
                    self.searchPage()
                elif user_input == "p settings":
                    self.settingsPage()
                else:
                    self.notifyUser("invalid input")



    """
    HELP PANEL
    
    """


    # Lists the commands
    def helpPanel(self):
        print("\n  <help>")
        print("  +------------------------------+")
        print("  | 'clear'      > clears window |")
        print("  | 'exit'       > exit program  |")
        print("  | 'p display'  > display page  |")
        print("  | 'p add'      > add page      |")
        print("  | 'p delete'   > delete page   |")
        print("  | 'p search'   > search page   |")
        print("  | 'p settings' > settings      |")
        print("  +------------------------------+")


    """
    ADD PAGE

    """


    # Adds accounts data to the database
    def addPage(self):
        print("\n  <add>")

        # Asks for user input
        username_input = input("  username\t: ").strip()
        while not self.validInput(username_input):
            self.notifyUser("  invalid input")
            username_input = input("  username\t: ").strip()
            if self.validInput(username_input):
                break

        email_input = input("  email\t\t: ").strip()
        while not self.validInput(email_input):
            self.notifyUser("  invalid input")
            email_input = input("  email\t\t: ").strip()
            if self.validInput(email_input):
                break

        password_input = input("  password\t: ").strip()
        while not self.validInput(password_input):
            self.notifyUser("  invalid input")
            password_input = input("  password\t: ").strip()
            if self.validInput(password_input):
                break

        website_name_input = input("  website name\t: ").strip()
        while not self.validInput(website_name_input):
            self.notifyUser("  invalid input")
            website_name_input = input("  website name\t: ").strip()
            if self.validInput(website_name_input):
                break

        website_url_input = input("  website url\t: ").strip()
        while not self.validInput(website_url_input):
            self.notifyUser("  invalid input")
            website_url_input = input("  website url\t\t: ").strip()
            if self.validInput(website_url_input):
                break


        while True:

            # Adds the data to the database if the user proceeds to
            confirmation = input("\n  >>proceed?(Y/N): ")
            if self.validInput(confirmation):

                if confirmation.strip().lower() == "y":
                    try:
                        self.accounts_database.insertToDatabase(
                            self.crypto.encrypt(username_input, self.enc_key),
                            self.crypto.encrypt(website_name_input, self.enc_key),
                            self.crypto.encrypt(website_url_input, self.enc_key),
                            self.crypto.encrypt(password_input, self.enc_key),
                            self.crypto.encrypt(email_input, self.enc_key)
                            )
                        self.notifyUser("  successfully added to the database")

                    except:
                        self.notifyUser("  invalid input")

                    break

                elif confirmation.strip().lower() == "n":
                    self.notifyUser("  action cancelled")
                    break


    """
    DELETE PAGE

    """



    # Deletes data from the database
    def deletePage(self):
        print("\n  <delete>")

        # Asks for input to delete from the database
        website_name_input = input("  website name\t: ").strip()
        while not self.validInput(website_name_input):
            self.notifyUser("  invalid input")
            website_name_input = input("  website name\t: ").strip()
            if self.validInput(website_name_input):
                break

        username_input = input("  username\t: ").strip()
        while not self.validInput(username_input):
            self.notifyUser("  invalid input")
            username_input = input("  username\t: ").strip()
            if self.validInput(username_input):
                break


        # Delets the data to the database if the user proceeds to
        while True:
            confirmation = input("\n  >>proceed?(Y/N): ")

            if self.validInput(confirmation):

                if confirmation.strip().lower() == "y":
                    
                    self.accounts_database.selectFromDatabase(
                        self.accounts_database.table_name,
                        "*",
                        f"WHERE username = '{self.crypto.encrypt(username_input, self.enc_key)}' AND website_name = '{self.crypto.encrypt(website_name_input, self.enc_key)}'"
                        )

                    items = self.accounts_database.cursor.fetchall()

                    if len(items) == 0:
                        self.notifyUser("  cant find item")
                        break
                    else:
                        self.accounts_database.deleteFromDatabase(f"WHERE username = '{self.crypto.encrypt(username_input, self.enc_key)}' AND website_name = '{self.crypto.encrypt(website_name_input, self.enc_key)}'")
                        break

                elif confirmation.strip().lower() == "n":
                    self.notifyUser("  action cancelled")
                    break


    """
    DISPLAY PAGE

    """



    # Displays the data
    def displayPage(self):

        print("\n  <display>")

        self.accounts_database.displayData()


    """
    SEARCH PAGE
    
    """



    def searchPage(self):
        run = True
        while run:
            print("\n  <search>")
            user_input = input("  website name>>").strip()

            # Try fetching from the database
            try:
                self.accounts_database.cursor.execute(f"""SELECT * FROM {self.accounts_database.table_name} WHERE website_name={user_input}""")
                items = self.accounts_database.cursor.fetchall()
                print(f"found {len(items)} item(s)")
                
                if len(items) == 0:
                    self.notifyUser("  item unavailable")

                else:

                    # Formats data with a table
                    table = pt(["Username", "Website Name", "Website URL", "Password", "Email"])
                    for item in items:
                        table.add_row([self.crypto.decrypt(item[i], self.enc_key) for i in range(5)])

                    print(f"\n{self.accounts_database.table_name.upper()}") # Prints The Table name
                    print(table) # Prints the table
            
            except:
                self.notifyUser("  item unavailable")

            break


    """
    SETTINGS PAGE

    """



    def settingsPage(self):
        run = True
        print("\n  ['help'] for help")

        while run:
            print("\n  <settings>")
            user_input = input("  >>").strip()

            # Reset all data
            if user_input == "reset":
                self.notifyUser("\n  <THIS ACTION WILL DELETE ALL SAVED DATA>")
                while True:
                    user_confirmation = input("  proceed?(Y/N): ")
                    if user_confirmation.strip().lower() == "y":
                        os.system("cls")
                        self.deleteData()

                    elif user_confirmation.strip().lower() == "n":
                        self.notifyUser("")
                        break

                    else:
                        self.notifyUser("  invalid input")

            # Go back to main page 
            elif user_input == "back":
                break
            
            # Help page
            elif user_input == "help":
                print("\n    <help>")
                print("    +-----------------------------+")
                print("    | 'back'  > back to main page |")
                print("    | 'reset' > reset data        |")
                print("    +-----------------------------+")

            else:
                self.notifyUser("  invalid input")



if __name__ == "__main__":
    pass
