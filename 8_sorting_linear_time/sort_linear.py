import random


# nice stuff. I knew this but it was also easy to implement.
# quite some memory and the book has an array only solution.
# this is a little different if you the numbers are objects where we need to carry around.
# satellite data.
def count_sort(arr, max_N):
    cache = [0] * (max_N + 1)
    # cache_map = {i:0 for i in range(max_N+1)}
    # if you know the set of numbers, keys but its not 1-N
    for a in arr:
        cache[a] += 1

    count = 0
    for i in range(1, max_N + 1):
        i_elem = cache[i]
        for j in range(i_elem):
            arr[count] = i
            count += 1
    return arr


def test_count_sort():
    res = count_sort([2, 1, 5, 4, 3, 3, 1], 5)
    print(res)


def count_sort_satellite(arr, max_N):
    count_tot = [0] * (max_N + 1)
    get_sort_data = lambda x: x[0]
    for a in arr:
        count_tot[get_sort_data(a)] += 1
    for j in range(1, len(count_tot)):
        count_tot[j] = count_tot[j - 1] + count_tot[j]
    res = [0] * len(arr)
    for a in arr:
        sort_a = get_sort_data(a)-1
        res[count_tot[sort_a]] = a
        count_tot[sort_a] += 1
    return res

def count_sort_satellite0(arr, max_N):
    count_tot = [0] * (max_N + 2)
    get_sort_data = lambda x: x[0]
    for a in arr:
        count_tot[get_sort_data(a)+1] += 1

    for j in range(1, len(count_tot)):
        count_tot[j] = count_tot[j - 1] + count_tot[j]
    res = [0] * len(arr)
    for a in arr:
        sort_a = get_sort_data(a)
        res[count_tot[sort_a]] = a
        count_tot[sort_a] += 1
    return res

def count_sort_satellite0_lambda(arr, max_N, lambda_index):
    count_tot = [0] * (max_N + 2)
    get_sort_data = lambda x: int(x[lambda_index])

    for a in arr:
        count_tot[get_sort_data(a)+1] += 1

    for j in range(1, len(count_tot)):
        count_tot[j] = count_tot[j - 1] + count_tot[j]
    res = [0] * len(arr)
    for a in arr:
        sort_a = get_sort_data(a)
        res[count_tot[sort_a]] = a
        count_tot[sort_a] += 1
    return res


# this got ugly
def count_sort_satellite_hashmap(arr, val_list):
    count_tot = {x: 0 for x in val_list}
    get_sort_data = lambda x: x[0]
    for a in arr:
        count_tot[get_sort_data(a)] += 1
    count_j_2 = 0
    for j in range(1, len(count_tot)):
        count_j_1 = count_tot[val_list[j]]
        count_tot[val_list[j]] = count_j_2 + count_tot[val_list[j-1]]
        count_j_2 = count_j_1

    count_tot[val_list[0]] = 0
    res = [0] * len(arr)
    for a in arr:
        sort_a = get_sort_data(a)
        res[count_tot[sort_a]] = a
        count_tot[sort_a] += 1
    return res

def count_sort_satellite_hashmap_lambda(arr, val_list, lambda_index):
    count_tot = {x: 0 for x in val_list}
    get_sort_data = lambda x: x[lambda_index]

    for a in arr:
        count_tot[get_sort_data(a)] += 1

    count_j_2 = 0
    for j in range(1, len(count_tot)):
        count_j_1 = count_tot[val_list[j]]
        count_tot[val_list[j]] = count_j_2 + count_tot[val_list[j-1]]
        count_j_2 = count_j_1

    count_tot[val_list[0]] = 0
    res = [0] * len(arr)
    for a in arr:
        sort_a = get_sort_data(a)
        res[count_tot[sort_a]] = a
        count_tot[sort_a] += 1
    return res


import time

def test_count_satellite():
    arr = [(random.randint(1, 5), random.randint(10, 20)) for _ in range(100000)]
    a = time.time()
    res = count_sort_satellite(arr, 5)
    b = time.time()
    arr.sort(key=lambda x: x[0])
    c = time.time()
    print(b - a)
    print(c - b)

    assert res == arr, res[:10]

    # python implementation pretty good.
    val_list = [1, 17, 128, 1234, 10 ** 6]
    arr = [(val_list[random.randint(0, 4)], random.randint(10, 20)) for _ in
           range(100000)]
    print(arr[:4])
    a = time.time()
    res = count_sort_satellite_hashmap(arr, val_list)
    b = time.time()
    arr.sort(key=lambda x: x[0])
    c = time.time()
    print(b - a)
    print(c - b)
    assert res == arr, res[:5]
#test_count_satellite()

# radix sort
# optimal value depends on size of list
# in a real programming language ofcourse this is implemented with the binary
# number representation shifts and stuff. I implement it the real way when i know C++
# no im still a 0 to 9 guy and this looks fun.

# for small n this looks faster in O notation being Delta(n) but high constant factors.
# if we split it into d groups that we sort by count_sort where each group has k possible values
# then this runs in O(d*(n+k))
def radix09(arr):
    max_len = len(str(max(arr)))
    ld = [str(x).rjust(max_len, "0") for x in arr]
    str9 = [str(i) for i in range(10)]
    for d in range(1, max_len + 1):
        ld = count_sort_satellite_hashmap_lambda(ld, str9, -d)
    return [int(x) for x in ld]

# my implementation is 20 times slower than python native.
# i blame slow python loops and overhead instead of me being stupid.
def radix09_2(arr):
    max_len = len(str(max(arr)))
    ld = [str(x).rjust(max_len, "0") for x in arr]
    for d in range(1, max_len + 1):
        ld = count_sort_satellite0_lambda(ld, 9, -d)
    return [int(x) for x in ld]

# accessing the different digits is really slow the way i did it.
# i think i got an idea.
def test_radix():
    max_n = 10**3-1
    arr = [random.randint(1, max_n) for _ in range(10**5)]
    a = time.time()
    res1 = radix09(arr)
    b = time.time()
    print(b-a)
    a = time.time()
    res2 = sorted(arr)
    b = time.time()
    print(b-a)

    a = time.time()
    res3 = count_sort(arr, max_n)
    b = time.time()
    print(b-a)

    assert res1 == res2, res1
    assert res3 == res2, res3


# bucket sort
# book claims that the average of square of bucket list sizes is 2 - 1/n
# and if we sort the bucket lists in k**2 then running time is n * (2- 1/n)
# O(n)
# key in the proof is to proof that its unlikely that buckets are getting big.
def bucket_sort(arr):
    len_arr = len(arr)
    buckets = [[] for _ in range(int(len_arr))]
    for a in arr:
        buckets[int(a*len_arr)].append(a)
    # assert sum([len(x) for x in buckets]) == len_arr
    print(max([len(x) for x in buckets]))
    # of course here i should implement my own sort thats good on small lists
    # good enough to get the idea
    return [a for bucket in buckets for a in sorted(bucket)]

def test_bucket_sort():
    arr = [random.random() for _ in range(10**6)]
    a = time.time()
    res1 = bucket_sort(arr)
    b = time.time()
    print(b-a)
    a = time.time()
    res2 = sorted(arr)
    b = time.time()
    print(b-a)
    assert res1 == res2, res1

test_bucket_sort()

