"""Requisition System Prototype.

Software Development Fundamentals - Final Assessment
Implements an Object-Oriented Requisition System using Python classes and methods.
Features:
- Encapsulation of requisition information
- Unique auto-incrementing ID tracking
- Automatic approval for requisitions under $500
- Manager response functionality (Approved, Not approved, Pending)
- Requisition statistics tracking and reporting
"""

# Global variable to track the unique requisition ID counter outside the __init__ method
# As per Assessment 1, IDs start from 10000 + 1 (10001, 10002, ...)
requisition_id_counter = 10000


class RequisitionSystem:
    """Class to implement the functionality of the requisition system."""

    # Class-level list to store all submitted requisition objects
    all_requisitions = []

    # Class-level counters to track system statistics
    total_submitted = 0
    total_approved = 0
    total_pending = 0
    total_not_approved = 0

    def __init__(self, date="", staff_id="", staff_name=""):
        """Initialize shared data for each requisition instance."""
        global requisition_id_counter
        requisition_id_counter += 1
        self.requisition_id = requisition_id_counter

        # Basic requisition information
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.items = []
        self.total = 0.0

        # Default status is 'Pending'
        self.status = "Pending"
        self.approval_reference = "Not available"

        # Record this requisition and update statistics
        RequisitionSystem.all_requisitions.append(self)
        RequisitionSystem.total_submitted += 1
        RequisitionSystem.total_pending += 1

    def update_status(self, new_status):
        """Helper method to update the status and adjust statistics accordingly.

        When a requisition moves from Pending to Approved or Not approved:
        - pending count decreases by 1
        - approved or not approved count increases by 1
        """
        if self.status == new_status:
            return

        # Deduct from previous status count
        if self.status == "Pending":
            RequisitionSystem.total_pending -= 1
        elif self.status == "Approved":
            RequisitionSystem.total_approved -= 1
        elif self.status == "Not approved":
            RequisitionSystem.total_not_approved -= 1

        # Apply new status
        self.status = new_status

        # Add to new status count and update reference number
        if self.status == "Approved":
            RequisitionSystem.total_approved += 1
            # Staff ID followed by the last three characters of the Requisition ID
            last_three = str(self.requisition_id)[-3:]
            self.approval_reference = f"{self.staff_id}{last_three}"
        elif self.status == "Not approved":
            RequisitionSystem.total_not_approved += 1
            self.approval_reference = "Not available"
        elif self.status == "Pending":
            RequisitionSystem.total_pending += 1
            self.approval_reference = "Not available"

    def requisitions_details(self, date=None, staff_id=None, staff_name=None, items=None):
        """Submit basic information and accept items with their prices,

        then calculate and return the total cost.
        Can be used interactively or with direct parameters.
        """
        # Set date, staff_id, staff_name if provided; otherwise ask user if missing
        if date is not None:
            self.date = date
        elif not self.date:
            self.date = input("Enter Date: ")

        if staff_id is not None:
            self.staff_id = staff_id
        elif not self.staff_id:
            self.staff_id = input("Enter Staff ID: ")

        if staff_name is not None:
            self.staff_name = staff_name
        elif not self.staff_name:
            self.staff_name = input("Enter Staff Name: ")

        # Process list of items
        if items is not None:
            self.items = []
            self.total = 0.0
            for item in items:
                if isinstance(item, (list, tuple)):
                    name, price = item[0], float(item[1])
                    self.items.append({"name": name, "price": price})
                    self.total += price
                elif isinstance(item, dict):
                    name = item.get("name", "Item")
                    price = float(item.get("price", 0.0))
                    self.items.append({"name": name, "price": price})
                    self.total += price
        else:
            # Interactive entry
            print("Add items:")
            while True:
                item_name = input("Item Name: ")
                while True:
                    try:
                        item_price = float(input("Item Price ($): "))
                        break
                    except ValueError:
                        print("Invalid price. Please enter a numerical value.")

                self.items.append({"name": item_name, "price": item_price})
                self.total += item_price

                another = input("Add another item (yes/no): ").strip().lower()
                if another != "yes":
                    break

        return self.total

    # Method alias
    add_requisition = requisitions_details

    def approve_requisition(self):
        """Decide if a requisition is approved based on the requisition total.

        - If Total < $500: Automatically sets status to 'Approved'
        - If Total >= $500: Sets/leaves status as 'Pending'
        """
        if self.total < 500:
            self.update_status("Approved")
        else:
            self.update_status("Pending")

        return self.status

    # Method alias
    requisition_approval = approve_requisition

    def respond_requisition(self, decision):
        """Allows a manager to respond to a pending requisition.

        Parameters:
            decision (str): 'Approved', 'Not approved', or 'Pending'
        """
        decision_clean = decision.strip().lower()

        if "not" in decision_clean or "reject" in decision_clean:
            self.update_status("Not approved")
        elif "approve" in decision_clean:
            self.update_status("Approved")
        elif "pending" in decision_clean:
            self.update_status("Pending")
        else:
            print(f"Invalid decision '{decision}'. Status remained {self.status}.")

        return self.status

    def display_requisition(self):
        """Display information for this single requisition."""
        # Format total cleanly (e.g. $450 if integer, or $450.50 if decimal)
        if self.total.is_integer():
            total_display = f"${int(self.total)}"
        else:
            total_display = f"${self.total:.2f}"

        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: {total_display}")
        print(f"Status: {self.status}")
        print(f"Approval Reference Number: {self.approval_reference}")

    @classmethod
    def display_requisitions(cls):
        """Print information for all requisition objects."""
        for req in cls.all_requisitions:
            req.display_requisition()
            print()  # Empty line between requisitions as shown in brief

    @classmethod
    def requisition_statistics(cls):
        """Display and return the statistical information for all requisitions."""
        print("Statistics:")
        print("Displaying the Requisition Statistics\n")
        print(f"The total number of requisitions submitted: {cls.total_submitted}\n")
        print(f"The total number of approved requisitions: {cls.total_approved}\n")
        print(f"The total number of pending requisitions: {cls.total_pending}\n")
        print(f"The total number of not approved requisitions: {cls.total_not_approved}\n")

        return {
            "total_submitted": cls.total_submitted,
            "total_approved": cls.total_approved,
            "total_pending": cls.total_pending,
            "total_not_approved": cls.total_not_approved
        }


# Class alias for convenience
Requisition = RequisitionSystem


def main():
    """Test the program by creating 5 instances and simulating manager responses."""
    print("=" * 65)
    print("REQUISITION SYSTEM: TEST SIMULATION")
    print("=" * 65)

    # -------------------------------------------------------------
    # Step 1: Submit at least 5 requisitions (under $500 & >= $500)
    # -------------------------------------------------------------
    print("\n--- Submitting 5 Requisitions ---\n")

    # Requisition 1: Total < $500 -> Auto-Approved
    req1 = RequisitionSystem()
    req1.requisitions_details(
        date="03/04/2024",
        staff_id="FN19",
        staff_name="John Paul",
        items=[("Office Supplies", 250), ("Coffee", 200)]  # Total = $450
    )
    req1.approve_requisition()

    # Requisition 2: Total >= $500 -> Pending
    req2 = RequisitionSystem()
    req2.requisitions_details(
        date="05/04/2024",
        staff_id="FN20",
        staff_name="Tracy Brown",
        items=[("Office Desk", 700), ("Ergonomic Chair", 300)]  # Total = $1000
    )
    req2.approve_requisition()

    # Requisition 3: Total >= $500 -> Pending
    req3 = RequisitionSystem()
    req3.requisitions_details(
        date="07/05/2024",
        staff_id="FN15",
        staff_name="Emma Wellington",
        items=[("High-End Server", 3000), ("Network Switch", 500)]  # Total = $3500
    )
    req3.approve_requisition()

    # Requisition 4: Total < $500 -> Auto-Approved
    req4 = RequisitionSystem()
    req4.requisitions_details(
        date="03/05/2024",
        staff_id="FN02",
        staff_name="Catlin White",
        items=[("Printer Cartridges", 340), ("Paper Bundles", 150)]  # Total = $490
    )
    req4.approve_requisition()

    # Requisition 5: Total >= $500 -> Pending
    req5 = RequisitionSystem()
    req5.requisitions_details(
        date="10/05/2024",
        staff_id="FN08",
        staff_name="David Miller",
        items=[("Laptop", 650), ("Backpack", 100)]  # Total = $750
    )
    req5.approve_requisition()

    # -------------------------------------------------------------
    # Step 2: Display Statistics after initial submissions
    # -------------------------------------------------------------
    print("--- Statistics Immediately After Submission ---")
    RequisitionSystem.requisition_statistics()

    # -------------------------------------------------------------
    # Step 3: Manager responds to requisitions with total >= $500
    # -------------------------------------------------------------
    print("=" * 65)
    print("MANAGER RESPONSES TO PENDING REQUISITIONS (>= $500)")
    print("=" * 65)

    # Manager approves Requisition 2 ($1000)
    print("\n[Manager Action] Approving Requisition 10002 ($1000)...")
    req2.respond_requisition("Approved")

    # Manager rejects Requisition 3 ($3500)
    print("[Manager Action] Rejecting Requisition 10003 ($3500)...")
    req3.respond_requisition("Not approved")

    # Manager leaves Requisition 5 ($750) as Pending
    print("[Manager Action] Leaving Requisition 10005 ($750) as Pending...")
    req5.respond_requisition("Pending")

    # -------------------------------------------------------------
    # Step 4: Display all requisitions and updated statistics
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print("DISPLAYING ALL REQUISITIONS")
    print("=" * 65 + "\n")
    RequisitionSystem.display_requisitions()

    print("=" * 65)
    print("UPDATED REQUISITION STATISTICS")
    print("=" * 65 + "\n")
    RequisitionSystem.requisition_statistics()


if __name__ == "__main__":
    main()
