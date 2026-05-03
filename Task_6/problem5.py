class Book:
    def __init__(self, title, author, is_available = True):
        self.title = title
        self.author = author
        self.is_available = is_available

    def borrow_book(self):
        if self.is_available:
            self.is_available = False
            print(f"{self.title} borrowed successfully")

        else:
            print(f"{self.title} is already out")

b = Book("Book1", "Mike")
b.borrow_book()
b.borrow_book()