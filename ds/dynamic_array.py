"""Dynamic array over a fixed-size buffer that doubles/halves its capacity."""


class DynamicArray:
    _MIN_CAPACITY = 4

    def __init__(self, iterable=()):
        self._capacity = self._MIN_CAPACITY
        self._data = [None] * self._capacity
        self._size = 0
        for value in iterable:
            self.append(value)

    @property
    def capacity(self):
        return self._capacity

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def __contains__(self, value):
        return any(v == value for v in self)

    def __eq__(self, other):
        if not isinstance(other, DynamicArray):
            return NotImplemented
        return list(self) == list(other)

    def __repr__(self):
        return f"DynamicArray({list(self)!r})"

    def _normalize(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("array index out of range")
        return index

    def __getitem__(self, index):
        return self._data[self._normalize(index)]

    def __setitem__(self, index, value):
        self._data[self._normalize(index)] = value

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        self.insert(self._size, value)

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("array index out of range")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def pop(self, index=-1):
        if self._size == 0:
            raise IndexError("pop from empty array")
        index = self._normalize(index)
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        if self._capacity > self._MIN_CAPACITY and self._size <= self._capacity // 4:
            self._resize(max(self._MIN_CAPACITY, self._capacity // 2))
        return value

    def index(self, value):
        for i, v in enumerate(self):
            if v == value:
                return i
        raise ValueError(f"{value!r} is not in array")

    def remove(self, value):
        self.pop(self.index(value))

    def clear(self):
        self._capacity = self._MIN_CAPACITY
        self._data = [None] * self._capacity
        self._size = 0
