# lets try this again
from collections import deque


class LRU_Cache:
    def __init__(self, limit=100):
        self.cache = {}
        self.q = Node(key="headkey", value="headvalue")
        self.q.left = self.q
        self.q.right = self.q
        self.limit = limit

    def get(self, key):
        return self.cache.get(key, None)

    def add(self, key, value):
        if key in self.cache:
            self._add_already_in(key, value)
        else:
            node = Node(key, value)
            self.cache[key] = node
            # add node
            tmp = self.q.left
            self.q.left = node
            node.right = self.q
            node.left = tmp
            tmp.right = node
            if len(self.cache) > self.limit:
                self.remove(self.q.right.key)

    def _add_already_in(self, key, value):
        self.remove(key)
        self.add(key, value)

    def remove(self, key):
        node = self.cache[key]
        del self.cache[key]
        node.remove()


class Node:
    def __init__(self, key, value, left=None, right=None):
        self.value = value
        self.key = key
        self.left = left
        self.right = right

    def remove(self):
        if self.left is None:
            if self.right is None:
                return
            self.right.left = None
        elif self.right is None:
            self.left.right = None
        else:
            self.left.right = self.right
            self.right.left = self.left


def test_lru_cache():
    lru = LRU_Cache(10)
    for i in range(15):
        lru.add(f"k{i}", f"v{i}")
    assert "k0" not in lru.cache
    assert "k14" in lru.cache
    lru.add("k13", "vnew")
    assert lru.q.left.key == "k13"
    lru.add("k1", "v1")


def test_lru_cache_time():
    import time
    start=time.time()
    n=10**5
    lru = LRU_Cache(50)
    for i in range(n):
        lru.add(f"k{i%100}", f"v{i%100}")
    assert len(lru.cache) == 50
    assert time.time()-start < 1


## clearly it just goes through the queue left to right
def time_deque():
    # python deque remove O(n)???
    import time
    n=10**5
    start_time = time.time()
    q= deque()
    for i in range(n):
        q.append(i)
    for i in reversed(range(n)):
        q.remove(i)

    end_time = time.time()
    print(f"runtime: {end_time-start_time:.2f}s")

    start_time = time.time()
    q= deque()
    for i in range(n):
        q.append(i)
    for i in range(n):
        q.remove(i)
    end_time = time.time()
    print(f"runtime: {end_time-start_time:.2f}s")
