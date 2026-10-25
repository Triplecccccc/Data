import collections
import random

import pytest

from ds.deque import Deque


def test_empty():
    d = Deque()
    assert len(d) == 0
    assert not d
    with pytest.raises(IndexError):
        d.pop()
    with pytest.raises(IndexError):
        d.popleft()
    with pytest.raises(IndexError):
        d.peek()
    with pytest.raises(IndexError):
        d.peekleft()


def test_append_both_ends():
    d = Deque()
    d.append(2)
    d.append(3)
    d.appendleft(1)
    d.appendleft(0)
    assert list(d) == [0, 1, 2, 3]
    assert d.peekleft() == 0
    assert d.peek() == 3


def test_pop_both_ends():
    d = Deque([1, 2, 3, 4])
    assert d.pop() == 4
    assert d.popleft() == 1
    assert list(d) == [2, 3]


def test_indexing():
    d = Deque([1, 2, 3])
    d.appendleft(0)
    assert d[0] == 0
    assert d[-1] == 3
    d[1] = 10
    assert list(d) == [0, 10, 2, 3]
    with pytest.raises(IndexError):
        d[4]


def test_growth_with_wraparound():
    d = Deque()
    for i in range(50):
        d.appendleft(-i)
        d.append(i)
    assert len(d) == 100
    assert list(d) == list(range(-49, 1)) + list(range(50))


def test_clear_and_repr():
    d = Deque([1, 2])
    assert repr(d) == "Deque([1, 2])"
    d.clear()
    assert len(d) == 0
    assert list(d) == []


def test_matches_collections_deque():
    rng = random.Random(0)
    mine, ref = Deque(), collections.deque()
    for _ in range(5000):
        op = rng.randrange(4)
        if op == 0:
            x = rng.randrange(100)
            mine.append(x)
            ref.append(x)
        elif op == 1:
            x = rng.randrange(100)
            mine.appendleft(x)
            ref.appendleft(x)
        elif op == 2 and ref:
            assert mine.pop() == ref.pop()
        elif op == 3 and ref:
            assert mine.popleft() == ref.popleft()
        assert len(mine) == len(ref)
    assert list(mine) == list(ref)
