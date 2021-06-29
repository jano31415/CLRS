from functools import lru_cache
from random import randint
from time import sleep

query_dict = {}
for i in range(101):
    v = randint(0, 500)
    query_dict[i] = v


def query(k):
    # print("query")
    sleep(0.01)
    return query_dict[k]

# the functools python implementation considers multithreading with locking
# of course my quick implementation can not do that. They use a lightweight list
# as a node instead of a class and just one root node and a circular linkedlist
# instead of start and end. Need to check some more edge cases but i think
# the general concept is correct.
class My_lru_cache:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.cache = {}
        self.start = None
        self.end = None
        self.length = 0

    def get(self, key):
        if key in self.cache:
            # print("cached")
            self.move_to_front(key)
            return self.cache[key].value
        else:
            value = query(key)
            self.add(key, value)
            return value

    def move_to_front(self, key):
        remove_node = self.cache[key]
        # link left to right
        if remove_node == self.start:
            return
        elif remove_node == self.end:
            remove_node.before.after = None
            self.end = remove_node.before
        else:
            rem_before = remove_node.before
            rem_after = remove_node.after
            rem_before.after = rem_after
            rem_after.before = rem_before
        # unlink node
        remove_node.before = None
        remove_node.after = None
        # use add to front
        self.add_to_front(remove_node)

    def add(self, key, value):
        if key in self.cache:
            return
        new_Node = Node(key, value)

        self.add_to_cache(new_Node)
        if self.length > self.maxsize:
            self.remove_last()
        self.add_to_front(new_Node)

    def add_to_cache(self, new_Node):
        self.cache[new_Node.key] = new_Node
        self.length += 1

    def add_to_front(self, new_Node):
        if new_Node == self.start:
            return
        if self.start is None:
            self.start = new_Node
            self.end = new_Node
            return
        new_Node.after = self.start
        self.start.before = new_Node
        self.start = new_Node
        assert self.start.before is None

    def remove_last(self):
        self._remove_from_cache(self.end)

        self.end.before.after = None
        tmp = self.end
        self.end = tmp.before
        tmp.before = None
        assert self.end.after is None

    def _remove_from_cache(self, node):
        del self.cache[node.key]
        self.length -= 1


class Node:
    def __init__(self, key, value, before=None, after=None):
        self.key = key
        self.value = value
        self.before = before
        self.after = after

from time import time
import random
random.seed(42)
maxsize = 50
keys = [randint(0, 100) for k in range(500)]

a = time()
mycache = {}
l1=[]
for k in keys:
    if k in mycache:
        v = mycache[k]
    else:
        v = query(k)
        mycache[k] = v
    l1.append(v)
b = time()
print(b-a)

a = time()
mycache = {}
l1=[]
for k in keys:
    l1.append(query(k))
b = time()
print(b-a)

a = time()
mycache = My_lru_cache(maxsize)
l1=[]
for k in keys:
    l1.append(mycache.get(k))
b = time()
print(b-a)
assert len(mycache.cache) <= maxsize

@lru_cache(maxsize=maxsize)
def query2(k):
    return query(k)

a = time()
l2=[]
for k in keys:
    l2.append(query2(k))
b=time()
print(b-a)
print(l1)
print(l2)
assert l1 == l2

assert len(mycache.cache) == maxsize