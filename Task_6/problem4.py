class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height
    
r = Rectangle(4, 5)
print(r.get_area())
    