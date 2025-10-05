import numpy as np

class DSAHeapEntry:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value
    
    def getPriority(self):
        return self.priority
    
    def setPriority(self, priority):
        self.priority = priority
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def __str__(self):
        return f"({self.priority}, {self.value})"
    
class DSAHeap:
    def __init__(self, maxSize):
        self.heap = np.empty(maxSize, dtype = object)
        self.count = 0
        self.maxSize = maxSize
    
    def add(self, priority, value):
        if self.count >= self.maxSize:
            raise Exception("Heap is full")

        newEntry = DSAHeapEntry(priority,value)
        self.heap[self.count] = newEntry
        self.trickleUp(self.count)
        self.count += 1
    
    def remove(self):
        if self.count == 0:
            raise Exception("Heap is empty")
        rootEntry = self.heap[0]
        self.count -= 1
        self.heap[0] = self.heap[self.count]

        if self.count > 0:
            self.trickleDown(0)
        
        return rootEntry
    
    def trickleUp(self, index):
        while index > 0:
            parentIdx = (index - 1) // 2
            if self.heap[index].getPriority() > self.heap[parentIdx].getPriority():
                temp = self.heap[parentIdx]
                self.heap[parentIdx] = self.heap[index]
                self.heap[index] = temp
                index = parentIdx
            else:
                break
    
    def trickleDown(self, index):
        leftChildIdx = (index * 2) + 1
        rightChildIdx = leftChildIdx + 1
        keepGoing = True

        while keepGoing and leftChildIdx < self.count:
            keepGoing = False
            largeIdx = leftChildIdx

            if (rightChildIdx < self.count and
                self.heap[leftChildIdx].getPriority() < self.heap[rightChildIdx].getPriority()):
                largeIdx = rightChildIdx
            
            if self.heap[largeIdx].getPriority() > self.heap[index].getPriority():
                temp = self.heap[largeIdx]
                self.heap[largeIdx] = self.heap[index]
                self.heap[index] = temp

                keepGoing = True
                index = largeIdx
                leftChildIdx = (index * 2) + 1
                rightChildIdx = leftChildIdx + 1
    
    def display(self):
        print("Heap contents:")
        for i in range(self.count):
            print(f"    Index {i}: {self.heap[i]}")
        print()

def heapify(heapArray, numItems):
    for i in range((numItems // 2) - 1, -1, -1):
        trickleDownArray(heapArray, i, numItems)

def trickleDownArray(heapArray, curIdx, numItems):
    leftChildIdx = (curIdx * 2) + 1
    rightChildIdx = leftChildIdx + 1

    if leftChildIdx < numItems:
        largeIdx = leftChildIdx

        if (rightChildIdx < numItems and
            heapArray[leftChildIdx].getPriority() < heapArray[rightChildIdx].getPriority()):
            largeIdx = rightChildIdx
        
        if heapArray[largeIdx].getPriority() > heapArray[curIdx].getPriority():
            temp = heapArray[largeIdx]
            heapArray[largeIdx] = heapArray[curIdx]
            heapArray[curIdx] = temp

            trickleDownArray(heapArray, largeIdx, numItems)

def heapSort(array):
    numItems = len(array)
    heapify(array, numItems)

    for i in range(numItems - 1, 0, -1):
        temp = array[0]
        array[0] = array[i]
        array[i] = temp
        trickleDownArray(array, 0, i)