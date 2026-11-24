import random
import pytest
from ds.hash_table import HashTable


def test_empty():
    h = HashTable()
    assert len(h) == 0
    assert h.keys() == []
    assert "a" not in h


def test_put_and_get():
    h = HashTable()
    h.put("a", 1)
    h.put("b", 2)
    assert h.get("a") == 1
    assert h.get("b") == 2
    assert len(h) == 2


def test_get_default():
    h = HashTable()
    assert h.get("missing") is None
    assert h.get("missing", 5) == 5


def test_update_existing_key():
    h = HashTable()
    h.put("a", 1)
    h.put("a", 2)
    assert h["a"] == 2
    assert len(h) == 1


def test_getitem_missing_raises():
    with pytest.raises(KeyError):
        HashTable()["x"]


def test_setitem_delitem():
    h = HashTable()
    h["a"] = 1
    assert "a" in h
    del h["a"]
    assert "a" not in h
    assert len(h) == 0


def test_remove_missing_raises():
    with pytest.raises(KeyError):
        HashTable().remove("x")


def test_init_from_dict_and_pairs():
    assert dict(HashTable({"a": 1, "b": 2}).items()) == {"a": 1, "b": 2}
    assert dict(HashTable([("a", 1), ("b", 2)]).items()) == {"a": 1, "b": 2}


def test_keys_values_items_iter():
    h = HashTable({"a": 1, "b": 2, "c": 3})
    assert sorted(h.keys()) == ["a", "b", "c"]
    assert sorted(h.values()) == [1, 2, 3]
    assert sorted(h.items()) == [("a", 1), ("b", 2), ("c", 3)]
    assert sorted(h) == ["a", "b", "c"]


def test_resize_keeps_data():
    h = HashTable()
    start = h.capacity
    for i in range(100):
        h.put(i, i * i)
    assert h.capacity > start
    assert len(h) == 100
    for i in range(100):
        assert h[i] == i * i


def test_collisions():
    class Same:
        def __init__(self, name):
            self.name = name

        def __hash__(self):
            return 1

        def __eq__(self, other):
            return isinstance(other, Same) and self.name == other.name

    h = HashTable()
    keys = [Same(str(i)) for i in range(5)]
    for i, key in enumerate(keys):
        h.put(key, i)
    for i, key in enumerate(keys):
        assert h.get(key) == i
    h.remove(keys[2])
    assert keys[2] not in h
    assert len(h) == 4


def test_various_key_types():
    h = HashTable()
    h.put(1, "int")
    h.put("1", "str")
    h.put((1, 2), "tuple")
    assert h[1] == "int"
    assert h["1"] == "str"
    assert h[(1, 2)] == "tuple"


def test_clear():
    h = HashTable({"a": 1})
    h.clear()
    assert len(h) == 0
    h.put("b", 2)
    assert h["b"] == 2


def test_random_operations_match_dict():
    rng = random.Random(7)
    h = HashTable()
    ref = {}
    for _ in range(3000):
        key = rng.randint(0, 300)
        if rng.random() < 0.6:
            value = rng.randint(0, 1000)
            h.put(key, value)
            ref[key] = value
        elif key in ref:
            h.remove(key)
            del ref[key]
        else:
            with pytest.raises(KeyError):
                h.remove(key)
        assert len(h) == len(ref)
    assert dict(h.items()) == ref
