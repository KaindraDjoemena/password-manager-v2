import os
import json
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
    
        self.crypto = Crypto()
        with open(".key.json") as json_file:
            self.enc_key = json.load(json_file)


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
    MAIN PAGE

    """ 


    # Main page of the program
    def mainPage(self):

        run = True
        while run:
            user_input = input("\nm>>")
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

        print("  <add>")

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
                    self.accounts_database.insertToDatabase(
                        self.crypto.encrypt(username_input, self.enc_key),
                        self.crypto.encrypt(website_name_input, self.enc_key),
                        self.crypto.encrypt(website_url_input, self.enc_key),
                        self.crypto.encrypt(password_input, self.enc_key),
                        self.crypto.encrypt(email_input, self.enc_key)
                        )
                    self.notifyUser("  successfully added to the database")
                    break

                elif confirmation.lower() == "n":
                    self.notifyUser("  action cancelled")
                    break


    """
    DELETE PAGE

    """



    # Deletes data from the database
    def deletePage(self):
        
        print("  <delete>")

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

        # Adds the data to the database if the user proceeds to
        while True:
            confirmation = input("\n  >>proceed?(Y/N): ")

            if self.validInput(confirmation):

                if confirmation.lower() == "y":

                    self.accounts_database.cursor.execute(f"SELECT * from {self.accounts_database.table_name}")
                    
                    database_item = self.accounts_database.cursor.fetchall()
                    
                    traversal_count = 0
                    for item in database_item:
                        if (item[0] == self.crypto.encrypt(username_input, self.enc_key)) and (item[1] == self.crypto.encrypt(website_name_input, self.enc_key)):
                            self.accounts_database.deleteFromDatabase(f"WHERE username='{self.crypto.encrypt(username_input, self.enc_key)}' AND website_name='{self.crypto.encrypt(website_name_input, self.enc_key)}'")
                            self.notifyUser("  successfully deleted from the database")
                            traversal_count += 1
                    if traversal_count == len(database_item):
                        self.notifyUser("  cant find item")
                    

                elif confirmation.lower() == "n":
                    self.notifyUser("  action cancelled")
                break


    """
    DISPLAY PAGE

    """



    # Displays the data
    def displayPage(self):

        print("  <display>")

        self.accounts_database.displayData()



if __name__ == "__main__":
    pass
