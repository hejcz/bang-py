class Queue:
    list = []

    def enqueue(self, element):
        self.list = self.list + [element]

    def peek(self):
        return self.list[0] if len(self.list) > 0 else None

    def poll(self):
        return self.list.pop(0) if len(self.list) > 0 else None