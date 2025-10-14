from Hospital import *
from LinkedList import DSALinkedList

# Graph Algorithm Functions
def bfs_group_by_level(graph, startLabel):
    visited = DSALinkedMap()
    levels = DSALinkedMap()
    result = DSALinkedList() # to create a linked list of the department per level

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

        # placing correct department to the correct level
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

    # getting the department per level printed
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

def dfs_detect_cycle(graph, startLabel):
    graph.clearVisited()
    node = graph.getVertex(startLabel)
    if node is None:
        print("Start vertex not found.")
        return DSALinkedList()
    longest_cycle = DSALinkedList()
    path = DSALinkedList()
    
    def removeLast(ll):
        if ll.head is None:
            return
        if ll.head == ll.tail:
            ll.head = None
            ll.tail = None
            return
        curr = ll.head
        while curr.getNext() != ll.tail:
            curr = curr.getNext()
        curr.setNext(None)
        ll.tail = curr
    
    def getLength(ll):
        count = 0
        curr = ll.head
        while curr is not None:
            count += 1
            curr = curr.getNext()
        return count
    
    def dfs(current, parent):
        current.setVisited(True)
        path.insertLast(current.getLabel())
        
        lCurr = current.links.head
        while lCurr is not None:
            nbr = lCurr.getValue()
            is_parent = (nbr == parent)
            if not is_parent:
                if not nbr.getVisited():
                    #if not parent and not visited yet, recursively go deeper
                    dfs(nbr, current)
                else:
                    # if visited, check if the edge leads to the parent
                    pCurr = path.head
                    in_path = False
                    while pCurr is not None:
                        if pCurr.getValue() == nbr.getLabel():
                            in_path = True
                        pCurr = pCurr.getNext()
                    if in_path:
                        # find where the cycle starts in the path
                        idx = 0
                        pCurr = path.head
                        found = False
                        while pCurr is not None and not found:
                            if pCurr.getValue() == nbr.getLabel():
                                found = True
                            else:
                                idx += 1
                                pCurr = pCurr.getNext()
                        # copy from that point to the end of the cycle        
                        cycle = DSALinkedList()
                        pCurr = path.head
                        count = 0
                        # copy nodes from path[idx] to path[end]
                        while pCurr is not None and count < idx:
                            pCurr = pCurr.getNext()
                            count += 1
                        while pCurr is not None:
                            cycle.insertLast(pCurr.getValue())
                            pCurr = pCurr.getNext()
                        # close the cycle     
                        cycle.insertLast(nbr.getLabel())
                        contains_start = False
                        clCurr = cycle.head
                        while clCurr is not None:
                            if clCurr.getValue() == startLabel:
                                contains_start = True
                            clCurr = clCurr.getNext()
                        # check if the cycle is the longest
                        if contains_start and getLength(cycle) > getLength(longest_cycle):
                            longest_cycle.head = None
                            longest_cycle.tail = None
                            clCurr = cycle.head
                            while clCurr is not None:
                                longest_cycle.insertLast(clCurr.getValue())
                                clCurr = clCurr.getNext()
            lCurr = lCurr.getNext()
        # backtrack
        removeLast(path)
    
    dfs(node, None)
    if longest_cycle.head is not None:
        print("Cycle detected:")
        cycle_str = ""
        clCurr = longest_cycle.head
        while clCurr is not None:
            cycle_str += clCurr.getValue() + " "
            clCurr = clCurr.getNext()
        print(cycle_str.strip())
    else:
        print("No cycle detected.")
    return longest_cycle

def a_star_shortest_path(graph, weightList, src, dst):
    #Source: https://www.geeksforgeeks.org/dsa/a-search-algorithm/
    #Source: https://www.geeksforgeeks.org/python/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
    pq = PriorityQueue()
    dist = DSALinkedMap()
    prev = DSALinkedMap()
    pq.enqueue(src, 0)
    dist.set(src, 0)
    prev.set(src, None)

    found = False
    while not pq.isEmpty() and not found:
        curr, currCost = pq.dequeue()
        currLabel = curr
        if currLabel == dst:
            found = True
        else:
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
    print("\nTotal walking time:", dist.get(dst)," minute(s)")