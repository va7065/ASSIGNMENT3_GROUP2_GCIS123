from lost_item import LostItem


class LostFoundSystem:
    """Manage campus lost-item records."""

    def __init__(self):
        self.items = []

    def add_item(self, item):
        if not isinstance(item, LostItem):
            raise TypeError("Only LostItem objects can be added.")

        if any(existing.get_id() == item.get_id() for existing in self.items):
            return False

        self.items.append(item)
        return True

    def search_item(self, item_id):
        for item in self.items:
            if item.get_id() == item_id:
                return item
        return None

    def claim_item(self, item_id):
        item = self.search_item(item_id)
        if item is None:
            return False
        return item.mark_claimed()

    def display_items(self):
        if not self.items:
            print("No items are currently registered.")
            return

        for item in self.items:
            print(item)  # Uses LostItem.__str__()

    def save_items(self, filename):
        """Save all records as comma-separated lines."""
        try:
            with open(filename, "w", encoding="utf-8") as file:
                for item in self.items:
                    record = (
                        f"{item.get_id()},{item.get_name()},"
                        f"{item.get_category()},{item.get_location()},"
                        f"{item.get_status()}\n"
                    )
                    file.write(record)
            return True
        except OSError as error:
            print(f"Error saving file: {error}")
            return False

    def load_items(self, filename):
        """
        Load valid records from a file.

        A successfully opened file replaces the current collection.
        Invalid records and duplicate IDs are skipped. If opening fails,
        the existing collection is left unchanged.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: File '{filename}' was not found.")
            return 0
        except OSError as error:
            print(f"Error opening file: {error}")
            return 0

        loaded_items = []
        seen_ids = set()

        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue

            fields = line.split(",")
            if len(fields) != 5:
                print(f"Skipping invalid record on line {line_number}: expected 5 fields.")
                continue

            raw_id, name, category, location, status = fields
            try:
                item_id = int(raw_id.strip())
                if item_id <= 0:
                    raise ValueError("ID must be positive.")

                name = name.strip()
                category = category.strip()
                location = location.strip()
                status = status.strip()

                if not name or not category or not location:
                    raise ValueError("Text fields cannot be empty.")
                if status not in ("Lost", "Claimed"):
                    raise ValueError("Status must be Lost or Claimed.")
                if item_id in seen_ids:
                    raise ValueError("Duplicate item ID.")

                item = LostItem(item_id, name, category, location)
                if status == "Claimed":
                    item.mark_claimed()

                loaded_items.append(item)
                seen_ids.add(item_id)

            except (ValueError, TypeError) as error:
                print(f"Skipping invalid record on line {line_number}: {error}")

        # Replace only after the file was opened and all lines were processed.
        self.items = loaded_items
        return len(self.items)
