class EmptyStack(Exception):
    pass

class Stack(object):

    def __init__(self):
        self.head = StackBase()

    def __top__(self):
        return self.head
    
    def __push__(self, value):
        self.head = self.head.push(value)

    def __pop__(self):
        old_head = self.head
        self.head = self.head.pop()
        return old_head

    def len(self):
        return self.head.len()

    def is_empty(self):
        return self.head.is_empty()


class StackBase(object):

    def push(self, value):
        return StackItem(parent = self, value = value)

    def pop(self):
        raise EmptyStack("Pila vacía")

    def len(self):
        return 0

    def is_empty(self):
        return True
    
    def __repr__(self):
        return "Base de la pila"

    
class StackItem(object):

    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
    
    def push(self, value):
        return StackItem(parent = self, value = value)

    def pop(self):
        return self.parent

    def len(self):
        return self.parent.len() + 1

    def is_empty(self):
        return False

    def __repr__(self):
        return str(self.value)


stack = Stack()
