class LostItem:
    """Represent one item reported to the campus Lost & Found system."""

    __slots__ = ("__ID", "__name", "__category", "__location", "__status")

    def __init__(self, ID, name, category, location):
        self.__ID = ID
        self.__name = name.strip()
        self.__category = category.strip()
        self.__location = location.strip()
        self.__status = "Lost"

    def get_id(self):
        return self.__ID

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_location(self):
        return self.__location

    def get_status(self):
        return self.__status

    def __str__(self):
        return (
            f"ID: {self.__ID} | Name: {self.__name} | "
            f"Category: {self.__category} | Location: {self.__location} | "
            f"Status: {self.__status}"
        )

    def __eq__(self, other):
        if isinstance(other, LostItem):
            return self.__ID == other.__ID
        else:
            return None

    def mark_claimed(self):
        """Mark this item as claimed once. Return whether it changed."""
        if self.__status == "Claimed":
            return False
        self.__status = "Claimed"
        return True