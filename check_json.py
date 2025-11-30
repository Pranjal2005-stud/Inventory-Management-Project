import json

print("=== Checking inventory.json ===")
with open('inventory.json', 'r') as f:
    inventory_data = json.load(f)
    print(f"Type: {type(inventory_data)}")
    print(f"Length: {len(inventory_data)}")
    if inventory_data:
        print("First item structure:")
        print(inventory_data[0])
        print("\nAll keys in first item:")
        print(list(inventory_data[0].keys()))

print("\n=== Checking categories.json ===")
with open('categories.json', 'r') as f:
    categories_data = json.load(f)
    print(f"Type: {type(categories_data)}")
    print(f"Length: {len(categories_data)}")
    if categories_data:
        print("First item structure:")
        print(categories_data[0])
