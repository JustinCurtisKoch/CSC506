# CSC505 Module 3 Critical Thinking.
# Algorithms: Bubble Sort and Merge Sort.

# Sample of patient records allowig for multiple sortable fields

patient_records = [
    {"patient_id": 12345, "first_name": "Clark", "last_name": "Kent", "state": "Metropolis"},
    {"patient_id": 56789, "first_name": "Bruce", "last_name": "Wayne", "state": "Gotham"},
    {"patient_id": 91012, "first_name": "Diana", "last_name": "Prince", "state": "Themyscira"},
    {"patient_id": 11123, "first_name": "Barry", "last_name": "Allen", "state": "Central City"},
    {"patient_id": 22234, "first_name": "Hal", "last_name": "Jordan", "state": "Coast City"},
    {"patient_id": 33345, "first_name": "Selina", "last_name": "Kyle", "state": "Gotham"},
    {"patient_id": 44456, "first_name": "Kara", "last_name": "Zor-El", "state": "National City"},
]

bubble_array = patient_records.copy()
merge_array = patient_records.copy()


def bubble_sort(arr, key):
    n = len(arr)
    for i in range(n - 1): # using for loop until len(arr) -1
        for j in range(n - i - 1):
            if arr[j][key] > arr[j + 1][key]: # compare array[j] with [j+1]
                arr[j], arr[j + 1] = arr[j + 1], arr[j] # swapping value
    return arr


sorted_by_name = bubble_sort(bubble_array, "last_name")
print("Sorted by Last Name:")
for record in sorted_by_name:
  print(record)

def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr) // 2  # median of array --> for splitting array into 2
        left_half = arr[:mid]  # split left array
        right_half = arr[mid:] # split right array
        
        # doing recursion until len of array just 1 or 2
        merge_sort(left_half, key)
        merge_sort(right_half, key)

        i = j = k = 0
        
        # using while loop while left array AND right array still have a value
        while i < len(left_half) and j < len(right_half):
            # placing smallest number on the left
            if left_half[i][key] < right_half[j][key]:
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
    return arr

sorted_by_id = merge_sort(merge_array, "patient_id")
print("Sorted by Patient ID:")
for record in sorted_by_id:
  print(record)