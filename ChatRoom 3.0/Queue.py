class Queue:
    head = None
    tail = None

    class Node:
        next = None
        value = None

        def __init__(self, value):
            self.value = value

    def put(self, value):
        if self.head == None:
            self.head = self.Node(value)
            self.tail = self.head

        else:
            self.tail.next = self.Node(value)
            self.tail = self.tail.next

    def empty(self):
        return self.head == None

    def get(self):
        if self.head == None:
            return None
            
        value = self.head.value

        if self.head.next == None:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next

        return value