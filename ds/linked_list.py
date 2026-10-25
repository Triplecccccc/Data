"""Singly linked list with a tail pointer."""


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, iterable=()):
        self._head = None
        self._tail = None
        self._size = 0
        for value in iterable:
            self.append(value)

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __contains__(self, value):
        return any(v == value for v in self)

    def __eq__(self, other):
        if not isinstance(other, LinkedList):
            return NotImplemented
        return len(self) == len(other) and list(self) == list(other)

    def __repr__(self):
        return f"LinkedList({list(self)!r})"

    def _normalize(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("list index out of range")
        return index

    def _node_at(self, index):
        node = self._head
        for _ in range(index):
            node = node.next
        return node

    def __getitem__(self, index):
        return self._node_at(self._normalize(index)).value

    def __setitem__(self, index, value):
        self._node_at(self._normalize(index)).value = value

    def append(self, value):
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value):
        self._head = _Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("list index out of range")
        if index == 0:
            self.prepend(value)
        elif index == self._size:
            self.append(value)
        else:
            prev = self._node_at(index - 1)
            prev.next = _Node(value, prev.next)
            self._size += 1

    def pop(self, index=-1):
        if self._size == 0:
            raise IndexError("pop from empty list")
        index = self._normalize(index)
        if index == 0:
            node = self._head
            self._head = node.next
            if self._head is None:
                self._tail = None
        else:
            prev = self._node_at(index - 1)
            node = prev.next
            prev.next = node.next
            if node is self._tail:
                self._tail = prev
        self._size -= 1
        return node.value

    def index(self, value):
        for i, v in enumerate(self):
            if v == value:
                return i
        raise ValueError(f"{value!r} is not in list")

    def remove(self, value):
        self.pop(self.index(value))

    def reverse(self):
        prev, node = None, self._head
        self._tail = self._head
        while node is not None:
            node.next, prev, node = prev, node, node.next
        self._head = prev

    def clear(self):
        self._head = self._tail = None
        self._size = 0
