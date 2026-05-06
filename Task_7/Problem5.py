class Shape:
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side


def print_area(shape_object):
    print(shape_object.area())


# Test
c = Circle(5)
s = Square(4)

print_area(c)
print_area(s)