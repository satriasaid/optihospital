from Graph import * # Source: 21522611_COMP5008_Prac06
from LinkedList import * # Source: 21522611_COMP5008_Prac04

# create a new class that enable us to add weight to the graph
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

# dictionary like data structure
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
        key_list = DSALinkedList()
        curr = self.ll.head
        while curr is not None:
            key_list.insertLast(curr.getValue().key)
            curr = curr.getNext()
        return key_list