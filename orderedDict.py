from typing import Iterable

import pytest


class OrderedDict:
    def __init__(self):
        self.dict = {}
        self.first: Node = None
        self.last: Node = None

    def insert_values(self, values: Iterable):
        for k, v in values:
            self.insert(k, v)

    def insert(self, key: str, value: int):
        new_node = Node(key, value)
        if key in self.dict:
            self.dict[key].value = value
            this_node = self.dict[key]
            left_node = this_node.left
            right_node = this_node.right
            # self.remove(this_node)
            # self.insert(this_node)
            return

        if self.first is None:
            node = new_node
            self.first = node
            self.last = node
        else:
            old_last = self.last
            self.last = new_node
            old_last.right = self.last
            self.last.left = old_last
        self.dict[key] = new_node

    def get(self, key: str):
        node = self.dict.get(key)
        if node is not None:
            return node.value


class Node:
    def __init__(self, key: str, value: int):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


# tdd: test driven development
@pytest.fixture
def od():
    return OrderedDict()


def test_insert(od):
    values = [("a", 1), ("b", 2), ("c", 3)]
    for k, v in values:
        od.insert(k, v)


def test_get(od):
    values = [("a", 1), ("b", 2), ("c", 3)]
    for k, v in values:
        od.insert(k, v)
    for k, v in values:
        assert od.get(k) == v


def test_get_not_in(od):
    assert od.get("missing_key") is None


def test_get_first(od):
    assert od.first is None
    od.insert("a", 1)
    assert od.first.key == "a"
    assert od.first.value == 1


def test_get_last(od):
    assert od.last is None
    od.insert("a", 1)
    assert od.last.key == "a"
    assert od.last.value == 1


def test_insert2(od):
    od.insert("a", 1)
    od.insert("b", 2)
    assert od.first.key == "a"
    assert od.first.value == 1
    assert od.last.key == "b"
    assert od.last.value == 2


def test_insertn(od):
    values = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]
    od.insert_values(values)
    # forward
    node = od.first
    for k, v in values:
        print(node.key)
        assert node.key == k
        assert node.value == v
        node = node.right
    assert node is None
    # back
    node = od.last
    for k, v in values[::-1]:
        print(node.key)
        assert node.key == k
        assert node.value == v
        node = node.left
    assert node is None


def test_insert_same_key(od):
    od.insert("a", 1)
    od.insert("a", 2)
    assert od.first is od.last
    assert od.first.key == "a"
    assert od.first.value == 2


def test_insert_same_switch_order(od):
    values = [("a", 1), ("b", 2), ("a", 3), ("d", 4), ("b", 5)]
    od.insert_values(values)
    assert od.first.key == "d"
    assert od.first.value == 4
    assert od.first.left is None
    second = od.first.right
    assert second.left is od.first
    assert second.key == "a"
    assert second.value == 3
    third = second.right
    assert third.left is second
    assert third.key == "b"
    assert third.value == 5
    assert third.right is None
