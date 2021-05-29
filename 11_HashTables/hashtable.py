import random

# ok so this is just an array
class DirectAdress:
    def __init__(self, max_N):
        self.table = [None]*max_N

    def insert(self, key, value):
        self.table[key] = value

    def search(self, key):
        return self.table[key]

    def delete_key(self, key):
        self.table[key] = None

    def delete_value(self, value):
        # i feel like its unrealistic to have the value an object that knows
        # its position.
        self.table.remove(value)


def test_direct_address():
    N = 10
    direct = DirectAdress(N)
    for i in range(N):
        v=random.random()
        direct.insert(i, v)
        print(direct.search(i))
        assert direct.search(i) == v
        direct.delete_key(i)
        assert direct.search(i) is None


class Node:
    def __init__(self, key, v):
        self.v = v
        self.before = None
        self.after = None
        self.key = key

    def to_list(self):
        l = [self.v]
        node = self
        while node.after is not None:
            l.append(node.v)
            node = node.after
        return l

class HashTableChain:
    def __init__(self, max_N):
        self.table = [None]*max_N
        self.max_N = max_N

    def hash(self, key):
        return key % self.max_N

    def insert(self, orig_key, value):
        hash_adress = self.hash(orig_key)
        new_Node = Node(orig_key, value)
        if self.table[hash_adress] is None:
            self.table[hash_adress] = new_Node
        else:
            node = self.table[hash_adress]
            if node.key == orig_key:
                self.table[hash_adress] = new_Node
                if node.after is not None:
                    new_Node.after = node.after
                    new_Node.after.before = new_Node
                    # node.before always None
                    return
            while node.after is not None:
                if node.key == orig_key:
                    new_Node.before = node.before
                    new_Node.after = node.after
                    new_Node.before.after = new_Node
                    new_Node.after.before = new_Node
                    return
                node = node.after
            node.after = new_Node
            new_Node.before = node

    def search(self, orig_key):
        node = self.search_node(orig_key)
        if node is not None:
            return node.v
        return None

    def search_node(self, orig_key):
        hash_adress = self.hash(orig_key)
        node = self.table[hash_adress]
        if node is None:
            return None
        while node.after is not None:
            if node.key == orig_key:
                return node
            node = node.after
        if node.key == orig_key:
            return node
        return None

    def delete_key(self, key):
        node = self.search_node(key)
        if node is None:
            return
        if node.before is None:
            self.table[self.hash(key)] = node.after
        else:
            node.before.after = node.after
        if node.after is not None:
            node.after.before = node.before


def test_hash_chain():
    N = 100000
    direct = HashTableChain(N)
    import time
    time1=time.time()
    for _ in range(int(0.1*N)):
        i = random.randint(0, 10*N)
        v = random.random()
        direct.insert(i, v)
    time2=time.time()
    print(time2-time1)

    direct.insert(N+11, "wrong")
    direct.insert(11, "test")
    assert direct.search(11) == "test"
    direct.delete_key(11)
    assert direct.search(11) is None
    assert direct.search(N+11) == "wrong"

    python_dict = {}
    time1=time.time()
    for _ in range(int(0.1*N)):
        i = random.randint(0, 10*N)
        v = random.random()
        python_dict[i] = v
    time2=time.time()
    print(time2-time1)

    # around three times slower for 2 time as many as size
    # around 60% slower for only 20% fuller. Of course the python dice adapts its size

    # print([x.to_list() if x is not None else x for  x in direct.table])
