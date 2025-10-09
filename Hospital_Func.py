from Hospital import *

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

class CycleState:
    def __init__(self):
        self.foundCycle = False
        self.cycleStart = None
        self.cycleEnd = None

def dfs_detect_cycle(graph, startLabel):
    parentMap = DSALinkedMap()
    onPath = DSALinkedMap()
    state = CycleState()

    def visit(node, parent):
        label = node.getLabel()
        onPath.set(label, True)
        nbrs = node.getLinks().head
        while nbrs is not None:
            nbrNode = nbrs.getValue()
            nbrLabel = nbrNode.getLabel()
            if parent is not None and nbrLabel == parent.getLabel():
                nbrs = nbrs.getNext()
                continue
            if onPath.has(nbrLabel):
                state.foundCycle = True
                state.cycleStart = nbrLabel
                state.cycleEnd = label
                parentMap.set(nbrLabel, label)
                return True
            if not parentMap.has(nbrLabel):
                parentMap.set(nbrLabel, label)
                if visit(nbrNode, node):
                    return True
            nbrs = nbrs.getNext()
        onPath.set(label, False)
        return False

    root = graph.getVertex(startLabel)
    parentMap.set(startLabel, None)
    visit(root, None)
    print("DFS Cycle Detection:")
    if not state.foundCycle:
        print("No cycles found.")
    else:
        pathLL = DSALinkedList()
        curr = state.cycleEnd
        while curr != state.cycleStart:
            pathLL.insertFirst(curr)
            curr = parentMap.get(curr)
        pathLL.insertFirst(state.cycleStart)
        print("Cycle found: ", end=" ")
        p = pathLL.head
        while p is not None:
            print(p.getValue(), end=", ")
            p = p.getNext()
        print()

def a_star_shortest_path(graph, weightList, src, dst):
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
    print("\nTotal walking time:", dist.get(dst)," minute(s)")