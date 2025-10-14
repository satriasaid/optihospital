import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys
import io
import matplotlib.pyplot as plt
import csv
import numpy as np
import time

# importing custom classes and functions
from Hospital import *
from Hospital_Func import bfs_group_by_level, dfs_detect_cycle, a_star_shortest_path
from Graph import *
from LinkedList import *
from Patients import *
from PatientSort import benchmark_sorts_np
from Heaps import *
from Emergency import *
from PatientSort import benchmark_sorts_np, generate_patients_np, priorities_from_patients, stable_patients_by_priority
from HashTable import DSAHashTable
from Emergency import EmergencyScheduler
from AdvancedSort import mergeSort, quickSortMedian3


# the setup of tabs in the main webpage
tab1, tab2, tab3, tab4 = st.tabs(["Hospital Graph", "Patient Records", "Patient Priority Queue", "Sorting Benchmarks"])

with tab1:
    st.header("Hospital Graph Builder")

    # Allowing CSV upload of departments
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

    # Allowing CSV upload of corridors of the previously uploaded departments
    st.subheader("Corridors (Edges)")
    corridors_file = st.file_uploader("Upload Corridors CSV (columns: DepartmentA, DepartmentB, WalkingTime)", type="csv", key="corridors_csv")
    corridors = []
    if corridors_file is not None:
        corridors_df = pd.read_csv(corridors_file)
        if all(col in corridors_df.columns for col in ["DepartmentA", "DepartmentB", "WalkingTime"]):
            for _, row in corridors_df.iterrows():
                deptA = str(row["DepartmentA"]).strip()
                deptB = str(row["DepartmentB"]).strip()
                weight_str = str(row["WalkingTime"]).strip()
                if deptA and deptB and weight_str.isdigit():
                    weight = int(weight_str)
                    corridors.append((deptA, deptB, weight))
            st.write("Loaded Corridors:", corridors)
        else:
            st.error("CSV must have 'DepartmentA', 'DepartmentB', and 'WalkingTime' columns.")

    # Create hospital map's graph
    if st.button("Visualize Hospital Graph") and departments and corridors:
        hgraph = HospitalGraph()
        for dept in departments:
            hgraph.addVertex(dept)
        for u, v, w in corridors:
            hgraph.addWeightedEdge(u, v, w)

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

        # Print adjacency list in the web page
        # Source: https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
        st.write("Adjacency List:")
        buf = io.StringIO()
        sys.stdout = buf
        hgraph.displayAsList()
        sys.stdout = sys.__stdout__
        st.text(buf.getvalue())

        # preserve value in the session
        # Source: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
        st.session_state['hgraph'] = hgraph
        st.session_state['weightList'] = hgraph.weightList

    # BFS for hopping and DFS for cycle detection
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
        
        # A* shortest path across two different departments
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

    # initialise patient in the session
    if 'patients' not in st.session_state:
        st.session_state['patients'] = HashPatientRecords()

    patients = st.session_state['patients']

    # Allowing to upload csv
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

    # Allowing to add new patient into the webpage system
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
                if 'patients_df' in st.session_state:
                    df = st.session_state['patients_df']
                    if str(pid) in df['patient_id'].astype(str).values:
                        # Update existing row
                        df.loc[df['patient_id'].astype(str) == str(pid), ['name', 'age', 'department', 'urgency', 'status']] = [name, age, department, urgency, status]
                        st.session_state['patients_df'] = df
                    else:
                        # Add new row
                        new_row = pd.DataFrame([{
                            "patient_id": pid, "name": name, "age": age, 
                            "department": department, "urgency": urgency, "status": status
                        }])
                        st.session_state['patients_df'] = pd.concat([df, new_row], ignore_index=True)
                st.success("Patient inserted/updated.")
            except Exception as e:
                st.error(f"Insert error: {e}")

    # Patient Lookup
    st.subheader("Search Patient")
    search_id = st.text_input("Patient ID to Search")
    if st.button("Search"):
        result = patients.search(search_id)
        if result:
            st.write("Found Patient:")
            st.write(f"ID: {result.patient_id}, Name: {result.name}, Age: {result.age}, Department: {result.department}, Urgency: {result.urgency}, Status: {result.status}")
        else:
            st.error("Patient not found.")

    # Patient Removal
    st.subheader("Delete Patient")
    delete_id = st.text_input("Patient ID to Delete")
    if st.button("Delete"):
        patients.delete(delete_id)
        if 'patients_df' in st.session_state:
            st.session_state['patients_df'] = st.session_state['patients_df'][st.session_state['patients_df']['patient_id'].astype(str) != str(delete_id)]

    # Show list of patients
    st.subheader("All Patient Records")
    if 'patients_df' in st.session_state:
        st.dataframe(st.session_state['patients_df'])
    else:
        st.write("No patients loaded.")

with tab3:
    st.header("Emergency Scheduler")

    # Add scheduler to the session state
    if 'scheduler' not in st.session_state:
        st.session_state['scheduler'] = EmergencyScheduler(1000, st.session_state['patients']) # need to load the patient data

    scheduler = st.session_state['scheduler']

    # Allow to upload CSV
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

    # Peek the item with the highest priority
    st.subheader("Peek Highest Priority")
    if st.button("Peek"):
        buf = io.StringIO()
        sys.stdout = buf
        req = scheduler.peek()
        sys.stdout = sys.__stdout__
        st.text("Peek Output:")
        st.text(buf.getvalue())
        # print the table of to know the current and next priority
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

    # print the table of to know the next priority after the current priority is extracted
    st.subheader("Extract Highest Priority")
    if st.button("Extract"):
        buf = io.StringIO()
        sys.stdout = buf
        req = scheduler.extract_priority()
        sys.stdout = sys.__stdout__
        st.text("Extract Output:")
        st.text(buf.getvalue())
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

    # feature to update the patient's priority based on urgency and new expected time
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

with tab4:
    st.header("Sorting Benchmarks")

    st.subheader("Benchmark Parameters")
    sizes_input = st.text_input("Sizes (comma-separated, e.g., 10,50,100,500,1000,5000,10000)", value="10,50,100,500,1000,5000,10000")
    disorders_input = st.text_input("Disorders (comma-separated, e.g., random,nearly_sorted,reversed)", value="random,nearly_sorted,reversed")

    if st.button("Run Benchmark"):
        try:
            sizes = [int(s.strip()) for s in sizes_input.split(',')]
            disorders = [d.strip() for d in disorders_input.split(',')]
            results = benchmark_sorts_np(sizes, disorders)
            
            df = pd.DataFrame({
                'Size': results['size'],
                'Input Condition': results['disorder'],
                'MergeSort (s)': results['merge_time'],
                'QuickSort (s)': results['quick_time'],
                'Merge OK': results['merge_ok'],
                'Quick OK': results['quick_ok']
            })
            st.dataframe(df)
            
            # plot the performance of sorting in a graph
            fig, ax = plt.subplots(figsize=(10, 6))
            for disorder in disorders:
                subset = df[df['Input Condition'] == disorder]
                ax.plot(subset['Size'], subset['MergeSort (s)'], label=f'MergeSort - {disorder}', marker='o')
                ax.plot(subset['Size'], subset['QuickSort (s)'], label=f'QuickSort - {disorder}', marker='s')
            ax.set_xlabel('Size')
            ax.set_ylabel('Time (s)')
            ax.set_title('Sorting Algorithm Performance by Priority')
            ax.legend()
            ax.set_xscale('log')
            ax.set_yscale('log')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error running benchmark: {e}")
    
    st.subheader("Generate Patient CSVs")
    size = st.number_input("Size", min_value=1, value=100)
    disorder = st.selectbox("Disorder", ["random", "nearly_sorted", "reversed"])
    seed = st.number_input("Seed", min_value=0, value=42)
    sort_algorithm = st.selectbox("Sorting Algorithm", ["mergeSort", "quickSortMedian3"])

    if st.button("Generate CSVs"):
        # Set up dummy scheduler
        dummy_table = DSAHashTable()
        scheduler = EmergencyScheduler(1, dummy_table)

        # Generate patients
        patients = generate_patients_np(size, seed=seed, disorder=disorder)

        # Compute priorities
        priorities = priorities_from_patients(patients, scheduler)

        # Function to write patients to CSV
        def write_patients_to_csv(filename, patients_array, priorities_array=None):
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Patient_ID', 'Name', 'Age', 'Department', 'Urgency', 'Status', 'Duration', 'Priority']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i, patient in enumerate(patients_array):
                    priority = priorities_array[i] if priorities_array is not None else (6 - patient.urgency) + (1000 / patient.duration)
                    writer.writerow({
                        'Patient_ID': patient.patient_id,
                        'Name': patient.name,
                        'Age': patient.age,
                        'Department': patient.department,
                        'Urgency': patient.urgency,
                        'Status': patient.status,
                        'Duration': patient.duration,
                        'Priority': priority
                    })

        # Non-sorted CSV
        write_patients_to_csv('patients_nonsorted.csv', patients, priorities)

        # Sorted CSV: sort priorities in descending order (highest priority first)
        sorted_priorities = np.copy(priorities)
        t0 = time.time()
        if sort_algorithm == "mergeSort":
            mergeSort(sorted_priorities)
        elif sort_algorithm == "quickSortMedian3":
            quickSortMedian3(sorted_priorities)
        t1 = time.time()
        sort_time = t1 - t0
        # Reverse the sorted array to have highest priority first
        sorted_priorities = sorted_priorities[::-1]
        sorted_patients = stable_patients_by_priority(sorted_priorities, patients)
        write_patients_to_csv('patients_sorted.csv', sorted_patients, sorted_priorities)

        st.success(f"CSVs generated: patients_nonsorted.csv and patients_sorted.csv. Sorting time: {sort_time:.6f} seconds")
