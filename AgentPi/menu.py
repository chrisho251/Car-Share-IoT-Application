import os
import time
from datetime import datetime
from client import Client
from bluetoothIOT import BluetoothIOT
from qr_auth import Qr_auth
# from echo_client import Client


class Menu:
    """Console menu class"""
    INVALID_INPUT = "Invalid input, please try again!"
    INVALID_USER = "Invalid user, please login again!"
    client = Client()
    blu = BluetoothIOT()
    qrauth = Qr_auth()
    current_time = time.strftime("%b %y %H:%M", time.localtime())
    unlock_time = None
    lock_time = None
    current_email = ""
    car_id = "1"
    car_brand = "toyota"
    car_color = "red"
    car_seat = "7"
    is_user = True
    is_return = False

    def main_menu(self):
        """Function to print main menu"""
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
        """Function to print customer selection menu"""
        intro = "Here are the options available for you to choose from:"
        option1 = "[1] UNLOCK THE CAR"
        option2 = "[2] RETURN THE CAR"
        option3 = "[3] BACK"
        print(intro, option1, option2, option3, sep='\n')

    def unlock_menu_cust(self):
        """Function to print customer unlock menu"""
        intro = "Here are the options available for you to choose from"
        option1 = "[1] UNLOCK BY CREDENTIALS"
        option2 = "[2] UNLOCK BY FACIAL RECOGNITION"
        option3 = "[3] BACK"
        print(intro, option1, option2, option3, sep='\n')

    def menu_eng(self):
        """Function to print engineer unlock menu"""
        intro = "Here are the options available for you to choose from"
        option1 = "[1] UNLOCK BY CREDENTIALS"
        option2 = "[2] UNLOCK BY QR CODE"
        option3 = "[3] UNLOCK WITH BLUETOOTH"
        option4 = "[4] BACK"
        print(intro, option1, option2, option3, option4,  sep='\n')

    def successful_unlock(self):
        """Function to print successful unlock message"""
        print("""
        ******************************
        * CAR SUCCESSFULLY UNLOCKED! *
        ******************************
        """)
        print("Hi {}, welcome to {}, id: {}\n".format(
            self.current_email, self.car_brand, self.car_id))

    def successful_unlock_eng(self):
        """Function to print successful unlock message for engineer"""
        choice = input("Do you want to start the repair now? [Y/N]: ")
        if choice.lower() == 'y':
            print("Repair in process..")
        else:
            self.successful_unlock_eng()

    def get_input(self):
        """Function to get input from user with prompt"""
        option = input("Enter the number of your choice: ")
        return option

    def handle_selection_main(self):
        """Function to handle selection from main menu"""
        choice = self.get_input()
        if choice == '1':
            self.display_cust()
        elif choice == '2':
            self.is_user = False
            self.display_eng()

    def handle_selection_cust(self):
        """Function to handle selection from customer selection menu"""
        choice = self.get_input()
        if choice == '1':
            self.display_cust_unlock()
        elif choice == '2':
            self.display_return_car()
        elif choice == '3':
            self.display_main()

    def handle_selection_cust_unlock(self):
        """Function to handle selection from customer unlock menu"""
        choice = self.get_input()
        if choice == '1':
            self.login_menu()
        # elif choice == '2':
        #     ...
        elif choice == '3':
            self.display_cust()

    def handle_selection_eng(self):
        """Function to handle selection from engineer selection menu"""
        choice = self.get_input()
        if choice == '1':
            self.login_menu()
        elif choice == '2':
            self.authenticate_qr()
        elif choice == '3':
            self.authenticate_bluetooth()
        elif choice == '4':
            self.is_user = True
            self.display_main()

    def display_main(self):
        """Function to display main menu"""
        self.clear_terminal()
        self.main_menu()
        self.handle_selection_main()

    def display_cust(self):
        """Function to display customer selection menu"""
        self.clear_terminal()
        self.menu_cust()
        self.handle_selection_cust()

    def display_cust_unlock(self):
        """Function to display customer unlock menu"""
        self.clear_terminal()
        self.unlock_menu_cust()
        self.handle_selection_cust_unlock()

    def display_eng(self):
        """Function to display engineer selection menu"""
        self.clear_terminal()
        self.menu_eng()
        self.handle_selection_eng()

    def display_successful_unlock_cust(self):
        """Function to display successful unlock menu"""
        self.clear_terminal()
        self.successful_unlock()
        self.display_exit()

    def display_successful_unlock_eng(self):
        """Function to display successful unlock menu for engineer"""
        self.clear_terminal()
        self.successful_unlock()
        self.successful_unlock_eng()
        self.display_exit()

    def display_return_car(self):
        """Function to display return car message"""
        self.is_return = True
        self.login_menu()

    def display_exit(self):
        """Function to display logout option"""
        choice1 = input("Enter Q/q to exit: ")
        if choice1.lower() == 'q':
            choice2 = input("Are you sure you want to logout [Y/N]: ")
            if choice2.lower() == 'y':
                self.lock_time = round(datetime.now().timestamp())
                print("""
                *********************************
                * THANK YOU FOR USING CARSHARE! *
                *********************************
                """)
                print("\nThe car has been used for: {}s".format(
                    self.lock_time-self.unlock_time))
                print("\nTHE CAR IS NOW LOCKED!")
                time.sleep(5)
                self.is_user = True
                self.current_email = ""
                self.display_main()
            else:
                self.display_exit()
        else:
            self.display_exit()

    def validate_email(self):
        """Function to display validate email"""
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
        """Function to authenticate user by email and password"""
        authentication = self.client.validate(email, password).decode("utf-8")
        if authentication == "valid":
            self.current_email = email
            self.unlock_time = round(datetime.now().timestamp())
            if self.is_user and not self.is_return:
                self.display_successful_unlock_cust()
            elif self.is_user and self.is_return:
                self.return_car()
            else:
                self.display_successful_unlock_eng()
        elif authentication == "invalid":
            print(self.INVALID_USER)
            time.sleep(3)
            self.display_main()

    def authenticate_bluetooth(self):
        """Function to authenticate user by mac address"""
        data = self.blu.main()
        if bool(data) == True:
            authentication = self.client.validate_mac(
                data["mac_address"], data["email"]).decode("utf-8")
            if authentication == "valid":
                self.current_email = data["email"]
                self.unlock_time = round(datetime.now().timestamp())
                self.display_successful_unlock_eng()
            elif authentication == "invalid":
                print(self.INVALID_USER)
                time.sleep(3)
                self.display_main()
        else:
            self.display_eng()

    def authenticate_qr(self):
        """Function to authenticate user by qr data"""
        email = self.qrauth.read_qr()
        authentication = self.client.validate_qr(email).decode("utf-8")
        if authentication == "valid":
            self.current_email = email
            self.unlock_time = round(datetime.now().timestamp())
            self.display_successful_unlock_eng()
        elif authentication == "invalid":
            print(self.INVALID_USER)
            time.sleep(3)
            self.display_main()

    def return_car(self):
        """Function to print return car message"""
        successful_return = self.client.return_car(self.car_id)
        if successful_return:
            print("""
                *********************************
                * THANK YOU FOR USING CARSHARE! *
                *********************************
                """)
            print("Car (id: {}, model: {}) is succesfully returned at {}".format(
                self.car_id, self.car_brand, self.current_time))
            print("Total time used: {}".format(self.lock_time-self.unlock_time))
            self.display_main()

    def login_menu(self):
        """Function to print login menu"""
        print("\nPlease enter your email and password")
        email = self.validate_email()
        password = self.validate_password()
        self.authenticate_user(email, password)

    def clear_terminal(self):
        """Function to clear terminal"""
        os.system('clear')

    def main(self):
        """Main function"""
        self.display_main()


if __name__ == "__main__":
    menu = Menu()
    menu.main()
