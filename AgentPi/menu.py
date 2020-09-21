import os
import time
from datetime import datetime
from client import Client
# from echo_client import Client

class Menu:
    INVALID_INPUT = "Invalid input, please try again!"
    client = Client()
    current_time = time.strftime("%b %y %H:%M", time.localtime())
    unlock_time = None
    lock_time = None
    current_email = ""
    car_id = "1"
    car_brand = "toyota"
    is_user = True

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
        option3 = "[3] BACK"
        print(intro, option1, option2, option3, sep='\n')

    def unlock_menu_cust(self):
        intro = "Here are the options available for you to choose from"
        option1 = "[1] UNLOCK BY CREDENTIALS"
        option2 = "[2] UNLOCK BY FACIAL RECOGNITION"
        option3 = "[3] BACK"
        print(intro, option1, option2, option3, sep='\n')

    def menu_eng(self):
        intro = "Here are the options available for you to choose from"
        option1 = "[1] UNLOCK BY CREDENTIALS"
        option2 = "[2] UNLOCK BY QR CODE"
        option3 = "[3] UNLOCK WITH BLUETOOTH"
        option4 = "[4] BACK"
        print(intro, option1, option2, option3, option4,  sep='\n')

    def successful_unlock(self):
        print("""
        ******************************
        * CAR SUCCESSFULLY UNLOCKED! *
        ******************************
        """)
        print("Hi {}, welcome to {}, id: {}\n".format(self.current_email, self.car_brand, self.car_id))

    def successful_unlock_eng(self):
        choice = input("Do you want to start the repair now? [Y/N]: ")
        if choice.lower() == 'y':
            print("Repair in process..")
        else:
            self.successful_unlock_eng()
            

    def get_input(self):
        option = input("Enter the number of your choice: ")
        return option

    def handle_selection_main(self):
        choice = self.get_input()
        if choice == '1':
            self.display_cust()
        elif choice == '2':
            self.is_user = False
            self.display_eng()

    def handle_selection_cust(self):
        choice = self.get_input()
        if choice == '1':
            self.display_cust_unlock()
        # elif choice == '2':
        #     ...
        elif choice == '3':
            self.display_main()

    def handle_selection_cust_unlock(self):
        choice = self.get_input()
        if choice == '1':
            self.login_menu()
        # elif choice == '2':
        #     ...
        elif choice == '3':
            self.display_cust()

    def handle_selection_eng(self):
        choice = self.get_input()
        if choice == '1':
            self.login_menu()
        # elif choice == '2':
        #     ...
        # elif choice == '3':
        #     ...
        elif choice == '4':
            self.is_user = True
            self.display_main()

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

    def display_successful_unlock_cust(self):
        self.clear_terminal()
        self.successful_unlock()
        self.display_exit()
    
    def display_successful_unlock_eng(self):
        self.clear_terminal()
        self.successful_unlock()
        self.successful_unlock_eng()
        self.display_exit()

    def display_exit(self):
        choice1 = input("Enter Q/q to exit: ")
        if choice1.lower() == 'q':
            choice2 = input("Are you sure you want to logout [Y/N]: ")
            if choice2.lower() == 'y':
                self.lock_time = datetime.now().timestamp()
                print("The car has been used for: {}s".format(self.unlock_time-self.lock_time))
                print("""
                *********************************
                * THANK YOU FOR USING CARSHARE! *
                *********************************
                """)
                time.sleep(5)
                self.is_user = True
                self.display_main()
            else:
                self.display_exit()
        else:
            self.display_exit()
            



    def validate_email(self):
        email = input("Email: ").strip()
        if email is None or email == "":
            print(self.INVALID_INPUT)
            self.display_cust_unlock()
        else:
            return email
    
    def validate_password(self):
        password = input("Password: ").strip()
        if password is None or password == "":
            print(self.INVALID_INPUT)
            self.display_cust_unlock()
        else:
            return password

    def authenticate_user(self, email, password):
        authentication = self.client.validate(email, password)
        if authentication == "valid":
            self.current_email = email
            self.unlock_time = datetime.now().timestamp()
            if self.is_user:
                self.display_successful_unlock_cust()
            else:
                self.display_successful_unlock_eng()
        elif authentication == "invalid":
            print("Invalid user, please login again!")
            self.display_main()

    def login_menu(self):
        print("\nPlease enter your email and password")
        email = self.validate_email()
        password = self.validate_password()
        self.authenticate_user(email, password)

    def clear_terminal(self):
        os.system('cls')

    def main(self):
        self.display_main()

if __name__ == "__main__":
    menu = Menu()
    menu.main()
