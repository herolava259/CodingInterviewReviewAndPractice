from typing import List
import math
from typing import Optional

'''
Problem Statement	
In meteorology, a common statistical tool is the median of a given set of measurements. (You can find a definition of 
the median in the Notes section.)

You are writing software for a device that measures temperature once a second. The device has a small digital display. 
At any moment, the display has to show the median of temperatures measured in the last K seconds.

Before you upload your software into the device, you would like to test it on a computer.

Instead of measuring temperatures, we will use a random number generator (RNG) to generate fake temperatures. Given 
three ints seed, mul and add, we define a sequence of temperatures:

t0 = seed
tk+1 = (tk * mul + add) mod 65536
In addition to the parameters of the RNG, you will be given two ints N and K.

Consider the sequence containing the first N temperatures generated by the RNG (i.e., values t0 to tN-1). This sequence 
has N-K+1 contiguous subsequences of length K. For each such subsequence compute its median.

Your method will be given the numbers seed, mul, add, N, and K. Compute all the medians as described above, and return 
a long containing their sum.

 
Definition
    
Class:	FloatingMedian
Method:	sumOfMedians
Parameters:	int, int, int, int, int
Returns:	long
Method signature:	long sumOfMedians(int seed, int mul, int add, int N, int K)
(be sure your method is public)
    
 
Notes
-	Given K numbers, their median is the ((K+1)/2)-th smallest of them, rounding down for even K, and indexing from 1.

For example, the median of (1, 2, 6, 5, 4, 3) is 3, and the median of (11, 13, 12, 14, 15) is 13.
 
Constraints
-	seed, mul, and add are between 0 and 65535, inclusive.
-	N is between 1 and 250,000, inclusive.
-	K is between 1 and 5,000, inclusive.
-	N is greater than or equal to K.
 
Examples
0)	
    
3
1
1
10
3
Returns: 60
The generated temperatures are: 3, 4, 5, 6, 7, 8, 9, 10, 11, and 12.

The length-3 contiguous subsequences are (3, 4, 5), (4, 5, 6), ..., and (10, 11, 12).

Their medians are 4, 5, ..., 11.

The sum of these medians is 4+5+...+11 = 60.
1)	
    	
10
0
13
5
2
Returns: 49
This time the generated temperatures are 10, 13, 13, 13, and 13. The medians you should compute are 10, 13, 13, and 13.
2)	
    	
4123
2341
1231
7
3
Returns: 102186
Generated temperatures: 4123, 19382, 23581, 23040, 1743, 18362, 60593.
3)	
    	
47
5621
1
125000
1700
Returns: 4040137193
A quite large random test case.
4)	
    	
32321
46543
32552
17
17
Returns: 25569
Watch out for integer overflow when generating the temperatures.

'''
mod_k = 65536


class RandomNumberGenerator:
    def __init__(self, n: int, seed: int, mul: int, add: int):
        self.n = n
        self.seed = seed
        self.mul = mul
        self.add = add
        self.curr = seed % mod_k
        self.i = 0

    def __len__(self):
        return self.n

    def reset(self):
        self.i = 0
        self.curr = self.seed

    def __next__(self) -> int:
        res = self.curr
        if self.i < self.n:
            self.curr = (self.curr * self.mul + self.add) % mod_k
            self.i += 1
        else:
            self.reset()
            res = self.seed
        return res

    def __getitem__(self, item):

        mul_pow = 1
        sig_add = 0
        if item > 0:
            for i in range(item - 1):
                sig_add = (sig_add + mul_pow) % mod_k
                mul_pow = (mul_pow * self.mul) % mod_k
            sig_add = (sig_add * self.add) % mod_k
        res = (self.seed * mul_pow) % mod_k
        res = (res + sig_add) % mod_k

        return res

    def is_end(self) -> bool:
        return self.i == self.n

    def __iter__(self):

        curr = self.seed
        for i in range(self.n):
            yield curr
            curr = (curr * self.mul + self.add) % mod_k


def find_median(arr: List[int]):
    return find_element_pos_k(arr, ((len(arr) + 1) // 2) - 1)


def find_pos(arr: List[int], pivot: int = 0) -> tuple:
    pivot_val = arr[pivot]
    counter = 0
    left: List[int] = []
    right: List[int] = []

    for i in range(len(arr)):
        if i == pivot:
            continue
        if pivot_val >= arr[i]:
            counter += 1
            left.append(arr[i])
        else:
            right.append(arr[i])

    return counter, left, right


def find_element_pos_k(arr: List[int], kth: int) -> tuple:
    if len(arr) == 1:
        return arr[0], 0
    pos, left_arr, right_arr = find_pos(arr)

    if pos == kth:
        return arr[0], pos
    if pos > kth:
        return find_element_pos_k(left_arr, kth)
    return find_element_pos_k(right_arr, kth - pos - 1)


class Node:
    def __init__(self, val: int, eid: int, nid: int, prev_node: Optional['Node'] = None,
                 next_node: Optional['Node'] = None):
        self.value = val
        self.eid = eid
        self.nid = nid
        self.prev_node: Optional['Node'] = prev_node
        self.next_node: Optional['Node'] = next_node


def insert_node(new_node: Node, median_node: Node) -> bool:

    if new_node.value < median_node.value:
        after_node = median_node
        while after_node.prev_node is not None and after_node.prev_node.value > new_node.value:
            after_node = after_node.prev_node

        if after_node.prev_node is not None:
            new_node.prev_node = after_node.prev_node
            after_node.prev_node.next_node = new_node
        else:
            new_node.prev_node = None
        new_node.next_node = after_node
        after_node.prev_node = new_node

        return True

    if new_node.value >= median_node.value:
        before_node = median_node
        while before_node.next_node is not None and before_node.next_node.value <= new_node.value:
            before_node = before_node.next_node

        if before_node.next_node is not None:
            new_node.next_node = before_node.next_node
            before_node.next_node.prev_node = new_node
        else:
            # case new_node is tail of linked list
            new_node.next_node = None

        before_node.next_node = new_node
        new_node.prev_node = before_node
        return True

    return False


class SortedLinkedList:
    def __init__(self, k: int, rng: RandomNumberGenerator):
        self.k: int = k
        self.nodes_map: List[Node] = []
        self.head_id: int = 0
        self.tail_id: int = 0
        self.median_id: int = 0
        self.first_id: int = 0
        self.rng: RandomNumberGenerator = rng

    def build(self):
        arr: List[int] = []
        counter = 0
        self.rng.reset()
        while counter <= self.k:
            arr.append(next(self.rng))
        sorted_arr = [(i, val) for i, val in enumerate(arr)]
        sorted_arr.sort(key=lambda c: c[1])
        curr_node: Node | None = None

        for i, item in enumerate(sorted_arr):
            eid, val = item
            prev_node = curr_node
            curr_node = Node(val, eid, i, prev_node, None, )
            prev_node.next_node = curr_node
            self.nodes_map.append(curr_node)

            if eid == 0:
                self.first_id = i

        self.head_id = 0
        self.tail_id = self.k - 1
        self.median_id = (self.k - 1) // 2

    def get_median(self) -> tuple:
        median_node = self.nodes_map[self.median_id]

        return median_node.eid, median_node.value

    def next_window(self):

        # cutting old node

        deleted_node = self.erase_first_val()
        median_node = self.nodes_map[self.median_id]
        # find median of k-1 sorted nodes base on median node of k sorted node before
        if deleted_node.value == median_node.value and deleted_node.nid == median_node.nid:
            if self.k % 2 == 0:
                median_node = median_node.next_node
            else:
                median_node = median_node.prev_node
        elif deleted_node.value < median_node.value:
            if self.k % 2 == 0:
                median_node = median_node.next_node
        elif deleted_node.value >= median_node.value:
            if self.k % 2 == 1:
                median_node = median_node.prev_node

        self.median_id = median_node.nid

        # init new node
        eid: int = self.rng.i
        new_val = next(self.rng)
        new_node = median_node
        new_node.eid = eid
        new_node.value = new_val
        # insert_node
        insert_node(new_node, median_node)

        # re-calc median node
        insert_after: bool = new_node.value >= median_node.value
        self.median_id = self.calc_median(insert_after)

    def calc_median(self, insert_after: bool = True) -> int:

        median_id = self.median_id
        if insert_after and self.k % 2 == 0:
            median_id = self.nodes_map[median_id].next_node.nid

        if not insert_after and self.k % 2 == 1:
            median_id = self.nodes_map[median_id].prev_node.nid

        return median_id

    def erase_first_val(self) -> Node:
        self.cutting_node(self.first_id)
        return self.nodes_map[self.first_id]

    def cutting_node(self, nid: int):

        curr_node = self.nodes_map[nid]
        prev_node = curr_node.prev_node
        next_node = curr_node.next_node

        prev_node.next_node = next_node
        next_node.prev_node = prev_node

        curr_node.prev_node = None
        curr_node.next_node = None


class FloatingMedianSolution:
    def __init__(self, seed: int, mul: int, add: int, n: int, k: int):
        self.seed = seed
        self.mul = mul
        self.add = add
        self.n = n
        self.k = k
        self.rng = RandomNumberGenerator(n, seed, mul, add)
        self.window = SortedLinkedList(k, self.rng)

    def solve_by_linked_list(self):
        self.window.build()
        res = 0

        for _ in range(0, self.n - self.k + 1):
            median_id, median_val = self.window.get_median()

            res = (res + median_val) % mod_k

            self.window.next_window()

        return res

