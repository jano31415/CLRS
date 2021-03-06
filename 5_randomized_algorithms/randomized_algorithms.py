from random import randint


# this makes a lot of sense to me since ever number has the same probability
# to go to the first position and then can not be swapped away. Then you go to
# the next position and again every number which that wasnt chosen has the same probability
# to go there independent of which numbers have been chosen. And so on. So this
# should be uniformly random
def random_shuffle(arr):
    len_arr = len(arr)
    for i in range(len_arr):
        swap(arr, i, randint(i, len_arr - 1))
    return arr


# probably works but harder to prove. Dont want to spend too much time on proves
# im here to code and not to think
def random_shuffle_all(arr):
    len_arr = len(arr)
    for i in range(len_arr):
        swap(arr, i, randint(0, len_arr - 1))
    return arr


# I think its at least easy to see that it does not have identities.
def random_shuffle_identity(arr):
    len_arr = len(arr)
    for i in range(len_arr - 1):
        swap(arr, i, randint(i + 1, len_arr - 1))
    return arr


def swap(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp


def test_swap():
    l = [1, 2, 3, 4]
    i = 0
    j = 2
    swap(l, i, j)
    assert l == [3, 2, 1, 4]

    l = [1, 2, 3, 4]
    i = 0
    j = 3
    swap(l, i, j)
    assert l == [4, 2, 3, 1]


test_swap()


# as promised i try to not think and test it. I guess it works but i will always
# use the version that i understand.
def test_uniformly():
    tot = {}
    arr = [1, 2, 3, 4]
    len_array = len(arr)
    tot = {(a, b): 0 for a in range(len_array) for b in range(len_array)}
    n = 100000
    for _ in range(n):
        res = random_shuffle_all(arr)
        for j, v in enumerate(res):
            tot[(j, v - 1)] += 1
    print(tot)
    # obv this might fail
    for k, v in tot.items():
        assert v > 0.98 * n / len_array, (k, v)
        assert v < 1.02 * n / len_array, (k, v)

import time
a = time.time()
test_uniformly()
b=time.time()
print(b-a)

# 5.3.4 permuatate by shifting the array cyclically fails obviously since it does the
# not even generate all permutations but just n different ones for each offset.


#fast random sample
# why recursion, looks preety smart though. I can not fully calculate in my head.
# nr 1 has prob of 1/ (n-m+1) + (n-m)/n-m+1 * 1/(n-m+2) + (n-m)/(n-m+1) * (n-m+1)/(n-m+2) 1/(n-m+3)...
# x= (n-m)
# =x/(x*(x+1)) + x/((x+1)*(x+2)) ...+ x/(x+m)(x+m+1)
# =x (2/(x*(x+2)) + ...)
# =x*(m/(x*(x+m+1))) = m/(x+m+1) = m/(n+1) ok but i got the general proof idea.
# quite difficult to cancel this out but i can do it on a piece of paper.
# lets continue
def random_sample(m, n):
    assert m <= n
    if m == 0:
        return set()
    S = random_sample(m-1, n-1)
    i = randint(1, n)
    if i in S:
        S.add(n)
    else:
        S.add(i)
    assert len(S) == m
    return S

def random_sample_iter(m,n):
    S = set()
    n_max = n-m+1
    for _ in range(m):
        i = randint(1, n_max)
        if i in S:
            S.add(n_max)
        else:
            S.add(i)
        n_max += 1
    return S

def test_random_sample():
    m=7
    n=15
    tot = {k:0 for k in range(1,n+1)}
    for _ in range(100000):
        res = random_sample_iter(m, n)
        for k in res:
            tot[k] +=1
    print(res)
    print(tot)

a = time.time()
test_random_sample()
b = time.time()
print(b-a)

#on line hiring
# there are n candidates coming in for job interview. You need to decide if you
# want to hire and then it stops or you say no and the candidate is lost.
# test the first k and find out best score of them then hire the next candidate
# that is better. This strategy finds the best candidate if k = n/e with probability
# 1/e