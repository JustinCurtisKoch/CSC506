# CSC505 Module 5 Critical Thinking
# Algorithm: Hash Table

# Import hash library 
import hashlib

# List of keys
keys = ["appricot", "banana", "cherry", "date", "grape"]

# Convert keys to integers
def key_to_int(key):
    return ord(key[0])
key_values = [key_to_int(key) for key in keys]

# Set up hash table
table_size = 5
hash_table = [None] * table_size

# Node class for separate chaining
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# Division hash function
def division_hash(key, table_size):
    hash_value = key % table_size
    return hash_value  

# Multiplication hash function
def multiplication_hash(key, table_size):
    a = 0.6180339887  # Golden ratio
    hash_value = int(table_size * ((a * key) % 1))
    return hash_value  

# MD5 hash function
def md5_hash(key):
    return hashlib.md5(key.encode()).hexdigest()

# Calculate and print hash values
for i, key_value in enumerate(key_values):
    print(f"Key {i+1}: {keys[i]}")
    division_hash_value = division_hash(key_value, table_size)
    multiplication_hash_value = multiplication_hash(key_value, table_size)
    md5_value = md5_hash(keys[i])  # Calculate MD5 hash for the key
    print(f"Division Hash for '{key_value}': {division_hash_value}")
    print(f"Multiplication Hash for '{key_value}': {multiplication_hash_value}")
    print(f"MD5 Hash for '{keys[i]}': {md5_value}")  # Print the MD5 hash
    print("-" * 20)

    # Insert the key into the hash table using separate chaining
    new_node = Node(keys[i], key_value)
    if hash_table[division_hash_value] is None:
        hash_table[division_hash_value] = new_node
    else:
        current = hash_table[division_hash_value]
        while current.next:
            current = current.next
        current.next = new_node

# Print the hash table
for i in range(table_size):
    if hash_table[i] is not None:
        print(f"Index {i}:")
        current = hash_table[i]
        while current:
            print(f"    {current.key}: {current.value}")
            current = current.next

