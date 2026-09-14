"""
HostelOps - Seed Data Script
Populates the hostelops_db database with sample data for development.
"""

import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "hostelops_db",
    "charset": "utf8mb4",
}


def run_seed():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # 1. Insert owner user
        cursor.execute(
            """INSERT INTO users (name, email, phone, password_hash, role)
               VALUES (%s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE name=name""",
            ("Rahul Sharma", "rahul@hostelops.in", "9876543210", "hashed_password_123", "OWNER"),
        )
        owner_id = cursor.lastrowid or 1

        # 2. Insert hostel
        cursor.execute(
            """INSERT INTO hostels (owner_id, name, address, city, state, pincode, total_rooms, contact_phone)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE name=name""",
            (owner_id, "Sunshine PG", "123 MG Road, Koramangala", "Bangalore", "Karnataka", "560034", 15, "9876543210"),
        )
        hostel_id = cursor.lastrowid or 1

        # 3. Insert 15 rooms across 3 floors
        rooms_data = [
            (hostel_id, "101", 1, "SINGLE", 1, 8000.00, 8000.00, "OCCUPIED"),
            (hostel_id, "102", 1, "SINGLE", 1, 8000.00, 8000.00, "OCCUPIED"),
            (hostel_id, "103", 1, "DOUBLE", 2, 7000.00, 7000.00, "PARTIALLY_OCCUPIED"),
            (hostel_id, "104", 1, "DOUBLE", 2, 7000.00, 7000.00, "VACANT"),
            (hostel_id, "105", 1, "TRIPLE", 3, 5500.00, 5500.00, "OCCUPIED"),
            (hostel_id, "201", 2, "SINGLE", 1, 9000.00, 9000.00, "OCCUPIED"),
            (hostel_id, "202", 2, "SINGLE", 1, 9000.00, 9000.00, "VACANT"),
            (hostel_id, "203", 2, "DOUBLE", 2, 8000.00, 8000.00, "OCCUPIED"),
            (hostel_id, "204", 2, "DOUBLE", 2, 8000.00, 8000.00, "OCCUPIED"),
            (hostel_id, "205", 2, "TRIPLE", 3, 6000.00, 6000.00, "PARTIALLY_OCCUPIED"),
            (hostel_id, "301", 3, "SINGLE", 1, 10000.00, 10000.00, "OCCUPIED"),
            (hostel_id, "302", 3, "SINGLE", 1, 10000.00, 10000.00, "VACANT"),
            (hostel_id, "303", 3, "DOUBLE", 2, 9000.00, 9000.00, "OCCUPIED"),
            (hostel_id, "304", 3, "DOUBLE", 2, 9000.00, 9000.00, "VACANT"),
            (hostel_id, "305", 3, "TRIPLE", 3, 7000.00, 7000.00, "OCCUPIED"),
        ]

        room_ids = []
        for r in rooms_data:
            cursor.execute(
                """INSERT INTO rooms (hostel_id, room_number, floor, room_type, capacity, rent_amount, security_deposit, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE room_number=room_number""",
                r,
            )
            room_ids.append(cursor.lastrowid or (rooms_data.index(r) + 1))

        # 4. Insert tenants
        tenants_data = [
            (room_ids[0], "Amit Verma", "9800000001", "amit@email.com", "Vijay Verma", "9800000099", "2025-01-15", None, 5, "ACTIVE"),
            (room_ids[1], "Priya Singh", "9800000002", "priya@email.com", "Sunita Singh", "9800000098", "2025-02-01", None, 5, "ACTIVE"),
            (room_ids[2], "Rohit Kumar", "9800000003", "rohit@email.com", "Rakesh Kumar", "9800000097", "2025-01-20", None, 10, "ACTIVE"),
            (room_ids[2], "Deepak Joshi", "9800000004", "deepak@email.com", "Manoj Joshi", "9800000096", "2025-03-01", None, 5, "ACTIVE"),
            (room_ids[4], "Sneha Patel", "9800000005", "sneha@email.com", "Ketan Patel", "9800000095", "2025-01-10", None, 5, "ACTIVE"),
            (room_ids[4], "Vikram Rao", "9800000006", "vikram@email.com", "Anand Rao", "9800000094", "2025-02-15", None, 10, "ACTIVE"),
            (room_ids[4], "Nisha Gupta", "9800000007", "nisha@email.com", "Sunil Gupta", "9800000093", "2025-04-01", None, 5, "ACTIVE"),
            (room_ids[5], "Arjun Mehta", "9800000008", "arjun@email.com", "Prakash Mehta", "9800000092", "2025-01-05", None, 5, "ACTIVE"),
            (room_ids[7], "Kavita Sharma", "9800000009", "kavita@email.com", "Ramesh Sharma", "9800000091", "2025-03-10", None, 5, "ACTIVE"),
            (room_ids[8], "Suresh Nair", "9800000010", "suresh@email.com", "Gopal Nair", "9800000090", "2025-02-20", None, 5, "ACTIVE"),
            (room_ids[10], "Pooja Reddy", "9800000011", "pooja@email.com", "Krishna Reddy", "9800000089", "2025-01-25", None, 5, "ACTIVE"),
            (room_ids[12], "Rajesh Iyer", "9800000012", "rajesh@email.com", "Venkat Iyer", "9800000088", "2025-04-15", None, 5, "ACTIVE"),
        ]

        tenant_ids = []
        for t in tenants_data:
            cursor.execute(
                """INSERT INTO tenants (room_id, name, phone, email, emergency_contact_name, emergency_contact_phone, move_in_date, move_out_date, rent_due_day, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE phone=phone""",
                t,
            )
            tenant_ids.append(cursor.lastrowid or (tenants_data.index(t) + 1))

        # 5. Insert vendors
        vendors_data = [
            ("Raj Plumbing", "9700000001", "raj@plumbing.in", "PLUMBING", 4.7, 550.00, "Koramangala, HSR Layout", "AVAILABLE", 45, 42),
            ("Quick Fix Plumbing", "9700000002", "quick@fix.in", "PLUMBING", 4.1, 450.00, "Koramangala, BTM Layout", "AVAILABLE", 30, 27),
            ("Venkatesh Electricals", "9700000003", "venki@electrical.in", "ELECTRICAL", 4.5, 600.00, "Koramangala, JP Nagar", "AVAILABLE", 60, 58),
            ("Spark Electric", "9700000004", "spark@electric.in", "ELECTRICAL", 3.9, 400.00, "HSR Layout, BTM", "BUSY", 25, 22),
            ("CoolAir AC Services", "9700000005", "cool@air.in", "AC", 4.8, 800.00, "Bangalore South", "AVAILABLE", 80, 78),
            ("FreshClean Services", "9700000006", "fresh@clean.in", "CLEANING", 4.3, 350.00, "Koramangala", "AVAILABLE", 100, 95),
            ("WoodWorks Carpentry", "9700000007", "wood@works.in", "CARPENTRY", 4.6, 700.00, "BTM Layout, JP Nagar", "AVAILABLE", 40, 38),
            ("HomeCare General", "9700000008", "home@care.in", "GENERAL", 4.0, 500.00, "Bangalore", "UNAVAILABLE", 55, 50),
        ]

        vendor_ids = []
        for v in vendors_data:
            cursor.execute(
                """INSERT INTO vendors (name, phone, email, category, rating, average_cost, service_area, availability, total_jobs, successful_jobs)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE phone=phone""",
                v,
            )
            vendor_ids.append(cursor.lastrowid or (vendors_data.index(v) + 1))

        # 6. Insert rent payments for current month
        import datetime
        today = datetime.date.today()
        due_date = today.replace(day=5) if today.day >= 5 else today

        for i, tid in enumerate(tenant_ids):
            room_idx = [0, 1, 2, 2, 4, 4, 4, 5, 7, 8, 10, 12][i]
            amount = rooms_data[room_idx][5]  # rent_amount

            # Most paid, some pending, one overdue
            if i < 8:
                status = "PAID"
                paid_date = due_date
            elif i == 10:
                status = "OVERDUE"
                paid_date = None
            else:
                status = "PENDING"
                paid_date = None

            cursor.execute(
                """INSERT INTO rent_payments (tenant_id, amount, due_date, paid_date, status, payment_method, notes)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE status=status""",
                (tid, amount, due_date, paid_date, status, "UPI" if status == "PAID" else None, "Monthly rent" if status == "PAID" else None),
            )

        conn.commit()
        print("Seed data inserted successfully!")
        print(f"  - 1 owner (Rahul Sharma)")
        print(f"  - 1 hostel (Sunshine PG)")
        print(f"  - 15 rooms")
        print(f"  - 12 tenants")
        print(f"  - 8 vendors")
        print(f"  - 12 rent payments")

    except Exception as e:
        conn.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_seed()
