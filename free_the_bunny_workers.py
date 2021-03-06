### level 4 - 1/2 ###
"""
Free the Bunny Workers
======================

You need to free the bunny workers before Commander Lambda's space station explodes! Unfortunately, the Commander was very careful with the highest-value workers -- they all work in separate, maximum-security work rooms. The rooms are opened by putting keys into each console, then pressing the open button on each console simultaneously. When the open button is pressed, each key opens its corresponding lock on the work room. So, the union of the keys in all of the consoles must be all of the keys. The scheme may require multiple copies of one key given to different minions.

The consoles are far enough apart that a separate minion is needed for each one. Fortunately, you have already relieved some bunnies to aid you - and even better, you were able to steal the keys while you were working as Commander Lambda's assistant. The problem is, you don't know which keys to use at which consoles. The consoles are programmed to know which keys each minion had, to prevent someone from just stealing all of the keys and using them blindly. There are signs by the consoles saying how many minions had some keys for the set of consoles. You suspect that Commander Lambda has a systematic way to decide which keys to give to each minion such that they could use the consoles.

You need to figure out the scheme that Commander Lambda used to distribute the keys. You know how many minions had keys, and how many consoles are by each work room.  You know that Command Lambda wouldn't issue more keys than necessary (beyond what the key distribution scheme requires), and that you need as many bunnies with keys as there are consoles to open the work room.

Given the number of bunnies available and the number of locks required to open a work room, write a function solution(num_buns, num_required) which returns a specification of how to distribute the keys such that any num_required bunnies can open the locks, but no group of (num_required - 1) bunnies can.

Each lock is numbered starting from 0. The keys are numbered the same as the lock they open (so for a duplicate key, the number will repeat, since it opens the same lock). For a given bunny, the keys they get is represented as a sorted list of the numbers for the keys. To cover all of the bunnies, the final solution is represented by a sorted list of each individual bunny's list of keys.  Find the lexicographically least such key distribution - that is, the first bunny should have keys sequentially starting from 0.

num_buns will always be between 1 and 9, and num_required will always be between 0 and 9 (both inclusive).  For example, if you had 3 bunnies and required only 1 of them to open the cell, you would give each bunny the same key such that any of the 3 of them would be able to open it, like so:
[
  [0],
  [0],
  [0],
]
If you had 2 bunnies and required both of them to open the cell, they would receive different keys (otherwise they wouldn't both actually be required), and your solution would be as follows:
[
  [0],
  [1],
]
Finally, if you had 3 bunnies and required 2 of them to open the cell, then any 2 of the 3 bunnies should have all of the keys necessary to open the cell, but no single bunny would be able to do it.  Thus, the solution would be:
[
  [0, 1],
  [0, 2],
  [1, 2],
]

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(2, 1)
Output:
    [[0], [0]]

Input:
solution.solution(4, 4)
Output:
    [[0], [1], [2], [3]]

Input:
solution.solution(5, 3)
Output:
    [[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]]
"""
def C(n, m):
    from functools import reduce
    prod = lambda x, y: x*y
    m = max(m, n-m)
    numerator = reduce(prod, range(m+1, n+1), 1)
    denominator = reduce(prod, range(1, n-m+1), 1)
    return numerator/denominator

def choose_bits(n, b, d):
    from collections import deque
    def getChildren(node):
        children = list()
        b_str = bin(node)[2:]
        b_str = '0'*(b-len(b_str)) + b_str
        for idx, c in enumerate(b_str):
            if idx == len(b_str)-1: break
            if c == '1' and b_str[idx+1] == '0':
                rev_child = bin(int(b_str[::-1],2) + (1<<idx))[-1:1:-1]
                child = int(rev_child + '0'*(b-len(rev_child)), 2)
                children.append(child)
        return children
    root = int('1'*d+'0'*(b-d), 2)
    q = deque()
    q.append(root)
    children = {root: list()}
    parents = dict()
    visited = dict()
    while q:
        cur = q.popleft()
        for child in getChildren(cur):
            if not visited.get(child, False):
                q.append(child)
                visited[child] = True
            children[cur].append(child)
            children[child] = children.get(child, list())
            parents[child] = parents.get(child, list())
            parents[child].append(cur)
    #### purge tree - for child with more than 1 parent, only keep left-most parent
    for child, parentList in parents.items():
        for parent in parentList[1:]:
            children[parent].remove(child)
        parents[child] = parentList[:1]
    #### pre-order traversal but iterate children from right to left (mirrored tree)
    s = list()
    path = list()
    s.append(root)
    while s:
        cur = s.pop()
        b_str = bin(cur)[2:]
        b_str = '0'*(b-len(b_str)) + b_str
        path.append([int(c) for c in b_str])
        for child in children[cur]:
            s.append(child)
    return path
def bits_to_buns(bits):
    n = len(bits)
    b = len(bits[0])
    buns = list()
    for i in range(b):
        bun = list()
        for j in range(n):
            if bits[j][i]:
                bun.append(j)
        buns.append(bun)
    return buns

def solution(b, m):
    n, e = C(b, m-1), C(b-1, m-1) # n is total number of keys, e is the number of keys each bunny must have
    d = b-m+1 # d is the number of duplicates each unique key must have
    assert(n*d == b*e)
    bits = choose_bits(n, b, d)
    res = bits_to_buns(bits)
    res = [sorted(a) for a in res]
    return sorted(res)

### verification ###
def set_union(ss):
    u = set()
    for subset in ss:
        u = u.union(set(subset))
    return u
def verify(sol, m):
    import itertools
    def findsubsets(s, n):
        return list(itertools.combinations(s, n))
    keys = set_union(sol)
    # print("Set of keys:")
    # print(keys)
    ### dk can
    subsets = findsubsets(sol, m)
    u = [set_union(subset) for subset in subsets]
    c = min(u, key=lambda x: len(x))
    # print("Subset of m = {0}".format(m))
    # print(c)
    ### dk du
    subsets = findsubsets(sol, m-1)
    # for subset in subsets:
    #     print(subset)
    u = [set_union(subset) for subset in subsets]
    d = max(u, key=lambda x: len(x))
    return (len(keys) == len(c) and (len(d) < len(c)))
    # print("Subset of m-1 = {0}".format(m-1))
    # print(c)

if __name__=='__main__':
    tests = [
        [2,1], [2,2],
        [3,1],
        [3,2],
        [4,2],
        [4,3], [4,4],
        [5,3],
        [6,5]
    ]
    for t in tests:
        print(t)
        sol = solution(*t)
        # print(sol)
        if verify(sol, t[1]):
            print('CORRECT')
        else: print('FALSE')
        print('')

'''
Given set U of size n, and an integer m. Construct b subsets of size e. Call the set of subsets B. B has to satify these constraints:
    (i) union of any m subsets (in B) equals U
    (ii) union of any m-1 subsets (in B) is less than U
E.g. U = {0, 1, 2}, n=3, m=2, b=3, e=2. One of such B is:
{
    {0,1},
    {0,2},
    {1,2}
}
Some of the characteristics deduced from the constraints:
    (i) Let d be the number of times an element of U appear in any element of B, we have d = b-m+1
    (ii) Any 2 elements in B (subset of U) is as similar as possible but never be equal
'''