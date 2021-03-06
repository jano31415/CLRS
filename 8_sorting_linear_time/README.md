proving  nlog(n) is a lower bound for comparison sort.
Idea:
a comparison based sorting algorithm is a sequence of comparisons.
The next comparison made depends on the truth values of the comparisons made before
so we can thinkg of it as a binary tree where we get to a different node depending on
the previous comparisons.
After ending at a leave a correct algorithm would know the correct sorting.
There are n! many input permutations. On each input the algorithm must finish on a leaf.
(If it never finishes then its not a correct algorithm and if its not at a leaf then its not finished)
In a binary tree there is a unique path to each leaf.
These n! leaves must be distinct because if there were two permutation ending at the
same leave then the algorithm can only return one sorting there but the permutations are different
so it can not be correct.
If this feels ok then its quite straightforward.
there are atmost 2^h many leaves in a binary tree of height h.
n! < 2^h
log2(n!) < h # this was not as obvious as thought but yeah
sum log2(k) < h
1/4 n log(n) < h

Idea this?
drop first half of logarithms, who cares. Second half is bigger than 1/4 n log(n)
1/2*log(n) < log(1/2 * n)
sqrt(n) < 1/2 n
    n < 1/4 n**2
i dont know prove by induction or somthing for big n. Idea works i guess.

book says use stirling for finding the some of ln k


Quite interesting ideas: Count sort, radix sort, bucket sort
Lot of problems at the end of the chapter that i didnt do.