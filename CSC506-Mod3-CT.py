# CSC505 Module 3 Critical Thinking.
# Algorithms: Bubble Sort and Merge Sort.

array = [456, 987, 123, 789, 567]
bubble_array = array.copy()
merge_array = array.copy()


def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1): # using for loop until len(arr) -1
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]: # compare array[j] with [j+1]
                arr[j], arr[j + 1] = arr[j + 1], arr[j] # swapping value

bubble_sort(bubble_array)
print(bubble_array)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # median of array --> for splitting array into 2
        left_half = arr[:mid]  # split left array
        right_half = arr[mid:] # split right array
        
        # doing recursion until len of array just 1 or 2
        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        
        # using while loop while left array AND right array still have a value
        while i < len(left_half) and j < len(right_half):
            # placing smallest number on the left
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i] 
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1


        # using while loop to do only left/right array
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

merge_sort(merge_array)
print(merge_array)