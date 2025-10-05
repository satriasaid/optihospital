from LinkedList import *

class DSAGraphNode:
    def __init__(self, inLabel):
        self.label = inLabel
        self.links = DSALinkedList()
        self.visited = False
    
    def addLink(self, otherNode):
        curr = self.links.head
        notPresent = True
        while curr is not None:
            if curr.getValue() == otherNode:
                notPresent = False
                break
            curr = curr.getNext()
        if notPresent:
            self.links.insertLast(otherNode)
    
    def getLabel(self):
        return self.label
    
    def getLinks(self):
        return self.links
    
    def setVisited(self, value):
        self.visited = value
    
    def getVisited(self):
        return self.visited
    
class DSAGraph:
    def __init__(self):
        self.vertices = DSALinkedList()
    
    def addVertex(self, newLabel):
        if self.getVertex(newLabel) is None:
            node = DSAGraphNode(newLabel)
            self.vertices.insertLast(node)
    
    def deleteVertex(self, label):
        curr = self.vertices.head
        prev = None
        foundNode = None
        while curr.getValue().getLabel() == label:
            foundNode = curr.getValue()
            if prev is None:
                self.vertices.head = curr.getNext()
                if self.vertices.tail == curr:
                    self.vertices.tail = None
            else:
                prev.setNext(curr.getNext())
                if self.vertices.tail == curr:
                    self.vertices.tail = prev
            break
        prev = curr
        curr = curr.getNext()

        if foundNode is not None:
            curr = self.vertices.head
            while curr is not None:
                node = curr.getValue()
                self._removeLink(node.links, foundNode)
                curr = curr.getNext()
            print("Vertex", label, "deleted.")
        else:
            print("Vertex", label, "not found.")
    
    def deleteEdge(self, label1, label2):
        node1 = self.getVertex(label1)
        node2 = self.getVertex(label2)
        if node1 is not None and node2 is not None:
            self._removeLink(node1.links, node2)
            self._removeLink(node2.links, node1)
            print(f"Edge between {label1} and {label2} deleted.")
        else:
            print("Vertices for the edge not found")
    
    def _removeLink(self, adjList, targetNode):
        curr = adjList.head
        prev = None
        while curr is not None:
            if curr.getValue() == targetNode:
                if prev is None:
                    adjList.head = curr.getNext()
                    if adjList.tail == curr:
                        adjList.tail = None
                else:
                    prev.setNext(curr.getNext())
                    if adjList.tail == curr:
                        adjList.tail = prev
            break
        prev = curr
        curr = curr.getNext()
            
    
    def getVertex(self, label):
        curr = self.vertices.head
        while curr is not None:
            if curr.getValue().getLabel() == label:
                return curr.getValue()
            curr = curr.getNext()
        return None

    def addEdge(self, label1, label2):
        node1 = self.getVertex(label1)
        node2 = self.getVertex(label2)
        if node1 is None or node2 is None:
            raise Exception("One or both vertices do not exist!")
        node1.addLink(node2)
        node2.addLink(node1)
    
    def displayAsList(self):
        curr = self.vertices.head
        while curr is not None:
            node = curr.getValue()
            print(node.getLabel(), end=": ")

            sortedLinks = DSALinkedList()
            lCurr = node.links.head
            while lCurr is not None:
                label = lCurr.getValue().getLabel()
                sortPtr = sortedLinks.head
                prevPtr = None
                inserted = False
                while sortPtr is not None and label > sortPtr.getValue():
                    prevPtr = sortPtr
                    sortPtr = sortPtr.getNext()
                newNd = DSAListNode(label)
                if prevPtr is None:
                    newNd.setNext(sortedLinks.head)
                    sortedLinks.head = newNd
                    if sortedLinks.tail is None:
                        sortedLinks.tail = newNd
                else:
                    newNd.setNext(prevPtr.getNext())
                    prevPtr.setNext(newNd)
                    if newNd.getNext() is None:
                        sortedLinks.tail = newNd
                lCurr = lCurr.getNext()
            linkCurr = sortedLinks.head
            while linkCurr is not None:
                print(linkCurr.getValue(), end=" ")
                linkCurr = linkCurr.getNext()
            print()
            curr = curr.getNext()
    
    def displayAsMatrix(self):
        sortedLabels = DSALinkedList()
        curr = self.vertices.head
        while curr is not None:
            label = curr.getValue().getLabel()
            sortPtr = sortedLabels.head
            prevPtr = None
            while sortPtr is not None and label > sortPtr.getValue():
                prevPtr = sortPtr
                sortPtr = sortPtr.getNext()
            newNd = DSAListNode(label)
            if prevPtr is None:
                newNd.setNext(sortedLabels.head)
                sortedLabels.head = newNd
                if sortedLabels.tail is None:
                    sortedLabels.tail = newNd
            else:
                newNd.setNext(prevPtr.getNext())
                prevPtr.setNext(newNd)
                if newNd.getNext() is None:
                    sortedLabels.tail = newNd
            curr = curr.getNext()

        col_width = 2
        header = " " * col_width
        scurr = sortedLabels.head
        while scurr is not None:
            header += f"{scurr.getValue():>{col_width}}"
            scurr = scurr.getNext()
        print(header)
        
        rowcurr = sortedLabels.head
        while rowcurr is not None:
            row_str = f"{rowcurr.getValue():>{col_width}}"
            node = self.getVertex(rowcurr.getValue())
            colcurr = sortedLabels.head
            while colcurr is not None:
                found = 0
                lCurr = node.links.head
                while lCurr is not None:
                    if lCurr.getValue().getLabel() == colcurr.getValue():
                        found = 1
                        break
                    lCurr = lCurr.getNext()
                row_str += f"{found:>{col_width}}"
                colcurr = colcurr.getNext()
            print(row_str)
            rowcurr = rowcurr.getNext()
    
    def clearVisited(self):
        curr = self.vertices.head
        while curr is not None:
            curr.getValue().setVisited(False)
            curr = curr.getNext()
    
    def breadthFirstSearch(self, startLabel):
        self.clearVisited()
        node = self.getVertex(startLabel)
        q = DSAQueue()
        result = DSALinkedList()
        node.setVisited(True)
        q.enqueue(node)
        while not q.isEmpty():
            current = q.dequeue()
            result.insertLast(current.getLabel())
            sortedNeighbors = DSALinkedList()
            lCurr = current.links.head
            while lCurr is not None:
                nbr = lCurr.getValue()
                if not nbr.getVisited():
                    label = nbr.getLabel()
                    sn_curr = sortedNeighbors.head
                    sn_prev = None
                    inserted = False
                    while sn_curr is not None and label > sn_curr.getValue().getLabel():
                        sn_prev = sn_curr
                        sn_curr = sn_curr.getNext()
                    newNode = DSAListNode(nbr)
                    if sn_prev is None:
                        newNode.setNext(sortedNeighbors.head)
                        sortedNeighbors.head = newNode
                        if sortedNeighbors.tail is None:
                            sortedNeighbors.tail = newNode
                    else:
                        newNode.setNext(sn_prev.getNext())
                        sn_prev.setNext(newNode)
                        if newNode.getNext() is None:
                            sortedNeighbors.tail = newNode
                lCurr = lCurr.getNext()
            
            currSorted = sortedNeighbors.head
            while currSorted is not None:
                currSorted.getValue().setVisited(True)
                q.enqueue(currSorted.getValue())
                currSorted = currSorted.getNext()
        
        outcurr = result.head
        outlabels = ""
        while outcurr is not None:
            outlabels += outcurr.getValue() + " "
            outcurr = outcurr.getNext()
        print("BFS order:", outlabels.strip())
    
    def dfsRecursive(self, node, result):
        result.insertLast(node.getLabel())
        node.setVisited(True)
        sortedNeighbors = DSALinkedList()
        lCurr = node.links.head
        while lCurr is not None:
            nbr = lCurr.getValue()
            label = nbr.getLabel()
            sn_curr = sortedNeighbors.head
            sn_prev = None
            while sn_curr is not None and label > sn_curr.getValue().getLabel():
                sn_prev = sn_curr
                sn_curr = sn_curr.getNext()
            newNode = DSAListNode(nbr)
            if sn_prev is None:
                newNode.setNext(sortedNeighbors.head)
                sortedNeighbors.head = newNode
                if sortedNeighbors.tail is None:
                    sortedNeighbors.tail = newNode
            else:
                newNode.setNext(sn_prev.getNext())
                sn_prev.setNext(newNode)
                if newNode.getNext() is None:
                    sortedNeighbors.tail = newNode
            lCurr = lCurr.getNext()
        currSorted = sortedNeighbors.head
        while currSorted is not None:
            nbr = currSorted.getValue()
            if not nbr.getVisited():
                self.dfsRecursive(nbr, result)
            currSorted = currSorted.getNext()

    def depthFirstSearch(self, startLabel):
        self.clearVisited()
        node = self.getVertex(startLabel)
        result = DSALinkedList()
        self.dfsRecursive(node, result)
        outcurr = result.head
        outlabels = ""
        while outcurr is not None:
            outlabels += outcurr.getValue() + " "
            outcurr = outcurr.getNext()
        print("DFS order:", outlabels.strip())