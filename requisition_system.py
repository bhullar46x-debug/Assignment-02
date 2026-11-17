"""Requisition System Prototype.

Software Development Fundamentals - Final Assessment
Implements an Object-Oriented Requisition System using Python classes and methods.

Key Features:
- Encapsulates staff requisition data
- Automatic sequential ID generation (starts at 10001)
- Automatic approval threshold (< $500)
- Manager review functionality for pending requests
- Class-level statistical tracking (Total, Approved, Pending, Not approved)
"""

# Unique requisition ID counter outside the __init__ method
# As per assessment requirements, ID generation starts from 10000 + 1 (10001, 10002, ...)
requisition_id_counter = 10000


class RequisitionSystem:
    """Class to manage and process purchase requisitions."""

    # Class-level list to store all submitted requisition instances
    all_requisitions = []

    # Class-level counters to track system statistics
    total_submitted = 0
    total_approved = 0
    total_pending = 0
    total_not_approved = 0

    def __init__(self, date="", staff_id="", staff_name=""):
        """Initialize shared data for a requisition object."""
        global requisition_id_counter
        requisition_id_counter += 1
        self.requisition_id = requisition_id_counter

        # Basic details
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.items = []
        self.total = 0.0

        # Status tracking (default is always 'Pending')
        self.status = "Pending"
        self.approval_reference = "Not available"

        # Register instance in the class list and update counters
        RequisitionSystem.all_requisitions.append(self)
        RequisitionSystem.total_submitted += 1
        RequisitionSystem.total_pending += 1

    def update_status(self, new_status):
        """Update the requisition status and adjust summary statistics accordingly.

        When status transitions:
        - Decrements the count of the previous status
        - Increments the count of the new status
        """
        if self.status == new_status:
            return

        # Deduct from previous status counter
        if self.status == "Pending":
            RequisitionSystem.total_pending -= 1
        elif self.status == "Approved":
            RequisitionSystem.total_approved -= 1
        elif self.status == "Not approved":
            RequisitionSystem.total_not_approved -= 1

        # Assign new status
        self.status = new_status

        # Increment new status counter and update approval reference number
        if self.status == "Approved":
            RequisitionSystem.total_approved += 1
            # Staff ID + last 3 characters of Requisition ID
            last_three = str(self.requisition_id)[-3:]
            self.approval_reference = f"{self.staff_id}{last_three}"
        elif self.status == "Not approved":
            RequisitionSystem.total_not_approved += 1
            self.approval_reference = "Not available"
        elif self.status == "Pending":
            RequisitionSystem.total_pending += 1
            self.approval_reference = "Not available"

    def requisitions_details(self, date=None, staff_id=None, staff_name=None, items=None):
        """Accept staff details and item costs, calculate the total cost, and return it.

        Supports both automated batch assignment and interactive console input.
        """
        # Populate basic info
        if date is not None:
            self.date = date
        elif not self.date:
            self.date = input("Enter Date (DD/MM/YYYY): ")

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
            # Interactive entry loop
            print("Add items:")
            while True:
                item_name = input("Item Name: ")
                while True:
                    try:
                        item_price = float(input("Item Price ($): "))
                        break
                    except ValueError:
                        print("Invalid price! Please enter a numerical value.")

                self.items.append({"name": item_name, "price": item_price})
                self.total += item_price

                another = input("Add another item (yes/no): ").strip().lower()
                if another != "yes":
                    break

        return self.total

    # Method alias matching brief
    add_requisition = requisitions_details

    def approve_requisition(self):
        """Evaluate initial approval based on requisition total:

        - Total < $500  -> 'Approved'
        - Total >= $500 -> 'Pending'
        """
        if self.total < 500:
            self.update_status("Approved")
        else:
            self.update_status("Pending")

        return self.status

    # Method alias
    requisition_approval = approve_requisition

    def respond_requisition(self, decision):
        """Allow a manager to review a pending requisition and decide its status.

        Accepts: 'Approved', 'Not approved', or 'Pending'.
        """
        decision_clean = decision.strip().lower()

        if "not" in decision_clean or "reject" in decision_clean:
            self.update_status("Not approved")
        elif "approve" in decision_clean:
            self.update_status("Approved")
        elif "pending" in decision_clean:
            self.update_status("Pending")
        else:
            print(f"Unknown decision '{decision}'. Status remained {self.status}.")

        return self.status

    def display_requisition(self):
        """Print the formatted details of a single requisition."""
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
        """Print formatted details for all requisition instances."""
        for req in cls.all_requisitions:
            req.display_requisition()
            print()

    @classmethod
    def requisition_statistics(cls):
        """Display and return the system-wide requisition statistics."""
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
    """Execute test demonstration with custom scenario instances."""
    print("=" * 65)
    print("REQUISITION SYSTEM: TEST SIMULATION")
    print("=" * 65)

    # -------------------------------------------------------------
    # Step 1: Submit 5 unique requisitions with diverse totals
    # -------------------------------------------------------------
    print("\n--- Submitting 5 Requisitions ---\n")

    # Instance 1: Total < $500 -> Auto-Approved
    req1 = RequisitionSystem()
    req1.requisitions_details(
        date="12/08/2024",
        staff_id="MK12",
        staff_name="Mehak Sharma",
        items=[("Wireless Mouse", 60), ("Mechanical Keyboard", 120), ("Desk Mat", 45)]  # Total = $225
    )
    req1.approve_requisition()

    # Instance 2: Total >= $500 -> Pending initially
    req2 = RequisitionSystem()
    req2.requisitions_details(
        date="15/08/2024",
        staff_id="AK24",
        staff_name="Ashanjot Kaur",
        items=[("Dual Monitors", 720), ("Monitor Stand", 130), ("HDMI Cables", 50)]  # Total = $900
    )
    req2.approve_requisition()

    # Instance 3: Total >= $500 -> Pending initially
    req3 = RequisitionSystem()
    req3.requisitions_details(
        date="22/08/2024",
        staff_id="NS07",
        staff_name="Navjeet Singh",
        items=[("Developer Workstation", 2400), ("32GB RAM Upgrade", 450)]  # Total = $2850
    )
    req3.approve_requisition()

    # Instance 4: Total < $500 -> Auto-Approved
    req4 = RequisitionSystem()
    req4.requisitions_details(
        date="04/09/2024",
        staff_id="GG18",
        staff_name="Gurpal Gill",
        items=[("IDE Software License", 320), ("USB-C Docking Station", 110)]  # Total = $430
    )
    req4.approve_requisition()

    # Instance 5: Total >= $500 -> Pending initially
    req5 = RequisitionSystem()
    req5.requisitions_details(
        date="18/09/2024",
        staff_id="SV31",
        staff_name="Simran Verma",
        items=[("Motorized Standing Desk", 680), ("Ergonomic Footrest", 80)]  # Total = $760
    )
    req5.approve_requisition()

    # -------------------------------------------------------------
    # Step 2: Show initial statistics
    # -------------------------------------------------------------
    print("--- Statistics Immediately After Submission ---")
    RequisitionSystem.requisition_statistics()

    # -------------------------------------------------------------
    # Step 3: Manager reviews pending requisitions (>= $500)
    # -------------------------------------------------------------
    print("=" * 65)
    print("MANAGER RESPONSES TO PENDING REQUISITIONS (>= $500)")
    print("=" * 65)

    # Manager approves Ashanjot's request ($900)
    print("\n[Manager Action] Approving Requisition 10002 for Ashanjot Kaur ($900)...")
    req2.respond_requisition("Approved")

    # Manager rejects Navjeet's request ($2850)
    print("[Manager Action] Rejecting Requisition 10003 for Navjeet Singh ($2850)...")
    req3.respond_requisition("Not approved")

    # Manager leaves Simran's request ($760) pending further budget check
    print("[Manager Action] Leaving Requisition 10005 for Simran Verma ($760) as Pending...")
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
