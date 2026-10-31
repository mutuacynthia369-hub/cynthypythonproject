import json
import os
import hashlib
from datetime import datetime

class MpesaAccount:
    def __init__(self, name,phone,pin,balance=0):
       self.name = name
       self.phone = phone
       self.__pin = self.hash_pin(pin)
       self.__balance = balance
       self.transactions =[]

    @staticmethod
    def hash_pin(pin):
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def verify_pin(self,pin):
        return self.__pin ==self.hash_pin(pin)

    @property
    def balance(self):
        return self.__balance

    def record_transaction(self, transaction_type, amount, details):
        transaction ={
            "type": transaction_type,
            "amount":amount,
            "details": details,
            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        }

        self.transactions.append(transaction)


    def deposit(self,amount):
        if amount <= 0:
            print("Enter a valid amount.")
            return False
        self.__balance += amount

        self.record_transaction(
            "Deposit", amount, "Money deposited"
        )
        print(f"Successfully deposited Ksh{amount:,.2f}")
        return True


    def withdraw(self,amount):
        if amount <=0:
            print("Invalid withdrawal amount.")
            return False
        self.__balance -= amount
        self.record_transaction(
            "withdrawal", amount,"cash withdrawal"
        )
        print(f"Successfully withdrawn Ksh{amount:,.2f}")
        return True

    def send_money(self,receiver,amount):

        if amount<=0:
            print("Invalid amount.")
            return False
        
        if amount > self.__balance:
            print("Insufficient balance!")
            return False
        
        self.__balance -=amount
        receiver.__balance += amount

        self.record_transaction(
            "send money",
            amount,
            f"sent to{receiver.phone}"
        )

        print(f"Ksh {amount:2f} sent successfully!")
        return True
    
    def buy_airtime(self,amount):
        if amount <= 0:
            print("Invalid airtime amount.")
            return False
        if amount >self.__balance:
            print("Insufficient balance!")
            return False
        self.__balance -= amount
        self.record_transaction(
            "Airtime",
            amount,
            "Airtime purchase"
        )
        print("Airtime purchased successfully!")
        return True

    def change_pin(self, old_pin,new_pin):
        if not self.verify_pin(old_pin):
            print("Incorrect old pin.")
            return False
        if not new_pin.isdigit() or len(new_pin)!= 4:
            print(" New PIN must contain 4 digits.")
            return False
        if self.verify_pin(new_pin):
            print("Choose a different PIN.")
            return False
        self.__pin = self.hash_pin(new_pin)
        print("PIN changed successfully!")
        return True

    def  to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "pin": self.__pin,
            "balance": self.__balance,
            "transactions":self.transactions
        }
    @classmethod
    def from_dict(cls,data):
        account = cls(
            data["name"],
            data["phone"],
            "0000",
            data["balance"]
        )
        account.__pin = data["pin"]
        account.transactions = data["transactions"]

        return account

class MpesaSystem:
    def __init__(self):
        self.accounts ={}
        self.load_accounts() 

    def save_accounts(self):
        data ={}
        for phone,account in self.accounts.items():
            data[phone] = account.to_dict()
        with open("mpesa_data.json", "w") as file:
            json.dump(data,file, indent =4)

    def load_accounts(self):
        if os.path.exists("mpesa_data.json"):

            try:
                with open("mpesa_data.json","r") as file:
                    data  = json.load(file)

                for phone,details in data.items():
                    self.accounts[phone] = (
                            MpesaAccount.from_dict(details)
                    )
            except(json.JSONDecodeError,KeyError):
                print(" Could not load saved account data.")

    def register(self):
        print("\n ======CREATE M-PESA ACCOUNT =====")

        name = input("Enter your full name:").strip()
        phone = input("Enter phone number (07xxxxxxxx or 01xxxxxxxx):").strip()

        if not name:
            print("Name cannot be empty.")
            return
        if(
            len(phone) !=10
            or not phone.isdigit()
            or not phone.startswith(("07","01"))

        ):
            print("Enter a valid Kenyan phone number.")
            return
        if phone in self.accounts:
            print("Phone number already registered.")
            return
        pin = input("Create a 4-digit PIN:")

        if not pin.isdigit() or len(pin) !=4:
            print("PIN must contain exactly 4 digits.")
            return
        account = MpesaAccount(name,phone,pin)
        self.accounts[phone] = account
        self.save_accounts()

        print("\nAccount created successfully!")
        print("Welcome to M-PESA,", name)


        # LOGIN

    def login(self):

        print("\n===== M-PESA LOGIN =====")

        phone = input("Enter phone number: ")
        pin = input("Enter your PIN: ")

        account = self.accounts.get(phone)

        if account and account.verify_pin(pin):

            print(f"\nWelcome {account.name}!")
            self.account_menu(account)

        else:
            print("Invalid phone number or PIN.")

    # ACCOUNT MENU

    def account_menu(self, account):

        while True:

            print("\n========== M-PESA MENU ==========")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Send Money")
            print("5. Buy Airtime")
            print("6. Transaction History")
            print("7. Change PIN")
            print("8. Logout")

            choice = input("Select an option: ")

            if choice == "1":

                print(
                    f"Your balance is Ksh {account.balance:,.2f}"
                )

            elif choice == "2":

                amount = self.get_amount("Enter deposit amount: ")

                if amount is not None:
                    if account.deposit(amount):
                        self.save_accounts()

            elif choice == "3":

                amount = self.get_amount("Enter withdrawal amount: ")

                if amount is not None:
                    if account.withdraw(amount):
                        self.save_accounts()

            elif choice == "4":

                self.transfer_money(account)

            elif choice == "5":

                amount = self.get_amount("Enter airtime amount: ")

                if amount is not None:
                    if account.buy_airtime(amount):
                        self.save_accounts()

            elif choice == "6":

                self.transaction_history(account)

            elif choice == "7":

                old_pin = input("Enter old PIN: ")
                new_pin = input("Enter new PIN: ")

                if account.change_pin(old_pin, new_pin):
                    self.save_accounts()

            elif choice == "8":

                print("You have logged out successfully.")
                break

            else:
                print("Invalid option. Try again.")

    # GET VALID AMOUNT

    @staticmethod
    def get_amount(message):

        try:
            amount = float(input(message))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return None

            return amount

        except ValueError:
            print("Please enter a valid number.")
            return None

    # TRANSFER MONEY

    def transfer_money(self, sender):

        receiver_phone = input(
            "Enter receiver's phone number: "
        )

        receiver = self.accounts.get(receiver_phone)

        if receiver is None:
            print("Receiver is not registered.")
            return

        if receiver_phone == sender.phone:
            print("You cannot send money to yourself.")
            return

        amount = self.get_amount("Enter amount to send: ")

        if amount is None:
            return

        pin = input("Confirm your PIN: ")

        if not sender.verify_pin(pin):
            print("Incorrect PIN. Transaction cancelled.")
            return

        if sender.send_money(receiver, amount):
            self.save_accounts()

    # TRANSACTION HISTORY

    @staticmethod
    def transaction_history(account):

        print("\n===== TRANSACTION HISTORY =====")

        if not account.transactions:
            print("No transactions found.")
            return

        for transaction in account.transactions:

            print("\n---------------------------")
            print("Type:", transaction["type"])
            print(
                "Amount: Ksh",
                f"{transaction['amount']:,.2f}"
            )
            print("Details:", transaction["details"])
            print("Date:", transaction["date"])


# ==========================================
# 3. MAIN FUNCTION
# ==========================================

def main():

    mpesa = MpesaSystem()

    while True:

        print("\n********************************")
        print("       WELCOME TO M-PESA")
        print("********************************")

        print("1. Register Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            mpesa.register()

        elif choice == "2":

            mpesa.login()

        elif choice == "3":

            print("Thank you for using M-PESA!")
            break

        else:

            print("Invalid choice. Try again.")


# ==========================================
# 4. START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()



    
