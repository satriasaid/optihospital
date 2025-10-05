from HashTable import DSAHashTable
from LinkedList import *

class PatientRecord:
    def __init__(self, patient_id, name, age, department, urgency, status):
        if not str(patient_id).isdigit():
            raise ValueError("Patient ID must be an integer.")
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        try:
            urgency_int = int(urgency)
        except ValueError:
            raise ValueError("Urgency must be an integer 1-5.")
        if not (1 <= urgency_int <= 5):
            raise ValueError("Urgency must be 1-5.")
        self.patient_id = str(patient_id)
        self.name = name
        self.age = age
        self.department = department
        self.urgency = urgency_int
        self.status = status

    def __str__(self):
        return (str(self.patient_id) + "," + str(self.name) + "," +
                str(self.age) + "," + str(self.department) + "," +
                str(self.urgency) + "," + str(self.status))

class HashPatientRecords(DSAHashTable):
    def __init__(self, size=103):
        super().__init__(size)

    def insert(self, patientRecord):
        try:
            updated = self.has_key(patientRecord.patient_id)
            self.put(patientRecord.patient_id, patientRecord)
            if updated:
                print(f"Updated record for patient {patientRecord.patient_id}.")
            else:
                print(f"Inserted new record for patient {patientRecord.patient_id}.")
        except Exception as e:
            print(f"Insert error: {e}")

    def search(self, patientID):
        try:
            return self.get(patientID)
        except Exception as e:
            print(f"Search error: {e}")
            return None

    def delete(self, patientID):
        try:
            self.remove(patientID)
            print(f"Deleted record for patient {patientID}.")
        except Exception as e:
            print(f"Delete error: {e}")

    def load_csv(self, filename):
        import csv
        with open(filename, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                pid, name, age, dept, urg, status = row
                record = PatientRecord(pid, name, age, dept, urg, status)
                self.insert(record)