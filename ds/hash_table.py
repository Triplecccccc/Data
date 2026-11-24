class HashTable:
    _INITIAL_CAPACITY = 8
    _MAX_LOAD = 0.75

    def __init__(self, items=()):
        self._capacity = self._INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        pairs = items.items() if hasattr(items, "items") else items
        for key, value in pairs:
            self.put(key, value)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self._find(key) is not None

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        pair = self._find(key)
        if pair is None:
            raise KeyError(key)
        return pair[1]

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __repr__(self):
        return f"HashTable({dict(self.items())})"

    @property
    def capacity(self):
        return self._capacity

    def _index(self, key):
        return hash(key) % self._capacity

    def _find(self, key):
        for pair in self._buckets[self._index(key)]:
            if pair[0] == key:
                return pair
        return None

    def _resize(self, new_capacity):
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        for bucket in old_buckets:
            for key, value in bucket:
                self._buckets[self._index(key)].append([key, value])

    def put(self, key, value):
        pair = self._find(key)
        if pair is not None:
            pair[1] = value
            return
        self._buckets[self._index(key)].append([key, value])
        self._size += 1
        if self._size / self._capacity > self._MAX_LOAD:
            self._resize(self._capacity * 2)

    def get(self, key, default=None):
        pair = self._find(key)
        return default if pair is None else pair[1]

    def remove(self, key):
        bucket = self._buckets[self._index(key)]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def keys(self):
        return [pair[0] for bucket in self._buckets for pair in bucket]

    def values(self):
        return [pair[1] for bucket in self._buckets for pair in bucket]

    def items(self):
        return [(pair[0], pair[1]) for bucket in self._buckets for pair in bucket]

    def clear(self):
        self._capacity = self._INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
