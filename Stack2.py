###STEPHEN LUKE TODD
###ADVANCED DATA STRUCTURES 
class Stack:
        def __init__(self):
            self.items = []

        def is_empty(self):
            if not self.items:
                return True
            else:
                return False

        def push(self,items):
            self.items.append(items)

        def pop(self):
            return self.items.pop()

        def peek(self):
            return self.items[len(self.items)-1]

        def size(self):
            return len(self.items)

