import numpy as np
import time
from AdvancedSort import mergeSort, quickSortMedian3

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

# Create duration numpy array from PatientRecords
def durations_from_patients(arr):
    dur_arr = np.zeros(arr.size, dtype=float)
    for i in range(arr.size):
        dur_arr[i] = arr[i].duration
    return dur_arr

# Rebuild record array sorted by durations (stable, no lists)
def stable_patients_by_duration(sorted_durations, original_patients):
    size = sorted_durations.size
    sorted_arr = np.empty(size, dtype=object)
    used = np.zeros(size, dtype=bool)
    for i in range(size):
        v = sorted_durations[i]
        for j in range(size):
            if not used[j] and original_patients[j].duration == v:
                sorted_arr[i] = original_patients[j]
                used[j] = True
                break
    return sorted_arr

def benchmark_sorts_np():
    sizes = np.array([100, 500, 1000])
    disorders = np.array(["random", "nearly_sorted", "reversed"])
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
                if sorted_merge[k].duration > sorted_merge[k+1].duration:
                    merge_ok = False
                    break
            for k in range(size-1):
                if sorted_quick[k].duration > sorted_quick[k+1].duration:
                    quick_ok = False
                    break
            results[idx] = (size, disorder, t1-t0, t3-t2, merge_ok, quick_ok)
            idx += 1
    print("\n| Size | Input Condition | MergeSort (s) | QuickSort (s) | Merge OK | Quick OK |")
    print("|------|----------------|---------------|--------------|----------|----------|")
    for i in range(results.size):
        r = results[i]
        print(f"| {r['size']:<4} | {r['disorder']:<14} | {r['merge_time']:<13.5f} | {r['quick_time']:<12.5f} | {str(r['merge_ok']):<8} | {str(r['quick_ok']):<8} |")

benchmark_sorts_np()