import os
from prettytable import PrettyTable as pt
from database import Accounts_database
from database import Master_database


class Program:

    def __init__(self):

        # Databases
        self.accounts_database = Accounts_database("accounts_database", "accounts_table")
        self.master_database = Master_database("master_database", "master_table")
    
    
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
                        username_input,
                        website_name_input,
                        website_name_input,
                        password_input,
                        email_input
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
                    self.accounts_database.deleteFromDatabase(f"WHERE website_name={website_name_input} AND username={username_input}")
                    self.notifyUser("  successfully deleted to the database")
                    break

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
    


    """
    SEARCH PAGE
    
    """



    def searchPage(self):
        run = True
        while run:
            print("  <search>")
            user_input = input("  s>>")

            # Gets the command from the user
            if user_input == "":
                self.accounts_database.selectFromDatabase(self.accounts_database.table_name)
            else:
                try:
                    self.accounts_database.selectFromDatabase(self.accounts_database.table_name, user_input)
                except:
                    self.notifyUser("  invalid command")

            items = self.accounts_database.cursor.fetchall()
            if len(items) == 0:
                self.notifyUser("  item unavailable")

            else:

                # Formats data with a table
                table = pt(["ID", "Username", "Website Name", "Website URL", "Password", "Email"])
                for item in items:
                    table.add_row([item[i] for i in range(6)])

                print(f"\n{self.accounts_database.table_name.upper()}") # Prints The Table name
                print(table) # Prints the table

            break
