
class Deque:
    _MIN_CAPACITY = 8

    def __init__(self, iterable=()):
        self._data = [None] * self._MIN_CAPACITY
        self._head = 0
        self._size = 0
        for value in iterable:
            self.append(value)

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[(self._head + i) % len(self._data)]

    def __repr__(self):
        return f"Deque({list(self)!r})"

    def _physical(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("deque index out of range")
        return (self._head + index) % len(self._data)

    def __getitem__(self, index):
        return self._data[self._physical(index)]

    def __setitem__(self, index, value):
        self._data[self._physical(index)] = value

    def _grow_if_full(self):
        if self._size == len(self._data):
            self._data = list(self) + [None] * len(self._data)
            self._head = 0

    def append(self, value):
        self._grow_if_full()
        self._data[(self._head + self._size) % len(self._data)] = value
        self._size += 1

    def appendleft(self, value):
        self._grow_if_full()
        self._head = (self._head - 1) % len(self._data)
        self._data[self._head] = value
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise IndexError("pop from empty deque")
        i = self._physical(-1)
        value, self._data[i] = self._data[i], None
        self._size -= 1
        return value

    def popleft(self):
        if self._size == 0:
            raise IndexError("pop from empty deque")
        value, self._data[self._head] = self._data[self._head], None
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return value

    def peek(self):
        if self._size == 0:
            raise IndexError("peek from empty deque")
        return self[-1]

    def peekleft(self):
        if self._size == 0:
            raise IndexError("peek from empty deque")
        return self[0]

    def clear(self):
        self._data = [None] * self._MIN_CAPACITY
        self._head = 0
        self._size = 0
