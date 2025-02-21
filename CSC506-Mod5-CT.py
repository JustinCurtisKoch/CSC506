# CSC505 Module 5 Critical Thinking
# Algorithm: Hash Table

keys = ["apricot", "banana", "cherry", "date", "grape"]
table_size = 9

# Convert keys to integers
key_ints = []
for key in keys:
    key_int = 0
    for char in key:
        key_int += ord(char)
    key_ints.append(key_int)

# Hash functions
def division_hash(key, table_size):
    hash_value = key % table_size
    print(f"Division Hash for '{key}': {hash_value}")
    return hash_value

def multiplication_hash(key, table_size):
    a = 0.6180339887
    hash_value = int(table_size * ((a * key) % 1))
    print(f"Multiplication Hash for '{key}': {hash_value}")
    return hash_value

# Calculate and print hash values
for i, key_int in enumerate(key_ints):
    print(f"Key {i+1}: {keys[i]}")
    division_hash(key_int, table_size)
    multiplication_hash(key_int, table_size)
    print("-" * 20)


