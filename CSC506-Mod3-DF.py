# List of students (name, class)
students = [
    ("Zoe", "3A"),
    ("Alice", "2B"),
    ("Charlie", "1A"),
    ("David", "3A"),
    ("Eve", "2B"),
    ("Frank", "1B"),
    ("Grace", "2A"),
    ("Hannah", "3B"),
    ("Bob", "1A"),
    ("Isaac", "2B"),
]

students_merge = students.copy()
students_quick_sort = students.copy()

def merge_sort(arr, key_index):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half, key_index)
        merge_sort(right_half, key_index)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][key_index] < right_half[j][key_index]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr

print(students)

students_merge_by_name = merge_sort(students_merge, 0)
print(students_merge_by_name)

students_merge_by_course = merge_sort(students_merge, 1)
print(students_merge_by_course)


def quick_sort(arr, key_index):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][key_index]
    left = [x for x in arr if x[key_index] < pivot]
    middle = [x for x in arr if x[key_index] == pivot]
    right = [x for x in arr if x[key_index] > pivot]
    return quick_sort(left, key_index) + middle + quick_sort(right, key_index)

print(students)

students_quick_sort_by_name = quick_sort(students_quick_sort, 0)
print(students_quick_sort_by_name)

students_quick_sort_by_course = quick_sort(students_quick_sort, 1)
print(students_quick_sort_by_course)