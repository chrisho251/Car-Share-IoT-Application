import os
# from echo_client import Client

class Menu:
    # client = Client()
    INVALID_INPUT = "Invalid input, please try again!"

    def main_menu(self):
        welcome = """
        ************************
        * WELCOME TO CARSHARE! *
        ************************
        """
        intro = "Are you a USER or an ENGINEER?"
        option1 = "[1] USER"
        option2 = "[2] ENGINEER"
        print(welcome, intro, option1, option2, sep='\n')

    def menu_cust(self):
        intro = "Here are the options available for you to choose from:"
        option1 = "[1] UNLOCK THE CAR"
        option2 = "[2] RETURN THE CAR"
        print(intro, option1, option2, sep='\n')

    def unlock_menu_cust(self):
        intro = "Here are the options available for you to choose from"
        option1 = "[1] UNLOCK BY CREDENTIALS"
        option2 = "[2] UNLOCK BY FACIAL RECOGNITION"
        print(intro, option1, option2, sep='\n')

    def menu_eng(self):
        intro = "Here are the options available for you to choose from"
        option1 = "[1] UNLOCK BY CREDENTIALS"
        option2 = "[2] UNLOCK BY QR CODE"
        option3 = "[3] UNLOCK WITH BLUETOOTH"
        print(intro, option1, option2, option3, sep='\n')

    def creds_menu(self):
        print("\nPlease enter your username and password")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

    def get_input(self):
        option = input("Enter the number of your choice: ")
        return option

    def handle_selection_main(self):
        choice = self.get_input()
        if choice == '1':
            self.display_cust()
        elif choice == '2':
            self.display_eng()

    def handle_selection_cust(self):
        choice = self.get_input()
        if choice == '1':
            self.display_cust_unlock()
        # elif choice == '2':
        #     ...

    def handle_selection_cust_unlock(self):
        choice = self.get_input()
        if choice == '1':
            self.creds_menu()
        # elif choice == '2':
        #     ...

    def handle_selection_eng(self):
        choice = self.get_input()
        if choice == '1':
            self.creds_menu()
        # elif choice == '2':
        #     ...
        # elif choice == '3':
        #     ...

    def display_main(self):
        self.clear_terminal()
        self.main_menu()
        self.handle_selection_main()

    def display_cust(self):
        self.clear_terminal()
        self.menu_cust()
        self.handle_selection_cust()

    def display_cust_unlock(self):
        self.clear_terminal()
        self.unlock_menu_cust()
        self.handle_selection_cust_unlock()

    def display_eng(self):
        self.clear_terminal()
        self.menu_eng()
        self.handle_selection_eng()

    def validate_username(self):
        username = input("Username: ").strip()
        if username is None or username == "":
            print(self.INVALID_INPUT)
            self.display_cust_unlock()
        else:
            return username
    
    def validate_password(self):
        password = input("Password: ").strip()


    def clear_terminal(self):
        os.system('cls')

    def main(self):
        self.display_main()

if __name__ == "__main__":
    menu = Menu()
    menu.main()