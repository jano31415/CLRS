import math
import time
import random


class RMQ:
    def __init__(self, arr, min_max):
        self.cache = [arr]
        self.func = min_max
        self.precompute(arr, self.func)

    def precompute(self, arr, min_max):

        max_log = int(math.log2(len(arr)))
        for i in range(1, max_log + 1):
            new_row = []
            for j in range(0, len(arr) - 2 ** i + 1):
                new_row.append(min_max(self.cache[i - 1][j],
                                       self.cache[i - 1][j + 2 ** (i - 1)]))
            self.cache.append(new_row)

    # should be equal to min(arr[l:r]) care l == r, plus minus 1 error
    def query(self, l, r):

        log_val = int(math.log2(r - l))
        return self.func(self.cache[log_val][l],
                         self.cache[log_val][r - 2 ** log_val])


def check_same_as_naiv(arr, rmq):
    for l in range(len(arr)):
        for r in range(l + 1, len(arr)):
            res1 = min(arr[l:r])
            res2 = rmq.query(l, r)
            assert res1 == res2


def test_small_example_rmq():
    arr = [4, 3, 6, 5, 4, 7, 2, 5, 4]
    rmq = RMQ(arr, min)
    check_same_as_naiv(arr, rmq)


def test_random_rmq():
    N = 100
    arr = [random.randint(0, 100) for _ in range(N)]
    rmq = RMQ(arr, min)
    check_same_as_naiv(arr, rmq)


def time_rmq(N):
    arr = [random.randint(0, 100) for _ in range(N)]
    time1 = time.time()
    for l in range(len(arr)):
        for r in range(l + 1, len(arr)):
            res1 = min(arr[l:r])
    time2 = time.time()
    print(f"naiv len {N}: {time2 - time1}")

    time_rmq_only(N, arr)


def time_rmq_only(N, arr=None):
    if arr is None:
        arr = [random.randint(0, 100) for _ in range(N)]
    time1 = time.time()
    rmq = RMQ(arr, min)
    for l in range(len(arr)):
        for r in range(l + 1, len(arr)):
            res1 = rmq.query(l, r)
    time2 = time.time()
    print(f"rmq len {N}: {time2 - time1}")


def time_rmq_Q(N, Q, arr=None):
    if arr is None:
        arr = [random.randint(0, 100) for _ in range(N)]
    time1 = time.time()
    rmq = RMQ(arr, min)
    for i in range(Q):
        l = random.randint(0,N-2)
        r=random.randint(l+1,N-1)
        res1 = rmq.query(l, r)
    time2 = time.time()
    print(f"rmq len {N}: {time2 - time1}")

time_rmq(100) # slower
time_rmq(10**3) # faster
# from 10**4 on calculating all ranges is infeasible
# asking for linearly many range is still fast
time_rmq_Q(10**4, 10**4)
# N many range minimum queries for N up to 10**5 should still  be under magic 2s
time_rmq_Q(10**5, 10**5)