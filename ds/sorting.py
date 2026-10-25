"""Bubble sort and quick sort. Both return a new list, like sorted()."""

import random


def _identity(x):
    return x


def bubble_sort(iterable, key=None, reverse=False):
    items = list(iterable)
    key = key or _identity
    n = len(items)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            a, b = key(items[i]), key(items[i + 1])
            if (a < b) if reverse else (b < a):
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break
    return items


def quick_sort(iterable, key=None, reverse=False):
    items = list(iterable)
    key = key or _identity
    keys = [key(x) for x in items]
    order = list(range(len(items)))
    rng = random.Random()


    stack = [(0, len(order) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot = keys[order[rng.randint(lo, hi)]]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            k = keys[order[i]]
            if k < pivot:
                order[lt], order[i] = order[i], order[lt]
                lt += 1
                i += 1
            elif pivot < k:
                order[i], order[gt] = order[gt], order[i]
                gt -= 1
            else:
                i += 1
        stack.append((lo, lt - 1))
        stack.append((gt + 1, hi))

    result = [items[i] for i in order]
    if reverse:
        result.reverse()
    return result
