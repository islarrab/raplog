class Stack(list):

    def push(self, data):
        self.append(data)

    def tos(self):
        if self:
            return self[-1]

    def peek(self, index):
        if self and 0 <= index < len(self):
            return self[index]

    def __iter__(self):
        if self:
            ptr = len(self) - 1
            while ptr >= 0:
                yield self[ptr]
                ptr -= 1
