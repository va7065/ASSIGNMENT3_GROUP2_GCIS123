from lost_item import LostItem
from lost_found_system import LostFoundSystem


def get_positive_integer(prompt):
    """Keep asking until the user enters a positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Enter a whole number.")


def get_non_empty_text(prompt):
    """Keep asking until the user enters non-empty text without commas."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty.")
        elif "," in value:
            print("Commas are not allowed in text fields.")
        else:
            return value


def main():
    system = LostFoundSystem()

    while True:
        print("\n===== CAMPUS LOST & FOUND =====")
        print("1. Register Item")
        print("2. Search")
        print("3. Claim")
        print("4. Display All")
        print("5. Save")
        print("6. Load")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            item_id = get_positive_integer("Enter item ID: ")
            name = get_non_empty_text("Enter item name: ")
            category = get_non_empty_text("Enter category: ")
            location = get_non_empty_text("Enter location: ")

            try:
                item = LostItem(item_id, name, category, location)
                if system.add_item(item):
                    print("Item registered successfully.")
                else:
                    print("An item with that ID already exists.")
            except (ValueError, TypeError) as error:
                print(f"Could not register item: {error}")

        elif choice == "2":
            item_id = get_positive_integer("Enter item ID to search: ")
            item = system.search_item(item_id)
            if item is None:
                print("Item not found.")
            else:
                print(item)

        elif choice == "3":
            item_id = get_positive_integer("Enter item ID to claim: ")
            item = system.search_item(item_id)
            if item is None:
                print("Item not found.")
            elif system.claim_item(item_id):
                print("Item successfully marked as Claimed.")
            else:
                print("This item has already been claimed.")

        elif choice == "4":
            system.display_items()

        elif choice == "5":
            filename = input("Enter filename to save to (e.g. items.txt): ").strip()
            if not filename:
                print("Filename cannot be empty.")
            elif system.save_items(filename):
                print(f"Records saved to '{filename}'.")

        elif choice == "6":
            filename = input("Enter filename to load (e.g. items.txt): ").strip()
            if not filename:
                print("Filename cannot be empty.")
            else:
                count = system.load_items(filename)
                print(f"Loaded {count} valid item(s).")

        elif choice == "7":
            print("Exiting Campus Lost & Found. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
