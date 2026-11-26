# data-structures

Учебные реализации на Python (написаны по TDD: сначала тесты, потом код).

| Модуль | Что внутри |
|---|---|
| `ds/linked_list.py` | Односвязный список `LinkedList` |
| `ds/dynamic_array.py` | Динамический массив `DynamicArray` (удвоение/сжатие ёмкости) |
| `ds/deque.py` | Дек `Deque` на кольцевом буфере |
| `ds/avl_tree.py` | АВЛ-дерево `AVLTree` (вставка, удаление, поиск, обход) |
| `ds/sorting.py` | `bubble_sort`, `quick_sort` (с `key` и `reverse`) |

## Тесты

```bash
python3 --version && python3 -m pytest -v 2>&1 | tail -60
```

CI (GitHub Actions) прогоняет тесты на Python 3.9–3.13 при каждом push и pull request.
