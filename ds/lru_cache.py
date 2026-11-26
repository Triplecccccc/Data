class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("mi bomba capacity must be positive do it now or i will do something bad :)")
        self._capacity = capacity
        self._map = {}
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

    def __repr__(self):
        return f"LRUCache({[(k, self._map[k].value) for k in self.keys()]})"

    @property
    def capacity(self):
        return self._capacity

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node):
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def get(self, key, default=None):
        node = self._map.get(key)
        if node is None:
            return default
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self._map) >= self._capacity:
            oldest = self._tail.prev
            self._unlink(oldest)
            del self._map[oldest.key]
        node = _Node(key, value)
        self._map[key] = node
        self._push_front(node)

    def remove(self, key):
        node = self._map.pop(key, None)
        if node is None:
            raise KeyError(key)
        self._unlink(node)

    def keys(self):
        result = []
        node = self._head.next
        while node is not self._tail:
            result.append(node.key)
            node = node.next
        return result

    def clear(self):
        self._map.clear()
        self._head.next = self._tail
        self._tail.prev = self._head
