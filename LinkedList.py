class DSAListNode:
    def __init__(self, inValue):
        self.value = inValue
        self.next = None
        self.prev = None
    
    def getValue(self):
        return self.value

    def setValue(self, inValue):
        self.value = inValue
    
    def getNext(self):
        return self.next
    
    def setNext(self, newNext):
        self.next = newNext
    
    def getPrev(self):
        return self.prev
    
    def setPrev(self, newPrev):
        self.prev = newPrev


class DSALinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def isEmpty(self):
        return self.head is None
    
    def insertFirst(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd
            self.tail = newNd

        else:
            newNd.setNext(self.head)
            self.head.setPrev(newNd)
            self.head = newNd
    
    def insertLast(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd
            self.tail = newNd
        else:
            self.tail.setNext(newNd)
            newNd.setPrev(self.tail)
            self.tail = newNd
    
    def peekFirst(self):
        if self.isEmpty():
            raise Exception("List is empty")
        return self.head.getValue()
    
    def peekLast(self):
        if self.isEmpty():
            raise Exception("List is empty")
        return self.tail.getValue()
    
    def removeFirst(self):
        if self.isEmpty():
            raise Exception("List is empty")
        
        nodeValue = self.head.getValue()

        if self.head.getNext() is None:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.getNext()
            self.head.setPrev(None)
        
        return nodeValue
    
    def removeLast(self):
        if self.isEmpty():
            raise Exception("List is empty")
        
        nodeValue = self.tail.getValue()
        if self.head.getNext() is None:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.getPrev()
            self.tail.setNext(None)
        
        return nodeValue
    
    def display(self):
        currNd = self.head
        while currNd is not None:
            print(currNd.getValue(), end=" ")
            currNd = currNd.getNext()
        print()

class DSAStack:
    # Reference: 21522611_COMP5008_Prac03.ipynb
    def __init__(self):
        self.list = DSALinkedList()
    
    def push(self, value):
        self.list.insertFirst(value)
    
    def pop(self):
        return self.list.removeFirst()
    
    def top(self):
        return self.list.peekFirst()
    
    def isEmpty(self):
        return self.list.isEmpty()
    
    def display(self):
        print("Stack contents:")
        self.list.display()

class DSAQueue:
    # Reference: 21522611_COMP5008_Prac03.ipynb
    def __init__(self):
        self.list = DSALinkedList()
    
    def enqueue(self,value):
        self.list.insertLast(value)
    
    def dequeue(self):
        return self.list.removeFirst()
    
    def peek(self):
        return self.list.peekFirst()
    
    def isEmpty(self):
        return self.list.isEmpty()
    
    def display(self):
        print("Queue contents:")
        self.list.display()

class PQNode:
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority

class PriorityQueue:
    def __init__(self):
        self.list = DSALinkedList()
    
    def isEmpty(self):
        return self.list.isEmpty()
    
    def enqueue(self, item, priority):
        newNode = PQNode(item, priority)
        # Insert in order (lowest priority first)
        dsaNode = DSAListNode(newNode)
        if self.list.isEmpty():
            self.list.insertFirst(newNode)
            return
        curr = self.list.head
        prev = None
        while curr is not None and curr.getValue().priority <= priority:
            prev = curr
            curr = curr.getNext()
        if prev is None:
            dsaNode.setNext(self.list.head)
            self.list.head = dsaNode
            if self.list.tail is None:
                self.list.tail = dsaNode
        else:
            dsaNode.setNext(curr)
            prev.setNext(dsaNode)
            if dsaNode.getNext() is None:
                self.list.tail = dsaNode
    
    def dequeue(self):
        if self.list.isEmpty():
            raise Exception("PriorityQueue is empty")
        pqNode = self.list.removeFirst()
        return pqNode.item, pqNode.priority
