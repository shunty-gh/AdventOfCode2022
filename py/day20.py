import os

# https://adventofcode.com/2022/day/20 - Day 20: Grove Positioning System

# Probably could be quicker with a bit more thought and tracking the head/next item
# index a bit better when mixing but it runs in under a minute on my machine.
#
# Turns out it could be a lot easier than here by just doing array deletes and inserts.
# See the C# version at ../cs/days/day20.cs or https://github.com/shunty-gh/AdventOfCode2022/blob/main/cs/days/day20.cs

class Node:
    def __init__(self, value: int):
        self.previous: Node | None = None
        self.data = value
        self.next: Node | None = None
        self.index: int = 0

class CircularList:
    def __init__(self, data: list[int] = [], mult: int = 1):
        self.head: Node | None = None
        self.zero: Node | None = None
        self.len: int = 0
        self.indexes: dict[int, Node] = {}
        if len(data) > 0:
            self.add_range(data, mult)

    def add(self, value: int) -> Node:
        """ Add/insert a new node before the head of the list (ie at the 'end' of the list, even though it's circular) """
        nd = Node(value)
        if self.head == None:
            self.head = nd
            nd.next = nd
            nd.previous = nd
        else:
            nd.previous = self.head.previous
            nd.next = self.head
            if self.head.previous:
                hp = self.head.previous
                hp.next = nd
            self.head.previous = nd

        self.len += 1
        if value == 0:
            self.zero = nd
        return nd

    def add_range(self, data: list[int], mult: int = 1):
        """ Add a collection of values to the list """
        for i,item in enumerate(data):
            nd = self.add(item * mult)
            nd.index = i
            self.indexes[nd.index] = nd

    def mix(self):
        """ Do the magic mixing of values """
        if self.head == None:
            raise KeyError("Invalid list")
        n = self.head
        while n != None:
            ix = n.index
            self._mix_node(n)
            # find the next node to mix
            n = self._find_index(ix+1)
            if n == None:
                break

    def grove_coords(self) -> tuple[int,int,int]:
        z = self.zero
        if z == None or z.next == None:
            raise KeyError("Invalid list")

        result: list[int] = []
        for i in [1000, 2000, 3000]:
            mv = i % self.len
            n = z
            for _ in range(mv):
                if n.next == None:
                    raise KeyError("Invalid list")
                n = n.next
            result.append(n.data)
        return tuple(result[:3])

    def _mix_node(self, nd: Node):
        v = nd.data % (self.len - 1)
        for _ in range(v):
            self._move_node_forward(nd)

    def _move_node_forward(self, nd: Node):
        """ Swap the pointers around to move a node one step forward """
        if nd.next == None or nd.previous == None:
            raise KeyError("Invalid list")

        tmpP = nd.previous
        tmpN = nd.next

        tmpP.next = tmpN
        tmpN.previous = tmpP
        nd.previous = tmpN
        nd.next = tmpN.next
        tmpN.next = nd
        if nd.next:
            nd.next.previous = nd

    def _find_index(self, index: int) -> Node | None:
        # Look in the 'cache' first. Doesn't speed it up as much as I expected.
        if index in self.indexes:
            return self.indexes[index]

        next = self.head
        start = next
        while next != None and next.index != index:
            next = next.next
            if next == start:
                return None
        if next == None:
            raise KeyError("Invalid list")
        return next

    def print(self):
        n = self.head
        if n == None:
            print("No entries")
            return
        done = False
        while n != None and not done:
            ln = ''
            for i in range(50):
                ln += str(n.data) + ','
                n = n.next
                if n == self.head:
                    done = True
                    break
                if n == None:
                    raise KeyError("Invalid list")
            print(ln)


#data = [int(i) for i in "1\n2\n-3\n3\n-2\n0\n4".splitlines()]   # Expect P1: 3; P2: 1623178306
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day20-input", "r") as f:
    data = [int(line.strip()) for line in f.readlines()]

lst1 = CircularList(data)
lst1.mix()
print("Part 1: ", sum(lst1.grove_coords()))

decryption_key = 811589153
lst2 = CircularList(data, decryption_key)
for i in range(10):
    lst2.mix()
print("Part 2: ", sum(lst2.grove_coords()))
