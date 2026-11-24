import pytest
from ds.lru_cache import LRUCache


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)


def test_put_and_get():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    assert c.get("b") == 2
    assert len(c) == 2


def test_get_missing():
    c = LRUCache(2)
    assert c.get("x") is None
    assert c.get("x", 0) == 0


def test_evicts_least_recently_used():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert "a" not in c
    assert c.get("b") == 2
    assert c.get("c") == 3
    assert len(c) == 2


def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")
    c.put("c", 3)
    assert "b" not in c
    assert "a" in c
    assert "c" in c


def test_put_existing_updates_and_refreshes():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("a") == 10
    assert "b" not in c
    assert len(c) == 2


def test_keys_order():
    c = LRUCache(3)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.keys() == ["c", "b", "a"]
    c.get("a")
    assert c.keys() == ["a", "c", "b"]


def test_contains_does_not_refresh():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert "a" in c
    c.put("c", 3)
    assert "a" not in c


def test_capacity_one():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("b", 2)
    assert "a" not in c
    assert c.get("b") == 2
    assert c.capacity == 1


def test_remove():
    c = LRUCache(3)
    c.put("a", 1)
    c.put("b", 2)
    c.remove("a")
    assert "a" not in c
    assert len(c) == 1
    with pytest.raises(KeyError):
        c.remove("a")
    c.put("c", 3)
    c.put("d", 4)
    assert c.keys() == ["d", "c", "b"]


def test_clear():
    c = LRUCache(2)
    c.put("a", 1)
    c.clear()
    assert len(c) == 0
    assert c.keys() == []
    c.put("b", 2)
    assert c.get("b") == 2


def test_stores_none_value():
    c = LRUCache(2)
    c.put("a", None)
    assert "a" in c
    assert c.get("a", "default") is None
