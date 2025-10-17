import numpy as np
import sys

sys.setrecursionlimit(99999999)

def mergeSort(A):
    _mergeSortRec(A, 0, A.size - 1)

def _mergeSortRec(A, leftIdx, rightIdx):
    if leftIdx < rightIdx:
        midIdx = (leftIdx + rightIdx) // 2
        _mergeSortRec(A, leftIdx, midIdx)
        _mergeSortRec(A, midIdx + 1, rightIdx)
        _merge(A, leftIdx, midIdx, rightIdx)

def _merge(A, leftIdx, midIdx, rightIdx):
    tempArr = np.empty(rightIdx - leftIdx + 1, dtype= A.dtype)
    ii = leftIdx
    jj = midIdx + 1
    kk = 0

    while ii <= midIdx and jj <= rightIdx:
        if A[ii] <= A[jj]:
            tempArr[kk] = A[ii]
            ii += 1
        else:
            tempArr[kk] = A[jj]
            jj += 1
        kk += 1
    
    while ii <= midIdx:
        tempArr[kk] = A[ii]
        ii += 1
        kk += 1
    
    while jj <= rightIdx:
        tempArr[kk] = A[jj]
        jj += 1
        kk += 1
    
    for kk in range(leftIdx, rightIdx + 1):
        A[kk] = tempArr[kk - leftIdx]

# quicksort with left-most pivot
def quickSort(A):
    _quickSortRec(A, 0, A.size - 1)

def _quickSortRec(A, leftIdx, rightIdx):
    if rightIdx > leftIdx:
        pivotIdx = leftIdx
        newPivotIdx = _doPartitioning(A, leftIdx, rightIdx, pivotIdx)
        _quickSortRec(A, leftIdx, newPivotIdx - 1)
        _quickSortRec(A, newPivotIdx + 1, rightIdx)

def _doPartitioning(A, leftIdx, rightIdx, pivIdx):
    pivotVal = A[pivIdx]
    A[pivIdx] = A[rightIdx]
    A[rightIdx] = pivotVal
    currIdx = leftIdx

    for ii in range(leftIdx, rightIdx):
        if A[ii] < pivotVal:
            temp = A[ii]
            A[ii] = A[currIdx]
            A[currIdx] = temp
            currIdx += 1
    newPivIdx = currIdx
    A[rightIdx] = A[newPivIdx]
    A[newPivIdx] = pivotVal
    return newPivIdx

# quicksort with median of three pivot
def quickSortMedian3(A):
    _quickSortMedian3Rec(A, 0, A.size - 1)

def _quickSortMedian3Rec(A, leftIdx, rightIdx):
    if rightIdx > leftIdx:
        pivotIdx = _medianOfThree(A, leftIdx, rightIdx)
        newPivotIdx = _doPartitioning(A, leftIdx, rightIdx, pivotIdx)
        _quickSortMedian3Rec(A, leftIdx, newPivotIdx - 1)
        _quickSortMedian3Rec(A, newPivotIdx + 1, rightIdx)

def _medianOfThree(A, leftIdx, rightIdx):
    midIdx = (leftIdx + rightIdx) // 2
    leftVal = A[leftIdx]
    midVal = A[midIdx]
    rightVal = A[rightIdx]

    if (leftVal <= midVal <= rightVal) or (rightVal <= midVal <= leftVal):
        return midIdx
    elif (midVal <= leftVal <= rightVal) or (rightVal <= leftVal <= midVal):
        return leftIdx
    else:
        return rightIdx

# quicksort with random pivot
def quickSortRandom(A):
    _quickSortRandomRec(A, 0, A.size - 1)

def _quickSortRandomRec(A, leftIdx, rightIdx):
    if rightIdx > leftIdx:
        pivotIdx = np.random.randint(leftIdx, rightIdx + 1)
        newPivotIdx = _doPartitioning(A, leftIdx, rightIdx, pivotIdx)
        _quickSortRandomRec(A, leftIdx, newPivotIdx - 1)
        _quickSortRandomRec(A, newPivotIdx + 1, rightIdx)