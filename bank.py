import json
import hashlib
import os
from datetime import datetime
from abc import ABC , abstractmethod


class Account(ABC):
    def __init__(self , account_number,name, pin, balance=0):
        self.account_number=account_number
        self.name=name
        self.__pin=self.hash_pin(pin)
        self.__balance = balance
        self.transactions=[]

    @staticmethod
    def hash_pin(pin):
       return hashlib.sha256(pin.encode()).hexdigest()
    def verify_pin(self,pin):
        return self.__pin == self.hash_pin(pin)
    @property
    def balance(self):
        return self.__balance
    @abstractmethod
    def account_type(self):
        pass
    def deposit(self, amount):
       if amount <= 0:
           print("Amount must be greater than zero.")
           return False
       self.__balance += amount
       self.add_transaction("Deposit", amount)
       print(f"Successfully deposited Ksh{amount}")
       return True
    def withdraw(self, amount):
        if amount <=0:
          print("Invalid wwithdrawal  amount.")
          return False
        if amount >self.__balance:
         print("insufficient funds.")
         return False
        self.__balance -= amount
        self.add_transaction("withdrawal",amount)
        print(f"Successfully withdrawn Ksh{amount}")
        return True
    def add_transaction(self,transaction_type,amount):
        transaction =  {
          "type": transaction_type,
           "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
        self.transactions.append(transaction)


class SavingsAccount(Account):
    def account_type(self):
        return "Savings Account"

class CurrentAccount(Account):
    def account_type(self):
        return"Current Account"


class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def save_accounts(self):
        data = {}
        for number, account in self.accounts.items():
            data[number] ={
                "name": account.name,
                "pin": account._Account__pin,
                "balance": account.balance,
                "type": account.account_type(),
                "transactions":account.transactions
            }
        with open("bank_data.json", "w") as file:
            json.dump(data, file,indent=4)

    def load_accounts(self):
        if not os.path.exists("bank_data.json"):
            return
        try:
            with open("bank_data.json," "r") as file:
                data = json.load(file)
            for number, details in data.items():
                if details["type"] == "Savings Account":
                    account =SavingsAccount(
                        number,details["name"],"0000",
                        details["balance"]
                    )

                else:
                    account = CurrentAccount(
                        number,details["name"],"0000",
                        details["balance"]
                    )
                    account._Account__pin = details["pin"]
                    account.transactions = details["transactions"]
                    self.accounts[number] = account
        except(json.JSONDecodeError,KeyError):
            print("Warning:Could not load bank data.")

    def create_account(self):
        print("\n ===== CREATE BANK ACCOUNT ====") 
        name = input("Enter your full name:") .strip() 
        if not name:
            print("Name cannot be empty.")
            return
        pin = input("create a 4-digit PIN:")
        if not pin.isdigit() or len(pin)!=4:
             print("PIN must contain exactly 4 digits.")
             return
        number = str(datetime.now().timestamp()).replace(".","")[-10:]
        print("\nSelect account type:")
        print("1.Savings Account")
        print("2.Current Account")

        choice = input ("Enter choice:")
        if choice =="1":
            account = SavingsAccount(number,name,pin)
        elif choice =="2":
            account = CurrentAccount(number, name,pin)

        else:
            print("Invalid account type.")
            return
        self.accounts[number] = account
        self.save_accounts()

        print("\nAccount created successfully!")
        print("Account number:", number)
        print("Account holder:", name)

    def login(self):
        print("\n ===== ACCOUNT LOGIN ====")
        number = input ("Enter account number:")
        pin = input ("Enter your PIN:")
        account = self.accounts.get(number)
        if account and account.verify_pin(pin):
            print(f"\nWelcome, {account.name}!")
            self.account_menu(account)
        else:
            print("invalid account number or PIN.")
    def account_menu(self, account):
        while True:
            print("\n =====BANK MENU =====")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4.Transfer Money")
            print("5.Transaction History")
            print("6.Account Details")
            print("7.Logout")

            choice = input("Choose an option:")

            if choice == "1":
                print("Available balance:",
                      account.balance)
            elif choice == "2":
                try:
                    amount = float(input("Enter deposit amount:"))
                    if account.deposit(amount):
                        self.save_accounts()

                except ValueError:
                    print("Please enter a valid number.")

            elif choice =="3":
                try:
                    amount = float(input("Enter withdrawal amount:"))
                    if account.withdraw(amount):
                        self.save_accounts()

                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "4":
                self.transfer_money(account)

            elif choice =="5":
                self.show_transactions(account)

            elif choice == "6":
                print("\nAccount holder:", account.name)
                print("Account number:", account.account_number)
                print("Account type:", account.account_type())
                print("Balance:", account.balance)
            elif choice == "7":
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice.")


    def transfer_money(self,sender):
        receiver_number = input(
            " Enter receiver account numbeer:" 
        )
        receiver = self.accounts.get(receiver_number)

        if receiver is None:
            print("Receiver account not found.")
            return
        if receiver.account_number == sender.account_number:
            print("You cannot transfer money to yourself.")
            return
        try:
            amount = float(input("Enter transfer amount:"))
            if amount <=0:
                print("Invalid amount.")
                return
            if amount> sender.balance:
                print("Insufficient funds.")
                return
            sender.withdraw(amount)
            receiver.deposit(amount)

            sender.add_transaction(
                "Transfer sent to" + receiver_number,amount
            )
            receiver.add_transaction(
                "Transfer received from" + sender.account_number,amount
            )
            self.save_accounts()
            print("Transfer completed successfully!")
        except ValueError:
            print(" Enter a valid amount.")



    def show_transactions(self,account):
        print("\n===== TRANSACTION HISTORY =====")
        if not account.transactions:
            print("No transactions available.")
            return
        for transaction in account.transactions:
            print("---------------------")
            print("type:", transaction["type"])
            print("Amount: Ksh", transaction["amount"])
            print("Date", transaction["date"])
def main():
        bank = Bank()
        while True:
            print("\n******************************")
            print("       PYTHON BANKING SYSTEM")
            print("********************************")

            print("1. Create Account")
            print("2. Login")
            print("3. Exit")


            choice = input("Enter your choice:")

            if choice == "1":
                bank.create_account()

            elif choice =="2":
                bank.login()
            elif choice =="3":
                print("Thank you for using our banking system!")
                break
            else:
                print("invalid choice.Try again.")


if __name__ =="__main__":
    main()
            



