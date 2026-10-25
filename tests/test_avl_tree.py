import random

import pytest

from ds.avl_tree import AVLTree


def check_invariants(tree):
    """Check BST ordering, AVL balance and stored heights; return height."""

    def walk(node, lo, hi):
        if node is None:
            return 0
        assert (lo is None or node.key > lo) and (hi is None or node.key < hi)
        lh = walk(node.left, lo, node.key)
        rh = walk(node.right, node.key, hi)
        assert abs(lh - rh) <= 1
        assert node.height == 1 + max(lh, rh)
        return node.height

    return walk(tree.root, None, None)


def test_empty():
    t = AVLTree()
    assert len(t) == 0
    assert list(t) == []
    assert 1 not in t
    assert t.height() == 0
    with pytest.raises(ValueError):
        t.min()
    with pytest.raises(ValueError):
        t.max()


def test_insert_and_inorder():
    t = AVLTree()
    for k in [5, 3, 8, 1, 4, 7, 9]:
        t.insert(k)
    assert list(t) == [1, 3, 4, 5, 7, 8, 9]
    assert len(t) == 7
    assert t.min() == 1
    assert t.max() == 9
    check_invariants(t)


def test_duplicate_insert_updates_value():
    t = AVLTree()
    t.insert(1, "a")
    t.insert(1, "b")
    assert len(t) == 1
    assert t.get(1) == "b"


def test_get_and_mapping_api():
    t = AVLTree()
    t[2] = "two"
    t[1] = "one"
    assert t[2] == "two"
    assert t.get(3) is None
    assert t.get(3, "x") == "x"
    with pytest.raises(KeyError):
        t[3]
    assert list(t.items()) == [(1, "one"), (2, "two")]


@pytest.mark.parametrize(
    "keys",
    [
        [3, 2, 1],  # LL
        [1, 2, 3],  # RR
        [3, 1, 2],  # LR
        [1, 3, 2],  # RL
    ],
)
def test_rotations(keys):
    t = AVLTree()
    for k in keys:
        t.insert(k)
    assert t.root.key == 2
    assert t.height() == 2
    check_invariants(t)


def test_sorted_insert_stays_logarithmic():
    t = AVLTree()
    n = 1023
    for k in range(n):
        t.insert(k)
    check_invariants(t)
    assert t.height() <= 1.45 * 10 + 1  # 1.44 * log2(n + 2)


def test_delete():
    t = AVLTree()
    for k in range(10):
        t.insert(k)
    t.delete(0)  # leaf
    t.delete(3)  # inner node
    t.delete(t.root.key)  # root
    assert 0 not in t and 3 not in t
    assert len(t) == 7
    check_invariants(t)
    with pytest.raises(KeyError):
        t.delete(100)


def test_random_against_set():
    rng = random.Random(42)
    t, ref = AVLTree(), set()
    for _ in range(3000):
        k = rng.randrange(500)
        if rng.random() < 0.6:
            t.insert(k)
            ref.add(k)
        elif k in ref:
            t.delete(k)
            ref.remove(k)
        else:
            with pytest.raises(KeyError):
                t.delete(k)
    assert list(t) == sorted(ref)
    assert len(t) == len(ref)
    check_invariants(t)
