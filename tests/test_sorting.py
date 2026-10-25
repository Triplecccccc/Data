import random

import pytest

from ds.sorting import bubble_sort, quick_sort

SORTS = [bubble_sort, quick_sort]

CASES = [
    [],
    [1],
    [2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 2, 3, 1, 2],
    [7, 7, 7, 7],
    [-3, 10, 0, -1, 5],
    [1.5, -0.5, 2.25, 0.0],
    ["pear", "apple", "fig"],
]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("data", CASES)
def test_known_cases(sort, data):
    assert sort(data) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_does_not_mutate_input(sort):
    data = [3, 1, 2]
    sort(data)
    assert data == [3, 1, 2]


@pytest.mark.parametrize("sort", SORTS)
def test_accepts_any_iterable(sort):
    assert sort((3, 1, 2)) == [1, 2, 3]
    assert sort(x for x in [2, 1]) == [1, 2]


@pytest.mark.parametrize("sort", SORTS)
def test_key_and_reverse(sort):
    words = ["ccc", "a", "bb"]
    assert sort(words, key=len) == ["a", "bb", "ccc"]
    assert sort([1, 3, 2], reverse=True) == [3, 2, 1]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("seed", range(10))
def test_random(sort, seed):
    rng = random.Random(seed)
    data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 200))]
    assert sort(data) == sorted(data)


def test_quick_sort_large_sorted_input():
    data = list(range(20000))
    assert quick_sort(data) == data
    assert quick_sort(data[::-1]) == data
    assert quick_sort([5] * 20000) == [5] * 20000
