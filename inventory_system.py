"""
A simple inventory management system.

This module allows adding, removing, and querying stock levels,
as well as saving and loading the inventory from a JSON file.
"""
import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Adds a specified quantity of an item to the stock."""
    if logs is None:
        logs = []
    if not item or qty < 0:
        # Basic validation: ignore invalid items or negative quantities
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(item, qty):
    """Removes a specified quantity of an item from the stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            # Remove item from stock if quantity is zero or less
            del stock_data[item]
    except KeyError:
        # Item not in stock, do nothing
        pass


def get_qty(item):
    """Gets the current quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads the inventory data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        # If no file exists, start with an empty inventory
        stock_data = {}
    except json.JSONDecodeError:
        # If file content is invalid, start with empty inventory
        stock_data = {}


def save_data(file="inventory.json"):
    """Saves the current inventory data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)


def print_data():
    """Prints a report of all items and their quantities."""
    print("--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    for i in stock_data:
        print(f"{i} -> {stock_data[i]}")
    print("--------------------")


def check_low_items(threshold=5):
    """Returns a list of items with stock below the threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory system operations."""
    # Load existing data on startup
    load_data()
    print("--- Initial Load ---")
    print_data()

    # Add and remove items
    add_item("apple", 10)
    add_item("banana", 15)
    remove_item("apple", 3)
    remove_item("orange", 1)  # Tries to remove item that doesn't exist
    add_item("apple", 5)

    # Check quantities and low stock
    print("\n--- After Transactions ---")
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    # Save data and print final report
    save_data()
    print("\n--- Final Report (from file) ---")
    load_data()
    print_data()


if __name__ == "__main__":
    main()