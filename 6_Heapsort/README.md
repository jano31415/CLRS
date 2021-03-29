6.1) number of elements in a heap of height h.
Since it is completely filled binary tree up until bottom row. The min is when
the bottom row has 1 elements and max is if it has 2**h.
max total = 1 + 2 + 4 + ... + 2**(h-1) = 2**h - 1
max total = 1 + 2 + 4 + ... + 2**(h-2) + 1 = 2**(h-1)

6.2) 2**(h-1) <= n <= 2**h - 1
    log2(n) < h (log strictly increasing)
   ? height is natural number so round this somehow. Dont really care about +- 1

6.3) i guess follows pretty much from the max heap property that each node is
the max value of the subtree with that node as root.

6.4)
minimum of a max heap is in a leaf.

6.5)
is a sorted array a min heap.
we need to check that A[parent(i)] < A[i]
A[j] < A[2*j]
A[j] < A[2*j+1]
so yes

6.6) too much manual check.

6.7) where are the leaves in a array heap.
the leftmost leave must be 2**h, second leftmost 2**h+1.
if n > 2**(h+1) then there would be another child of 2**h.
so 2**(h+1) ~ n , 2**h kind of n/2 not sure about arrays that dont have lenght 2**k
third leave would be  (2**(h-2)+1)*2 and so on. They are all bigger than 2**h.
I guess not 100% obvious that they are distinct.
Going left is times 2 so a shift in a binary representation. going right is
shift in binary plus leftmost setting to one. So each leave can be represented
with a h long binary number first is a 1 and then everywhere a 1 where we decided
to go right. Binary representation unique and no holes.
leaves dont have to be in the bottom row. If that is not full then the end of the
last row has leaves. Which is then 2**h -1 2**h -2 and so on. So definetly the
leaves are all the last elements in the array. How many is it though?
If its full then its (n+1)/2 many leaves. 1+2+4+...+2**(h-1) = 2**(h-2)-1 + 2**(h-1)
Full tree uneven try ceil(n/2)
Take one leave then its one less, but If we take two away then the parent suddenly becomes a leaf.

6.3.3
