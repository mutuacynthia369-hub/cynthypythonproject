import json
import os


class Room:
    def __init__(self, room_number, room_type,price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_available = True

    def display_room(self):
        status = "Available" if self.is_available else "Bookeed"

        print(
            f"Room { self.room_number}|"
            f"{self.room_type}|"
            f"Ksh{self.price}per night|"
            f"{status}"
        )

class Customer:
    def __init__(self, customer_id, name,phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone

    def display_customer(self):
        print(f"ID:{self.customer_id}")
        print(f"Name:{self.name}")
        print(f"Phone: {self.phone}")


class VIPCustomer(Customer):
    def __init__(self, customer_id, name, phone):
        super().__init__(customer_id, name, phone)
        self.discount =10

    def display_customer(self):
         super().display_customer()
         print (f"VIP Discount: {self.discount}%")

class Hotel:
    def __init__(self):
        self.rooms = {
            101: Room(101,"Single", 2000),
            102: Room(102," Double", 3500),
            103: Room(103,"Deluxe", 5000),
            104: Room(104, "Executive",8000)
        }

        self.customers = {}
        self.bookings = {}
        self.load_data()
    def load_data(self):
        try:
            with open("hotel_data.json", "r") as file:
                data = json.load(file)

            saved_rooms = data.get("rooms", {})

            if saved_rooms:
                self.rooms = {
                    int(room): details
                    for room, details in saved_rooms.items()
                }

            self.bookings = data.get("bookings", {})

        except FileNotFoundError:
            self.bookings = {}

        except json.JSONDecodeError:
            print("Error: Hotel data file is corrupted.")
            self.bookings = {}
           
    def register_customer(self):
        customer_id = input("Enter customer ID:")

        if customer_id in self.customers:
            print("Customer ID already exists!")
            return

        name = input("Enter customer name:")
        phone = input("Enter phone number:")

        vip = input("Is this a VIP customer? (yes/no):").lower()


        if vip == "yes":
            customer = VIPCustomer( customer_id, name,phone )

        else:
            customer = Customer(customer_id,name,phone)

        self.customers[customer_id] = customer

        print ("Customer registered successfully!")
        self.save_data()



    def display_rooms(self):
        print("\n -----HOTEL ROOMS -----")

        for room in self.rooms.values():
            room.display_room()


    def book_room(self):
        customer_id = input ("Enter customer ID:")

        if customer_id not in self.customers:
            print("Customer not found!")
            return

        try:
            room_number = int(input("Enter room number:"))
            nights = int(input("Enter number of nights:"))

            if nights <= 0:
                print(" Number of nights must be greater than zero.")
                return
            if room_number not in self.rooms:
                print("Room does not exist!")
                return
            room = self.rooms[room_number]

            if not room.is_available:
                print("Sorry, this room is already booked!")
                return
            customer = self.customers[customer_id]
            total = room.price* nights
            if isinstance(customer,VIPCustomer):
                total -= total * customer.discount / 100

            room.is_available = False

            self.bookings[room_number]={
                "customer_id": customer_id,
                "nights": nights,
                "total": total
            }


            print("\nBooking successful!")
            print(f"Customer : { customer.name}")
            print(f"Room: {room_number}")
            print(f"Nights:{nights}")
            print(f"Total bill: Ksh{total:,.2f}")

            self.save_data()

        except ValueError:
            print("Please enter valid numbers!")

    def view_customers(self):
        if not self.customers:
            print("No customers registered.")
            return

        for customer in self.customers.values():
            print("\n -----------")
            customer.display_customer()


    def checkout(self):
        try:
            room_number = int(input("Enter room number:"))

            if room_number not in self.bookings:
                print("No booking found for this room!")
                return
            booking = self.bookings[room_number]

            print(f"Final bill: Ksh {booking['total']:,.2f}")
            self.rooms[room_number].is_available = True
            del self.bookings[room_number]
            print("checkout completed successfully!")


            self.save_data()

        except ValueError:
            print("Enter a valid room number!")


    def view_customers(self):
        if not self.customers:
            print("No customers registered.")
            return
        for customer in self.customers.values():
            print("\n ----------------")
            customer.display_customer()

    def checkout(self):
        try:
            room_number = int(input("Enter room number:"))
            if room_number not in self.bookings:
                print("No booking found for this room!")
                return
            booking = self.bookings[room_number]

            print(f"Final bill: Ksh{booking['total']:,.2f}")

            self.rooms[room_number].is_available = True
            del self.bookings[room_number]
            print(f"Checkout completed successfully!")
            self.save_data()


        except ValueError:
            print("Enter a valid room number!")


    def save_data(self):
        data  = {
            "customers": {},
            "bookings": self.bookings
        }
        for customer_id, customer in self.customers.items():
            data["customers"][customer_id] = {
                "name": customer.name,
                "phone": customer.phone,
                "vip": isinstance(customer, VIPCustomer)
            }

            data["bookings"] = {
               str (room): booking
               for room, booking in self.bookings.items()

            }
            with open("hotel_data.json", "w") as file:
                json.dump(data, file,indent=4)

        def load_data(self):
         if not os.path.exists("hotel_data.json"):
            return

        try:
            with open("hotel_data.json", "r") as file:
                data = json.load(file)

            for customer_id, details in data.get("customers", {}).items():

                if details["vip"]:
                    customer = VIPCustomer(
                        customer_id,
                        details["name"],
                        details["phone"]
                    )
                else:
                    customer = Customer(
                        customer_id,
                        details["name"],
                        details["phone"]
                    )

                self.customers[customer_id] = customer

            for room, booking in data.get("bookings", {}).items():
                room_number = int(room)

                if room_number in self.rooms:
                    self.bookings[room_number] = booking
                    self.rooms[room_number].is_available = False

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Could not load saved hotel data.")


def main():

    hotel = Hotel()

    while True:

        print("\n================================")
        print("       HOTEL MANAGEMENT SYSTEM")
        print("================================")
        print("1. Register Customer")
        print("2. View Hotel Rooms")
        print("3. Book Room")
        print("4. View Customers")
        print("5. Check Out")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            hotel.register_customer()

        elif choice == "2":
            hotel.display_rooms()

        elif choice == "3":
            hotel.book_room()

        elif choice == "4":
            hotel.view_customers()

        elif choice == "5":
            hotel.checkout()

        elif choice == "6":
            print("Thank you for using our hotel system!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
  
             
             


    
                                                 
                                                 
                                                 
                                                 
                                                 
                                                 
                                                 





