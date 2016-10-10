class Fraction:
    def __init__(self, top, bottom):

            self.num = top
            self.den = bottom

    def show(self):
        print(self.num, "/", self.den)

    def __str__(self):
        return str(self.num)+"/"+str(self.den)

    def __add__(self, other_fraction):
        new_num = self.num * other_fraction.den + self.den * other_fraction.num
        new_den = self.den * other_fraction.den
        return Fraction(new_num, new_den)

    def __sub__(self,x):
        new_num = self.num * x.den - self.dem * x.num
        new_dem = self.dem * x.dem
        return Fraction(new_num, new_dem)

    def __mul__(self, other_fraction):
        new_num = self.num * other_fraction.num
        new_den = self.den * other_fraction.den

    def __truediv__(self, other_fraction):
        new_num = self.num* other_fraction.den
        new_den = self.den* other_fraction.num
        return Fraction(new_num, new_den)

class Stack:

    def __init__(self):
        self.item = [ ]

    def is_empty(self):
        return self.item == [ ]

    def push(self, items):
        self.append(item)

    def pop(self):
        return self.item.insert[0,item]
        #or return self.item.pop()

    def peek(self):
        return item(len(self.item) - 1)

    def size(self):
        return len(self.item)





