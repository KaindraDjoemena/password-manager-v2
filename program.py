import json
import os
import json
import random
from random import choices
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
        self.have_signed_up = self.config_file["config"]["have_signed_up"]

        # User signs up if havent, otherwise login
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


    """
    SIGN UP PAGE

    """



    # Sign up page
    def signUpPage(self):
        run = True
        while run:
            print("\n<make account>")

            username_input = input(">>username: ")
            while not self.validInput(username_input):
                self.notifyUser("  invalid input")
                username_input = input(">>username: ")
                if self.validInput(username_input):
                    break

            master_password_input = input(">>master password: ")
            while not self.validInput(master_password_input):
                self.notifyUser("  invalid input")
                master_password_input = input(">>master password: ")
                if self.validInput(master_password_input):
                    break

            email_input = input(">>email: ")
            while not self.validInput(email_input):
                self.notifyUser("  invalid input")
                email_input = input(">>email: ")
                if self.validInput(email_input):
                    break
            
            while True:
                user_confirmation = input("\ncontinue?(Y/N): ")
                if user_confirmation.lower() == "y":

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

                elif user_confirmation.lower() == "n":
                    quit()


    """
    LOGIN PAGE
    
    """



    # Login page
    def loginPage(self):
        run = True
        while run:
            user_input = input("master password: ")

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

        run = True
        while run:
            print("\n<main>")
            user_input = input(">>")
            if self.validInput(user_input):
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
                else:
                    self.notifyUser("invalid input")



    """
    ADD PAGE

    """


    # Adds accounts data to the database
    def addPage(self):
        print("  \n<add>")

        # Asks for user input
        username_input = input("  username: ")
        while not self.validInput(username_input):
            self.notifyUser("  invalid input")
            username_input = input("  username: ")
            if self.validInput(username_input):
                break

        email_input = input("  email: ")
        while not self.validInput(email_input):
            self.notifyUser("  invalid input")
            email_input = input("  email: ")
            if self.validInput(email_input):
                break

        password_input = input("  password: ")
        while not self.validInput(password_input):
            self.notifyUser("  invalid input")
            password_input = input("  password: ")
            if self.validInput(password_input):
                break

        website_name_input = input("  website name: ")
        while not self.validInput(website_name_input):
            self.notifyUser("  invalid input")
            website_name_input = input("  website name: ")
            if self.validInput(website_name_input):
                break

        website_url_input = input("  website url: ")
        while not self.validInput(website_url_input):
            self.notifyUser("  invalid input")
            website_url_input = input("  website url: ")
            if self.validInput(website_url_input):
                break


        while True:

            # Adds the data to the database if the user proceeds to
            confirmation = input("\n  >>proceed?(Y/N): ")
            if self.validInput(confirmation):

                if confirmation.lower() == "y":
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

                elif confirmation.lower() == "n":
                    self.notifyUser("  action cancelled")
                    break


    """
    DELETE PAGE

    """



    # Deletes data from the database
    def deletePage(self):
        print("  \n<delete>")

        # Asks for input to delete from the database
        website_name_input = input("  website name: ")
        while not self.validInput(website_name_input):
            self.notifyUser("  invalid input")
            website_name_input = input("  website name: ")
            if self.validInput(website_name_input):
                break

        username_input = input("  username: ")
        while not self.validInput(username_input):
            self.notifyUser("  invalid input")
            username_input = input("  username: ")
            if self.validInput(username_input):
                break


        # Delets the data to the database if the user proceeds to
        while True:
            confirmation = input("\n  >>proceed?(Y/N): ")

            if self.validInput(confirmation):

                if confirmation.lower() == "y":
                    
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

                elif confirmation.lower() == "n":
                    self.notifyUser("  action cancelled")
                    break


    """
    DISPLAY PAGE

    """



    # Displays the data
    def displayPage(self):

        print("  \n<display>")

        self.accounts_database.displayData()


    """
    SEARCH PAGE
    
    """



    def searchPage(self):
        run = True
        while run:
            print("  \n<search>")
            user_input = input("  >>")

            # Gets the command from the user
            if user_input != "":

                try:
                    first_comma_i = user_input.index("'")
                    last_comma_i = len(user_input)-1

                    key_word = user_input[first_comma_i+1: last_comma_i]

                    encrypted_key_word = self.crypto.encrypt(key_word, self.enc_key)

                    new_command = user_input[:first_comma_i+1] + encrypted_key_word + user_input[last_comma_i:]

                except:
                    self.notifyUser("  invalid command")

                try:
                    self.accounts_database.selectFromDatabase(self.accounts_database.table_name, "*", new_command)
                except:
                    self.notifyUser("  invalid command")

            items = self.accounts_database.cursor.fetchall()
            if len(items) == 0:
                self.notifyUser("  item unavailable")

            else:

                # Formats data with a table
                table = pt(["Username", "Website Name", "Website URL", "Password", "Email"])
                for item in items:
                    table.add_row([self.crypto.decrypt(item[i], self.enc_key) for i in range(5)])

                print(f"\n{self.accounts_database.table_name.upper()}") # Prints The Table name
                print(table) # Prints the table

            break



if __name__ == "__main__":
    pass
