# Chapter 5: Probablistic Analysis and Randomized Algorithms

Just some notes i made to myself when reading this chapter

Task 5.1.1: If we assume to know if a new element is better than the current max do we then know a total order?
Since we assume this algorithm will work for all permutations of candidates, we can pick for each tuple of candidates i,j a permutation where the first candidate is i and the second is j. We take the first one i as best and then assume in the first iteration of the loop that we know if the second (j) is better than best (i). So we know pairwise order and we assume "knowing if better" follows the total order 3 assumptions.

5.1.2: Running time of Random(a,b) by calling random(0,1)
We call random(0,1) repeatedly if the number is bigger then 1/(b-a-i) then chose i. This should give equal probability to
all numbers from a to b. We ignore edge cases +- 1 depending on if interval close open half.
we need to definetly make one call:
1 + (b-a-1)/(b-a) + (b-a-2)/(b-a-1) + ... 2/1
= 1 + (1 - 1/(b-a)) ...
=(b-a-1) - sum over 1/i 
which O(b-a) - O(ln(b-a)) #harmonic series
i think total just O(b-a) 

5.1.3 get 0 or 1 with equal probability by just calling a random number generator that creates a 1 with probability p and 0 with probability (1-p).

I think if p is a rational number than it can be represented as a/b. Then calling biased_random b times and summing the results.
The sum should be bigger than a with probability 1/2 and smaller equal than a with 1/2.
no clue about irrational p. I skip the proof, its probably using geometric series. Since im more practical now i would just implement and see if it gives kind of the same amount of 0 and 1 after 10000 runs.


5.2.1 probability to hire exaclty once, prob of hiring everytime.
hiring once only happens the first one is the maximum. 1/n.
Hiring everytime happens only if its increasing sorted, since no are same this should be only one permutation. 1/n!

5.2.2 probabilty to hire exactly twice:
First candidate always hired, for each i probabilty that the candidate is hired is 1/i and then all other need to not be hired (j-1)/j. Simplify somehow.
sum 1/i * (n-1)!/(n!) * (i)/(i-1) = 1/(n * (i-1))
= 1/n * (sum 1/i)

5.2.3 expected value sum of n dice
Xi is dice i. X= X_1 + ...+X_n
E[X] = sum E[X_i]
one dice
E[X_i] = 1E[X_i == 1] + 2* ...
= 1 * 1/6 + 2* 1/6 + ...
= ((1+6) + (2+5) + (3+4)) /6
= 3 * 7 /6 = 3.5
E[X] = 3.5n

5.2.4 hat check problem. People give their hat to some place and then get it at random order back. How many get correct hat.
First person gets back hat with probability 1/n, next 1/(n-1) and so on.
X_i is person i gets hat back
X = sum X_i
get correct hat if no one before took it:
E[X_i] = E[Indicator[hat == i]] = E[ 1/i * (n-1)/n * (n-2)/(n-1).. (i-1)/i] = E[1/i * (i-1)/n]
E[X] = sum 1/i * (i-1)/n = 1/n sum (i-1/i) we had this before

5.2.5) expected number of inversions in an array A[i] > A[j] for i<j.
first one has probablit (n-1)/2 inversions, next (n-2)/2. So i guess n * (n-1) /2 * 1/2.

I dont want to spend to many times on the details i did similar things before.

Randomly shuffle the input before the algorithm when you don't know anyhting about the distribution. Then its very unlikely that you hit the worst permutation while before it might have been likely on how you got the data.