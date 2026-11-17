"""Requisition System Prototype.

Software Development Fundamentals - Final Assessment (Task 1)
Implements an Object-Oriented Requisition System utilizing Python classes and methods.
"""

# Global variable to track the unique requisition ID counter outside the __init__ method
# As defined in Assessment 1, unique IDs start with a counter plus 10000 (10001, 10002, etc.)
requisition_id_counter = 10000


class RequisitionSystem:
    """Class encapsulating the functionality of the Requisition System."""

    def __init__(self, date="", staff_id="", staff_name=""):
        """Initialize shared data for a requisition.

        Parameters:
            date (str): Date of the requisition submission (DD/MM/YYYY)
            staff_id (str): Unique identifier of the staff member
            staff_name (str): Full name of the staff member
        """
        global requisition_id_counter
        # Increment global counter and assign unique Requisition ID
        requisition_id_counter += 1
        self.requisition_id = requisition_id_counter

        # Shared data attributes
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.items = []              # List of item dictionaries: [{'name': ..., 'price': ...}]
        self.total = 0.0             # Calculated total of requisition items
        self.status = "Pending"      # Default status as required: 'Pending'
        self.approval_reference = "N/A"

    def requisitions_details(self, date=None, staff_id=None, staff_name=None, items=None):
        """Submit basic information and accept a list of requisition items with the cost of each,

        then calculate and return the total cost.

        Can be called with arguments directly or interactively via user input.
        """
        # Collect basic staff information if not already provided
        if date is not None:
            self.date = date
        elif not self.date:
            self.date = input("Enter Date (e.g., DD/MM/YYYY): ")

        if staff_id is not None:
            self.staff_id = staff_id
        elif not self.staff_id:
            self.staff_id = input("Enter Staff ID: ")

        if staff_name is not None:
            self.staff_name = staff_name
        elif not self.staff_name:
            self.staff_name = input("Enter Staff Name: ")

        # Process requisition items
        if items is not None:
            # Accepts a list of tuples/lists [('Item Name', price), ...] or dicts [{'name': ..., 'price': ...}]
            self.items = []
            self.total = 0.0
            for item in items:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    name, price = item[0], float(item[1])
                    self.items.append({"name": name, "price": price})
                    self.total += price
                elif isinstance(item, dict):
                    name = item.get("name", "Item")
                    price = float(item.get("price", 0.0))
                    self.items.append({"name": name, "price": price})
                    self.total += price
        else:
            # Interactive entry matching Assessment 1 workflow
            print("Add items:")
            while True:
                item_name = input("Item Name: ")
                while True:
                    try:
                        item_price = float(input("Item Price ($): "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a numerical price.")

                self.items.append({"name": item_name, "price": item_price})
                self.total += item_price

                another = input("Add another item (yes/no): ").strip().lower()
                if another != "yes":
                    break

        return self.total

    # Method alias matching brief phrasing: 'add a requisition'
    add_requisition = requisitions_details

    def approve_requisition(self):
        """Decide if a requisition is approved based on the requisition total.

        Logic defined from Assessment 1:
        - Default status is 'Pending'.
        - If Total < $500:
            Status is set to 'Approved'.
            Approval Reference Number is generated: Staff ID followed by the last 3 characters of Requisition ID.
        - If Total >= $500:
            Status remains 'Pending'.
            Approval Reference Number is 'N/A'.

        Updates self.status and self.approval_reference automatically.
        Returns the updated status.
        """
        if self.total < 500:
            self.status = "Approved"
            # Staff ID followed by the last three characters of the Requisition ID
            last_three_chars = str(self.requisition_id)[-3:]
            self.approval_reference = f"{self.staff_id}{last_three_chars}"
        else:
            self.status = "Pending"
            self.approval_reference = "N/A"

        return self.status

    # Method alias matching brief naming: 'requisition_approval'
    requisition_approval = approve_requisition

    def display_requisition(self):
        """Display the requisition summary in the format specified in Assessment 1."""
        print("\nPrinting requisitions:")
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: ${self.total:.2f}")
        print(f"Status: {self.status}")
        print(f"Approval Reference Number: {self.approval_reference}")

    # Method alias matching brief naming: 'display_requisitions'
    display_requisitions = display_requisition


# Alias for class name flexibility
Requisition = RequisitionSystem


def run_tests():
    """Run test cases creating multiple instances to demonstrate functionality."""
    print("=" * 60)
    print("TESTING REQUISITION SYSTEM INSTANCES (AUTOMATED TEST)")
    print("=" * 60)

    # Instance 1: Total < $500 (Expect: Approved with Reference Number)
    print("\n--- Test Instance 1: Total < $500 ---")
    req1 = RequisitionSystem()
    req1.requisitions_details(
        date="03/04/2024",
        staff_id="FN19",
        staff_name="John Paul",
        items=[("Coffee", 200), ("Paper", 100), ("Pen", 50)]
    )
    req1.approve_requisition()
    req1.display_requisition()

    # Instance 2: Total >= $500 (Expect: Pending, Reference Number N/A)
    print("\n--- Test Instance 2: Total >= $500 ---")
    req2 = RequisitionSystem()
    req2.requisitions_details(
        date="04/04/2024",
        staff_id="MK42",
        staff_name="Sarah Connor",
        items=[("Monitor", 450), ("Keyboard", 80), ("Mouse", 45)]
    )
    req2.approve_requisition()
    req2.display_requisition()


if __name__ == "__main__":
    # Run test instances demonstrating OOP capabilities
    run_tests()
