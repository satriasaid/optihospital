import numpy as np
import time
from AdvancedSort import mergeSort, quickSortMedian3 # Source: 21522611_COMP5008 - Prac09
from HashTable import *
from Emergency import *
from Patients import *

def generate_patients_np(size, seed=42, disorder="random"):
    np.random.seed(seed)
    durations = np.random.randint(5, 180, size)
    if disorder == "nearly_sorted":
        durations = np.sort(durations)
        count = size // 10 if size >= 10 else 1
        idx1 = np.random.choice(np.arange(size), count, replace=False)
        idx2 = np.random.randint(0, size, count)
        for k in range(count):
            i = idx1[k]
            j = idx2[k]
            tmp = durations[i]
            durations[i] = durations[j]
            durations[j] = tmp
    elif disorder == "reversed":
        durations = np.sort(durations)[::-1]
    arr = np.empty(size, dtype=object)
    for i in range(size):
        rec = PatientRecord(f"{1000+i}", f"Name{i}", str(np.random.randint(20,90)), "ICU", np.random.randint(1,6), "Waiting")
        rec.duration = int(durations[i])
        arr[i] = rec
    return arr

def durations_from_patients(arr):
    dur_arr = np.zeros(arr.size, dtype=float)
    for i in range(arr.size):
        patient = arr[i]
        dur_arr[i] = patient.duration
    return dur_arr

def stable_patients_by_duration(sorted_durations, original_patients):
    size = sorted_durations.size
    sorted_arr = np.empty(size, dtype=object)
    used = np.zeros(size, dtype=bool)
    for i in range(size):
        v = sorted_durations[i]
        found = False
        for j in range(size):
            if not found and not used[j]:
                patient = original_patients[j]
                if patient.duration == v:
                    sorted_arr[i] = patient
                    used[j] = True
                    found = True
    return sorted_arr

def benchmark_sorts_np(sizes, disorders):
    sizes = np.array(sizes)
    disorders = np.array(disorders)
    results_dtype = [('size', 'i4'), ('disorder', 'U14'), ('merge_time', 'f8'), ('quick_time', 'f8'), ('merge_ok', '?'), ('quick_ok', '?')]
    results = np.empty(sizes.size * disorders.size, dtype=results_dtype)
    idx = 0
    for si in range(sizes.size):
        for di in range(disorders.size):
            size = sizes[si]
            disorder = disorders[di]
            patients = generate_patients_np(size, seed=42, disorder=disorder)
            arr_merge = durations_from_patients(patients)
            t0 = time.time()
            mergeSort(arr_merge)
            t1 = time.time()
            sorted_merge = stable_patients_by_duration(arr_merge, patients)
            patients_copy = np.copy(patients)
            arr_quick = durations_from_patients(patients_copy)
            t2 = time.time()
            quickSortMedian3(arr_quick)
            t3 = time.time()
            sorted_quick = stable_patients_by_duration(arr_quick, patients_copy)
            merge_ok = True
            quick_ok = True
            for k in range(size-1):
                if sorted_merge[k] is not None and sorted_merge[k+1] is not None:
                    dur1 = sorted_merge[k].duration
                    dur2 = sorted_merge[k+1].duration
                    if dur1 > dur2:
                        merge_ok = False
            for k in range(size-1):
                if sorted_quick[k] is not None and sorted_quick[k+1] is not None:
                    dur1 = sorted_quick[k].duration
                    dur2 = sorted_quick[k+1].duration
                    if dur1 > dur2:
                        quick_ok = False
            results[idx]['size'] = size
            results[idx]['disorder'] = disorder
            results[idx]['merge_time'] = t1-t0
            results[idx]['quick_time'] = t3-t2
            results[idx]['merge_ok'] = merge_ok
            results[idx]['quick_ok'] = quick_ok
            idx += 1
    return results