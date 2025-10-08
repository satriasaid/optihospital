from Graph import * # Source: 21522611_COMP5008_Prac06
from LinkedList import * # Source: 21522611_COMP5008_Prac04

class EdgeWeightNode:
    def __init__(self, nodeA, nodeB, weight):
        self.nodeA = nodeA 
        self.nodeB = nodeB
        self.weight = weight

    def matches(self, u, v):
        return (self.nodeA == u and self.nodeB == v)

class EdgeWeightList:
    def __init__(self):
        self.weights = DSALinkedList()

    def addWeight(self, u, v, w):
        self.weights.insertLast(EdgeWeightNode(u, v, w))
        self.weights.insertLast(EdgeWeightNode(v, u, w))

    def getWeight(self, u, v):
        curr = self.weights.head
        while curr is not None:
            ewNode = curr.getValue()
            if ewNode.matches(u, v):
                return ewNode.weight
            curr = curr.getNext()
        return None

class HospitalGraph(DSAGraph):
    def __init__(self):
        super().__init__()
        self.weightList = EdgeWeightList()

    def addWeightedEdge(self, label1, label2, weight):
        self.addVertex(label1)
        self.addVertex(label2)
        self.addEdge(label1, label2)
        self.weightList.addWeight(label1, label2, weight)

    def getWeight(self, label1, label2):
        return self.weightList.getWeight(label1, label2)

class MapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class DSALinkedMap:
    def __init__(self):
        self.ll = DSALinkedList()

    def set(self, key, value):
        curr = self.ll.head
        while curr is not None:
            n = curr.getValue()
            if n.key == key:
                n.value = value
                return
            curr = curr.getNext()
        self.ll.insertLast(MapNode(key, value))

    def get(self, key):
        curr = self.ll.head
        while curr is not None:
            n = curr.getValue()
            if n.key == key:
                return n.value
            curr = curr.getNext()
        return None

    def has(self, key):
        curr = self.ll.head
        while curr is not None:
            n = curr.getValue()
            if n.key == key:
                return True
            curr = curr.getNext()
        return False

    def keys(self):
        curr = self.ll.head
        while curr is not None:
            yield curr.getValue().key
            curr = curr.getNext()

def bfs_group_by_level(graph, startLabel):
    visited = DSALinkedMap()
    levels = DSALinkedMap()
    result = DSALinkedList()

    queue = DSAQueue()
    queue.enqueue(graph.getVertex(startLabel))
    visited.set(startLabel, True)
    levels.set(startLabel, 0)

    maxLevel = 0

    while not queue.isEmpty():
        currNode = queue.dequeue()
        currLabel = currNode.getLabel()
        currLevel = levels.get(currLabel)
        if currLevel > maxLevel:
            maxLevel = currLevel

        currLevelList = result.head
        levelFound = False
        levelIdx = 0
        for i in range(currLevel+1):
            if currLevelList is None:
                ll = DSALinkedList()
                result.insertLast(ll)
                currLevelList = result.tail
            currLevelList = currLevelList.getNext()

        levelList = result.head
        for i in range(currLevel):
            if levelList is not None:
                levelList = levelList.getNext()
        if levelList is not None:
            levelList.getValue().insertLast(currLabel)

        nbrs = currNode.getLinks().head
        while nbrs is not None:
            nNode = nbrs.getValue()
            nLabel = nNode.getLabel()
            if not visited.has(nLabel):
                queue.enqueue(nNode)
                visited.set(nLabel, True)
                levels.set(nLabel, currLevel+1)
            nbrs = nbrs.getNext()

    print("BFS Groups by Level (hops):")
    levelPtr = result.head
    levelIdx = 0
    while levelPtr is not None:
        print("Level", levelIdx, ":", end=" ")
        levelList = levelPtr.getValue()
        nPtr = levelList.head
        while nPtr is not None:
            print(nPtr.getValue(), end=", ")
            nPtr = nPtr.getNext()
        print()
        levelPtr = levelPtr.getNext()
        levelIdx += 1

def a_star_shortest_path(graph, weightList, src, dst):
    # Source: https://www.geeksforgeeks.org/python/a-search-algorithm-in-python/
    pq = PriorityQueue()
    dist = DSALinkedMap()
    prev = DSALinkedMap()
    pq.enqueue(src, 0)
    dist.set(src, 0)
    prev.set(src, None)

    while not pq.isEmpty():
        curr, currCost = pq.dequeue()
        currLabel = curr
        if currLabel == dst:
            break
        node = graph.getVertex(currLabel)
        nbrs = node.getLinks().head
        while nbrs is not None:
            nbrNode = nbrs.getValue()
            nbrLabel = nbrNode.getLabel()
            w = weightList.getWeight(currLabel, nbrLabel)
            alt = dist.get(currLabel) + w
            if not dist.has(nbrLabel) or alt < dist.get(nbrLabel):
                dist.set(nbrLabel, alt)
                prev.set(nbrLabel, currLabel)
                pq.enqueue(nbrLabel, alt)
            nbrs = nbrs.getNext()

    pathLL = DSALinkedList()
    crawl = dst
    if not prev.has(dst):
        print("No path found")
        return
    while crawl is not None:
        pathLL.insertFirst(crawl)
        crawl = prev.get(crawl)
    print("Shortest path from", src, "to", dst, ": ", end="")
    p = pathLL.head
    while p is not None:
        print(p.getValue(), end=", ")
        p = p.getNext()
    print("\nTotal walking time:", dist.get(dst))