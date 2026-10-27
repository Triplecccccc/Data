
_MISSING = object()


class _Node:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def _height(node):
    return node.height if node else 0


def _update(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node):
    return _height(node.left) - _height(node.right)


def _rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    _update(y)
    _update(x)
    return x


def _rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    _update(x)
    _update(y)
    return y


def _rebalance(node):
    _update(node)
    bf = _balance_factor(node)
    if bf > 1:
        if _balance_factor(node.left) < 0:
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if bf < -1:
        if _balance_factor(node.right) > 0:
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


class AVLTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def height(self):
        return _height(self.root)

    def _find(self, key):
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None

    def __contains__(self, key):
        return self._find(key) is not None

    def get(self, key, default=None):
        node = self._find(key)
        return node.value if node else default

    def __getitem__(self, key):
        node = self._find(key)
        if node is None:
            raise KeyError(key)
        return node.value

    def __setitem__(self, key, value):
        self.insert(key, value)

    def insert(self, key, value=None):
        def rec(node):
            if node is None:
                self._size += 1
                return _Node(key, value)
            if key < node.key:
                node.left = rec(node.left)
            elif key > node.key:
                node.right = rec(node.right)
            else:
                node.value = value
                return node
            return _rebalance(node)

        self.root = rec(self.root)

    def delete(self, key):
        def rec(node):
            if node is None:
                raise KeyError(key)
            if key < node.key:
                node.left = rec(node.left)
            elif key > node.key:
                node.right = rec(node.right)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                succ = node.right
                while succ.left is not None:
                    succ = succ.left
                node.key, node.value = succ.key, succ.value
                node.right = remove_min(node.right)
            return _rebalance(node)

        def remove_min(node):
            if node.left is None:
                return node.right
            node.left = remove_min(node.left)
            return _rebalance(node)

        self.root = rec(self.root)
        self._size -= 1

    def _extreme(self, attr):
        node = self.root
        if node is None:
            raise ValueError("tree is empty")
        while getattr(node, attr) is not None:
            node = getattr(node, attr)
        return node.key

    def min(self):
        return self._extreme("left")

    def max(self):
        return self._extreme("right")

    def items(self):
        stack, node = [], self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key, node.value
            node = node.right

    def __iter__(self):
        for key, _ in self.items():
            yield key
