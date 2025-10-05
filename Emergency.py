from Heaps import DSAHeap
from HashTable import DSAHashTable

# Emergency request for scheduling
class EmergencyRequest:
    def __init__(self, patient_id, expected_time):
        self.patient_id = patient_id
        self.expected_time = expected_time  # in minutes
        self.priority = None  # computed later
    
    def __str__(self):
        return f"PatientID: {self.patient_id}, ExpectedTime: {self.expected_time}, Priority: {self.priority}"

# Emergency Scheduler using Max Heap
class EmergencyScheduler:
    def __init__(self, maxSize, patientTable):
        self.heap = DSAHeap(maxSize)
        self.patientTable = patientTable  # DSAHashTable from Module 2
    
    def compute_priority(self, urgency, expected_time):
        # Priority = (6 - U) + 1000 / T
        if expected_time <= 0:
            raise ValueError("Expected treatment time must be positive.")
        return (6 - urgency) + (1000 / expected_time)
    
    def insert(self, patient_id, expected_time):
        # Validate patient
        try:
            patient = self.patientTable.get(patient_id)
        except Exception:
            print(f"Error: PatientID {patient_id} not found.")
            return
        if patient.status.lower() != "waiting" and patient.status.lower() != "critical":
            print(f"Error: Patient {patient_id} is not active (status: {patient.status}).")
            return
        if expected_time <= 0:
            print(f"Error: Invalid expected time for patient {patient_id}.")
            return
        priority = self.compute_priority(patient.urgency, expected_time)
        req = EmergencyRequest(patient_id, expected_time)
        req.priority = priority
        self.heap.add(priority, req)
        print(f"Inserted: {req} (U={patient.urgency}, T={expected_time}, Priority={priority:.2f})")
        self.heap.display()
    
    def peek(self):
        if self.heap.count == 0:
            print("Heap is empty.")
            return None
        entry = self.heap.heap[0] # because the heap is saved in an array, that is why .heap[0]
        print(f"Peek: {entry.getValue()} (Priority={entry.getPriority():.2f})")
        return entry.getValue()
    
    def extract_priority(self):
        if self.heap.count == 0:
            print("Heap is empty.")
            return None
        entry = self.heap.remove()
        req = entry.getValue()
        print(f"Extracted: {req} (Priority={entry.getPriority():.2f})")
        self.heap.display()
        return req
    
    def remove_patient(self, patient_id):
        for i in range(self.heap.count):
            if self.heap.heap[i].getValue().patient_id == patient_id:
                # Swap with last element
                self.heap.heap[i] = self.heap.heap[self.heap.count - 1]
                self.heap.count -= 1
                # Heapify down from i
                self.heap.trickleDown(i)
                return True
        return False
    
    def update(self, patient_id, new_urgency=None, new_expected_time=None):
        # Remove old entry if exists, then insert new
        try:
            patient = self.patientTable.get(patient_id)
        except Exception:
            print(f"Error: PatientID {patient_id} not found for update.")
            return
        if new_urgency is not None:
            patient.urgency = int(new_urgency)
        expected_time = new_expected_time if new_expected_time is not None else 30  # default
        # Remove old entry
        self.remove_patient(patient_id)
        # Insert new
        self.insert(patient_id, expected_time)
        print(f"Update: Patient {patient_id} updated with urgency {patient.urgency} and expected time {expected_time}.")
