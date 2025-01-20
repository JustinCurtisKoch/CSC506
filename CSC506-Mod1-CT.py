# CSC505 Module 1 Critical Thinking
# Linear Search Algorithm example.

# Sample of product numbers
product_numbers = [101, 102, 103, 104, 105, 106, 107]

# Sample of product names
product_names = ["Laptop", "Smartphone", "Tablet", "Smartwatch", "Headphones", "Camera", "Printer"]

# Linear Search Algorithm
def linear_search(product_list, target):
    for i in range(len(product_list)):
        if product_list[i] == target:
            return i
    return -1

# Test the linear search algorithm
target = 105
result = linear_search(product_numbers, target)
if result != -1:
    print("Product number", target, "found at index", result)

taget = "Smartwatch"
result = linear_search(product_names, target)
if result != -1:
    print("Product name", target, "found at index", result)

target = "Stereo"
result = linear_search(product_names, target)
if result != -1:
    print("Product name", target, "found at index", result)
else:
    print("Product name", target, "not found.")