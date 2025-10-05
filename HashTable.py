from LinkedList import *
import csv
import numpy as np

class DSAHashEntry:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        if key is None and value is None:
            self.state = 0
        else:
            self.state = 1
    
    def set(self, key, value):
        self.key = key
        self.value = value
        self.state = 1
    
    def remove(self):
        self.key = None
        self.value = None
        self.state = -1

class DSAHashTable:
    def __init__(self, initial_capacity=7):
        self.capacity = self._next_prime(initial_capacity)
        self.hashArray = self._make_array(self.capacity)
        self.count = 0
        self.up_threshold = 0.7
        self.low_threshold = 0.2
    
    def put(self, key, value):
        self._ensure_resize_on_insert()
        idx = self._hash(key)
        start = idx
        while True:
            entry = self.hashArray[idx]
            if entry.state in (0,-1) or (entry.state == 1 and entry.key == key):
                if entry.state != 1:
                    self.count += 1
                entry.set(key, value)
                return
            idx = (idx + 1) % self.capacity
            if idx == start:
                raise Exception("HashTable full")
            
    def get(self, key):
        idx = self._find_key_index(key)
        if idx is None:
            raise KeyError(f"{key} not found")
        return self.hashArray[idx].value
    
    def has_key(self, key):
        return self._find_key_index(key) is not None
    
    def remove(self, key):
        idx = self._find_key_index(key)
        if idx is None:
            raise KeyError(f"{key} not found")
        self.hashArray[idx].remove()
        self.count -= 1
        self._ensure_resize_on_remove()
    
    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            i = 0
            while i < self.capacity:
                entry = self.hashArray[i]
                if entry.state == 1:
                    writer.writerow([str(entry.key), str(entry.value)])
                i += 1
    
    def load_from_csv(self, filename):
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                key = row[0]
                value = row[1]
                self.put(key, value)
    
    def _find_key_index(self, key):
        idx = self._hash(key)
        start = idx
        while True:
            entry = self.hashArray[idx]
            if entry.state == 0:
                return None
            if entry.state == 1 and entry.key == key:
                return idx
            idx = (idx + 1) % self.capacity
            if idx == start:
                return None
    
    def _hash(self, key):
        #Source: https://www.geeksforgeeks.org/dsa/string-hashing-using-polynomial-rolling-hash-function/
        h = 0
        for ch in key:
            h = (31 * h + ord(ch)) % self.capacity
        return h
    
    def _ensure_resize_on_insert(self):
        if (self.count + 1)/ self.capacity > self.up_threshold:
            self._resize(self.capacity * 2)
        
    def _ensure_resize_on_remove(self):
        if self.capacity > 7 and self.count / self.capacity < self.low_threshold:
            self._resize(7 if 7 > self.capacity // 2 else self.capacity // 2)
    
    def _resize(self, new_size):
        old_keys = np.full(self.capacity, None, dtype = object)
        old_values = np.full(self.capacity, None, dtype = object)
        i = 0
        for idx in range(self.capacity):
            e = self.hashArray[idx]
            if e.state == 1:
                old_keys[i] = e.key
                old_values[i] = e.value
                i += 1
        old_keys = old_keys[:i]
        old_values = old_values[:i]
        self.capacity = self._next_prime(new_size)
        self.hashArray = self._make_array(self.capacity)
        self.count = 0
        for j in range(len(old_keys)):
            self.put(old_keys[j], old_values[j])
    
    def _is_prime(self, n):
        if n < 2: return False
        if n % 2 == 0 and n != 2: return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def _next_prime(self, n):
        if n % 2 == 0:
            n += 1
        while not self._is_prime(n):
            n += 2
        return n
    
    def _make_array(self, size):
        arr = np.empty(size, dtype = object)
        i = 0
        while i < size:
            arr[i] = DSAHashEntry()
            i += 1
        return arr
    
    def get_load_factor(self):
        return self.count / self.capacity