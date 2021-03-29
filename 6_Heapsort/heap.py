import math


# i implemented the max heap of CLRS. Python default is a min heap.
class Heap:
    def __init__(self, array):
        self.array = array
        self.len_array = len(array)
        self.max_heapify()

    def max_heapify(self):
        max_non_leaf = self.len_array - math.ceil(self.len_array/2) - 1
        for i in reversed(range(0, max_non_leaf + 1)):
            self.heapify_index_loop(i)

    def left(self, i):
        return 2*i + 1
        # return (i << 1) + 1

    def right(self, i):
        return 2*i + 2
        # return (i << 1) + 2

    def swap(self, i, j):
        tmp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = tmp

    def heapify_index(self, i):
        left = 2*i + 1 #self.left(i)
        right = 2*i + 2 #self.right(i)
        ind_largest_child = left
        if left >= self.len_array:
            ind_largest_child = i
        if right < self.len_array and self.array[ind_largest_child] < self.array[right]:
            ind_largest_child = right

        if self.array[i] < self.array[ind_largest_child]:
            self.swap(i, ind_largest_child)
            self.heapify_index(ind_largest_child)

    def heapify_index_loop_right_first(self, i):
        curr_i = i
        max_child = 2*i + 2
        while max_child < self.len_array:
            right_child = max_child - 1
            if self.array[right_child] > self.array[max_child]:
                max_child = right_child

            if self.array[max_child] > self.array[curr_i]:
                self.swap(curr_i, max_child)
                curr_i = max_child
            else:
                break
            max_child = 2*max_child+2

        # i made this up. Shouldnt this be faster to have one less check in each loop?
        if max_child == self.len_array and self.array[max_child-1] > curr_i:
            self.swap(curr_i, max_child-1)

    def heapify_index_loop(self, i):
        curr_i = i
        max_child = 2*i + 1
        while max_child < self.len_array:
            right_child = max_child + 1
            if right_child < self.len_array and self.array[right_child] > self.array[max_child]:
                max_child = right_child

            if self.array[max_child] > self.array[curr_i]:
                self.swap(curr_i, max_child)
                curr_i = max_child
            else:
                break
            max_child = 2*max_child+1


    def heappop(self):
        max_element = self.array[0]
        self.array[0] = self.array[self.len_array - 1]
        # !! drop the last element by reducing the len by one, fast "delete"
        self.len_array -= 1
        self.heapify_index(0)
        return max_element

    def sort(self):
        len_array = self.len_array
        for i in range(2, len_array+1):
            # could be less than the real length
            self.array[len_array-i] = self.heappop()
        self.len_array = len_array



import time
import random
from heapq import heappop, heapify
random.seed(42)


def test_heapify():
    n = 10000
    n2 = 10**3
    array = [random.randint(0,n) for _ in range(n2)]
    array2 = array[:]
    array3 = array[:]
    a = time.time()
    heap = Heap(array)
    b = time.time()
    print(f" time heapify my implementation: {b-a}")

    assert all([heap.array[i] >= heap.array[heap.left(i)] for i in range(heap.len_array) if heap.left(i) < heap.len_array])
    assert all([heap.array[i] >= heap.array[heap.right(i)] for i in range(heap.len_array) if heap.right(i) < heap.len_array])


    a = time.time()
    heapify(array2)
    b = time.time()
    print(f" time heapify heapq: {b-a}")

    assert all([array2[i] <= array2[2*i+1] for i in range(len(array2)) if 2*i+1 < len(array2)])
    assert all([array2[i] <= array2[2*i+2] for i in range(len(array2)) if 2*i+2 < len(array2)])

def test_heap_sort():
    n = 10000
    n2 = 10 ** 3
    array = [random.randint(0, n) for _ in range(n2)]
    array2 = array[:]
    array3 = array[:]
    heap = Heap(array)

    # urgs its quite a lot slower ~20 times
    a = time.time()
    heap.sort()
    b = time.time()
    print(f" time sort my implementation: {b-a}")

    # heapq does not really provide a sort. I think the sort on that list is still
    # normal python list sort. radix. This would be to check how fast are heappops
    a = time.time()
    l = []
    for i in range(len(array2)):
        l.append(heappop(array2))
    array2 = l
    b = time.time()
    print(f" time sort heapq: {b-a}")


    #much faster
    a = time.time()
    array3.sort()
    b = time.time()
    print(f" time sort list default: {b-a}")
    assert heap.array == array
