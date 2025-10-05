import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys
import io

# Import your custom hospital logic
from Hospital import *
from Graph import *
from LinkedList import *
from Patients import *
from Heaps import *
from Emergency import *

# Graph Algorithm Functions (copied from notebook for integration)
def bfs_group_by_level(graph, startLabel):
    # Output: departments grouped into DSALinkedList-of-DSALinkedList (hops)
    visited = DSALinkedMap()
    levels = DSALinkedMap()
    result = DSALinkedList()  # Each value is DSALinkedList of nodes for that level

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

        # Place in correct level bucket
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

    # Print level grouping
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
    foundCycle = False
    parentMap = DSALinkedMap()
    onPath = DSALinkedMap()
    cycleStart = None
    cycleEnd = None

    def visit(node, parent):
        nonlocal foundCycle, cycleStart, cycleEnd
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
                # found cycle
                foundCycle = True
                cycleStart = nbrLabel
                cycleEnd = label
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
    if not foundCycle:
        print("No cycles found.")
    else:
        # Trace cycle path using LinkedMap parent pointers
        pathLL = DSALinkedList()
        curr = cycleEnd
        while curr != cycleStart:
            pathLL.insertFirst(curr)
            curr = parentMap.get(curr)
        pathLL.insertFirst(cycleStart)
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
                pq.enqueue(nbrLabel, alt)  # heuristic=0
            nbrs = nbrs.getNext()

    # Reconstruct path
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

# Main UI with tabs
tab1, tab2, tab3 = st.tabs(["Hospital Graph", "Patient Records", "Patient Priority Queue"])

with tab1:
    st.header("Hospital Graph Builder")

    # Departments CSV Upload
    st.subheader("Departments (Nodes)")
    departments_file = st.file_uploader("Upload Departments CSV (column: Department)", type="csv", key="departments_csv")
    departments = []
    if departments_file is not None:
        departments_df = pd.read_csv(departments_file)
        if "Department" in departments_df.columns:
            departments = departments_df["Department"].dropna().tolist()
            departments = [str(d).strip() for d in departments if str(d).strip()]
            st.write("Loaded Departments:", departments)
        else:
            st.error("CSV must have a 'Department' column.")

    # Corridors CSV Upload
    st.subheader("Corridors (Edges)")
    corridors_file = st.file_uploader("Upload Corridors CSV (columns: DepartmentA, DepartmentB, WalkingTime)", type="csv", key="corridors_csv")
    corridors = []
    if corridors_file is not None:
        corridors_df = pd.read_csv(corridors_file)
        if all(col in corridors_df.columns for col in ["DepartmentA", "DepartmentB", "WalkingTime"]):
            for _, row in corridors_df.iterrows():
                try:
                    deptA = str(row["DepartmentA"]).strip()
                    deptB = str(row["DepartmentB"]).strip()
                    weight = int(row["WalkingTime"])
                    corridors.append((deptA, deptB, weight))
                except (ValueError, TypeError):
                    continue
            st.write("Loaded Corridors:", corridors)
        else:
            st.error("CSV must have 'DepartmentA', 'DepartmentB', and 'WalkingTime' columns.")

    if st.button("Visualize Hospital Graph") and departments and corridors:
        # -- Update HospitalGraph module object (your core logic) --
        hgraph = HospitalGraph()
        # Add nodes (departments)
        for dept in departments:
            hgraph.addVertex(dept)
        # Add edges
        for u, v, w in corridors:
            hgraph.addWeightedEdge(u, v, w)

        # -- Visualize using NetworkX (for display only) --
        G = nx.Graph()
        for dept in departments:
            G.add_node(dept)
        for u, v, w in corridors:
            G.add_edge(u, v, weight=w)
        pos = nx.spring_layout(G, seed=42)
        fig, ax = plt.subplots(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=10, ax=ax)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', ax=ax)
        ax.set_title("Hospital Departments and Corridors")
        st.pyplot(fig)

        # Optionally, print your adjacency/weight structure using HospitalGraph module methods
        st.write("Adjacency List from Module:")
        buf = io.StringIO()
        sys.stdout = buf
        hgraph.displayAsList()  # Provided in your module
        sys.stdout = sys.__stdout__
        st.text(buf.getvalue())

        # Store hgraph in session state for use in other buttons
        st.session_state['hgraph'] = hgraph
        st.session_state['weightList'] = hgraph.weightList  # Assuming weightList is accessible

    # Algorithm Inputs and Buttons (only show if graph is built)
    if 'hgraph' in st.session_state:
        st.subheader("Graph Algorithms")
        
        start_node = st.text_input("Start Node for BFS and DFS:", value="Emergency", key="start_node")
        
        if st.button("Run BFS Group by Level"):
            if start_node in departments:
                buf = io.StringIO()
                sys.stdout = buf
                bfs_group_by_level(st.session_state['hgraph'], start_node)
                sys.stdout = sys.__stdout__
                st.text("BFS Output:")
                st.text(buf.getvalue())
            else:
                st.error("Start node not in departments.")
        
        if st.button("Run DFS Detect Cycle"):
            if start_node in departments:
                buf = io.StringIO()
                sys.stdout = buf
                dfs_detect_cycle(st.session_state['hgraph'], start_node)
                sys.stdout = sys.__stdout__
                st.text("DFS Output:")
                st.text(buf.getvalue())
            else:
                st.error("Start node not in departments.")
        
        src = st.text_input("Source Node for A*:", value="Emergency", key="src")
        dst = st.text_input("Destination Node for A*:", value="ICU", key="dst")
        
        if st.button("Run A* Shortest Path"):
            if src in departments and dst in departments:
                buf = io.StringIO()
                sys.stdout = buf
                a_star_shortest_path(st.session_state['hgraph'], st.session_state['weightList'], src, dst)
                sys.stdout = sys.__stdout__
                st.text("A* Output:")
                st.text(buf.getvalue())
            else:
                st.error("Source or destination node not in departments.")

with tab2:
    st.header("Patient Records Management")

    # Initialize patient records in session state
    if 'patients' not in st.session_state:
        st.session_state['patients'] = HashPatientRecords()

    patients = st.session_state['patients']

    # Load CSV
    st.subheader("Load Patients from CSV")
    patients_file = st.file_uploader("Upload Patients CSV (columns: patient_id, name, age, department, urgency, status)", type="csv", key="patients_csv")
    if patients_file is not None and st.button("Load CSV"):
        patients_df = pd.read_csv(patients_file)
        if all(col in patients_df.columns for col in ["patient_id", "name", "age", "department", "urgency", "status"]):
            for _, row in patients_df.iterrows():
                try:
                    record = PatientRecord(
                        row["patient_id"], row["name"], row["age"], 
                        row["department"], row["urgency"], row["status"]
                    )
                    patients.insert(record)
                except Exception as e:
                    st.error(f"Error loading row: {e}")
            st.session_state['patients_df'] = patients_df
            st.success("Patients loaded from CSV.")
        else:
            st.error("CSV must have columns: patient_id, name, age, department, urgency, status.")

    # Insert New Patient
    st.subheader("Insert New Patient")
    with st.form("insert_patient"):
        pid = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        department = st.text_input("Department")
        urgency = st.selectbox("Urgency", [1, 2, 3, 4, 5])
        status = st.text_input("Status")
        submitted = st.form_submit_button("Insert Patient")
        if submitted:
            try:
                record = PatientRecord(pid, name, age, department, urgency, status)
                patients.insert(record)
                # Add to dataframe if loaded
                if 'patients_df' in st.session_state:
                    new_row = pd.DataFrame([{
                        "patient_id": pid, "name": name, "age": age, 
                        "department": department, "urgency": urgency, "status": status
                    }])
                    st.session_state['patients_df'] = pd.concat([st.session_state['patients_df'], new_row], ignore_index=True)
                st.success("Patient inserted.")
            except Exception as e:
                st.error(f"Insert error: {e}")

    # Search Patient
    st.subheader("Search Patient")
    search_id = st.text_input("Patient ID to Search")
    if st.button("Search"):
        result = patients.search(search_id)
        if result:
            st.write("Found Patient:")
            st.write(f"ID: {result.patient_id}, Name: {result.name}, Age: {result.age}, Department: {result.department}, Urgency: {result.urgency}, Status: {result.status}")
        else:
            st.error("Patient not found.")

    # Delete Patient
    st.subheader("Delete Patient")
    delete_id = st.text_input("Patient ID to Delete")
    if st.button("Delete"):
        patients.delete(delete_id)
        # Remove from dataframe if loaded
        if 'patients_df' in st.session_state:
            st.session_state['patients_df'] = st.session_state['patients_df'][st.session_state['patients_df']['patient_id'] != delete_id]

    # View All Patients
    st.subheader("All Patient Records")
    if 'patients_df' in st.session_state:
        st.dataframe(st.session_state['patients_df'])
    else:
        st.write("No patients loaded.")

with tab3:
    st.header("Emergency Scheduler")

    # Initialize scheduler in session state
    if 'scheduler' not in st.session_state:
        st.session_state['scheduler'] = EmergencyScheduler(1000, st.session_state['patients'])  # Assuming patients is loaded

    scheduler = st.session_state['scheduler']

    # Load CSV
    st.subheader("Load Patients from CSV")
    pq_file = st.file_uploader("Upload patient_treatment.csv", type="csv", key="pq_csv")
    if pq_file is not None and st.button("Load CSV for Scheduler"):
        pq_df = pd.read_csv(pq_file)
        if all(col in pq_df.columns for col in ["patient_id", "expected_time"]):
            for _, row in pq_df.iterrows():
                try:
                    pid = str(row["patient_id"])
                    expected_time = int(row["expected_time"])
                    scheduler.insert(pid, expected_time)
                except Exception as e:
                    st.error(f"Error loading row: {e}")
            st.session_state['sched_df'] = pq_df
            st.success("Patients loaded into scheduler.")
        else:
            st.error("CSV must have columns: patient_id, expected_time.")

    # Peek
    st.subheader("Peek Highest Priority")
    if st.button("Peek"):
        buf = io.StringIO()
        sys.stdout = buf
        req = scheduler.peek()
        sys.stdout = sys.__stdout__
        st.text("Peek Output:")
        st.text(buf.getvalue())
        # Show heap contents as dataframe
        contents = []
        for i in range(scheduler.heap.count):
            entry = scheduler.heap.heap[i]
            req = entry.getValue()
            contents.append({
                'Index': i,
                'PatientID': req.patient_id,
                'ExpectedTime': req.expected_time,
                'Priority': round(entry.getPriority(), 2)
            })
        if contents:
            df = pd.DataFrame(contents)
            st.dataframe(df)

    # Extract Priority
    st.subheader("Extract Highest Priority")
    if st.button("Extract"):
        buf = io.StringIO()
        sys.stdout = buf
        req = scheduler.extract_priority()
        sys.stdout = sys.__stdout__
        st.text("Extract Output:")
        st.text(buf.getvalue())
        # Show heap contents as dataframe after extraction
        contents = []
        for i in range(scheduler.heap.count):
            entry = scheduler.heap.heap[i]
            req = entry.getValue()
            contents.append({
                'Index': i,
                'PatientID': req.patient_id,
                'ExpectedTime': req.expected_time,
                'Priority': round(entry.getPriority(), 2)
            })
        if contents:
            df = pd.DataFrame(contents)
            st.dataframe(df)

    # Update
    st.subheader("Update Patient")
    with st.form("update_sched"):
        pid = st.text_input("Patient ID")
        new_urg = st.selectbox("New Urgency", [1,2,3,4,5])
        new_time = st.number_input("New Expected Time", min_value=1)
        submitted = st.form_submit_button("Update")
        if submitted:
            buf = io.StringIO()
            sys.stdout = buf
            scheduler.update(pid, new_urg, new_time)
            sys.stdout = sys.__stdout__
            st.text("Update Output:")
            st.text(buf.getvalue())
