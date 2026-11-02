

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def display_info(self):
        status = "Available" if self.available else "Borrowed"
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Status: {status}")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"'{book.title}' added successfully!")

    def show_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            print("\nLibrary Books:")
            for book in self.books:
                book.display_info()
                print("-" * 20)

    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                if book.available:
                    book.available = False
                    print(f"You borrowed '{book.title}'")
                else:
                    print("Book is already borrowed.")
                return
        print("Book not found.")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                if not book.available:
                    book.available = True
                    print(f"You returned '{book.title}'")
                else:
                    print("Book was not borrowed.")
                return
        print("Book not found.")

library = Library()

while True:
    print("\n===== Library Menu =====")
    print("1. Add Book")
    print("2. Show Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter author: ")
        library.add_book(Book(title, author))

    elif choice == "2":
        library.show_books()

    elif choice == "3":
        title = input("Enter title to borrow: ")
        library.borrow_book(title)

    elif choice == "4":
        title = input("Enter title to return: ")
        library.return_book(title)

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")


        