import csv
import os
from pymongo import MongoClient
import pyodbc

CSV_FILE = "BRMS_100_Records.csv"

# ---------------- CONNECTIONS ----------------

# MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mdb = mongo_client["BRMSFinal1"]
mongo_col = mdb["brms_denorm"]

# SQL Server
sql_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=WAARIHA-LENOVO\\SQLEXPRESS;"
    "DATABASE=BRMSFinal1;"
    "Trusted_Connection=yes;"
)
cursor = sql_conn.cursor()

# ---------------- MONGODB LOAD STORAGE ----------------
mongo_data = []

def load_mongodb_data():
    global mongo_data

    if mongo_col.count_documents({}) == 0:
        print("MongoDB is empty. Please insert data first (Option 2).")
        return

    mongo_data = list(mongo_col.find())
    print("MongoDB data loaded into Python dictionary.")
    print("Number of records loaded:", len(mongo_data))


# ---------------- FUNCTIONS ----------------

def load_csv():
    global csv_loaded

    if not os.path.exists(CSV_FILE):
        print("CSV file not found. Please place CSV in folder first.")
        csv_loaded = False
        return []

    with open(CSV_FILE) as f:
        data = list(csv.DictReader(f))

    csv_loaded = True
    print("CSV has been loaded successfully.")
    print("Number of records loaded from CSV:", len(data))
    return data


def insert_mongodb():
    try:
        if not csv_loaded:
            print("Please load CSV first (Option 1).")
            return
    except NameError:
        print("CSV status not found. Please load CSV first (Option 1).")
        return

    data = load_csv()
    if not data:
        print("CSV file not found or empty.")
        return

    mongo_col.delete_many({})

    denorm_docs = []

    for row in data:
        doc = {
            "route": {
                "routeId": int(row["RouteID"]),
                "source": row["Source"],
                "destination": row["Destination"],
                "distance": int(row["Distance"])
            },
            "bus": {
                "busId": int(row["BusID"]),
                "busName": row["BusName"],
                "capacity": int(row["Capacity"]),
                "routeId": int(row["RouteID"])
            },
            "passenger": {
                "passengerId": int(row["PassengerID"]),
                "name": row["PassengerName"],
                "age": int(row["Age"]),
                "gender": row["Gender"],
                "contact": row["Contact"]
            },
            "reservation": {
                "reservationId": int(row["ReservationID"]),
                "seatNo": int(row["SeatNo"]),
                "noOfSeats": int(row["NoOfSeats"]),
                "date": row["Date"]
            },
            "payment": {
                "paymentId": int(row["PaymentID"]),
                "amount": int(row["Amount"]),
                "paymentMode": row["PaymentMode"]
            }
        }
        denorm_docs.append(doc)

    mongo_col.insert_many(denorm_docs)
    print("MongoDB insertion successful.")
    print("Number of records inserted into MongoDB:", len(denorm_docs))


def insert_sql():
    try:
        if not csv_loaded:
            print("Please load CSV first (Option 1).")
            return
    except NameError:
        print("CSV status not found. Please load CSV first (Option 1).")
        return

    if mongo_col.count_documents({}) == 0:
        print("MongoDB is empty. Insert data into MongoDB first.")
        return

    cursor.execute("DELETE FROM Payment")
    cursor.execute("DELETE FROM Reservation")
    cursor.execute("DELETE FROM Passenger")
    cursor.execute("DELETE FROM Bus")
    cursor.execute("DELETE FROM Route")
    sql_conn.commit()

    routes = set()
    buses = set()
    passengers = set()

    count = 0

    for r in mongo_col.find():
        rid = r["route"]["routeId"]
        bid = r["bus"]["busId"]
        pid = r["passenger"]["passengerId"]

        if rid not in routes:
            cursor.execute(
                "INSERT INTO Route (RouteID, Source, Destination, Distance) VALUES (?,?,?,?)",
                rid,
                r["route"]["source"],
                r["route"]["destination"],
                r["route"]["distance"]
            )
            routes.add(rid)

        if bid not in buses:
            cursor.execute(
                "INSERT INTO Bus (BusID, BusName, Capacity, RouteID) VALUES (?,?,?,?)",
                bid,
                r["bus"]["busName"],
                r["bus"]["capacity"],
                rid
            )
            buses.add(bid)

        if pid not in passengers:
            cursor.execute(
                "INSERT INTO Passenger (PassengerID, Name, Age, Gender, Contact) VALUES (?,?,?,?,?)",
                pid,
                r["passenger"]["name"],
                r["passenger"]["age"],
                r["passenger"]["gender"],
                r["passenger"]["contact"]
            )
            passengers.add(pid)

        cursor.execute(
            "INSERT INTO Reservation (ReservationID, PassengerID, BusID, SeatNo, NoOfSeats, Date) VALUES (?,?,?,?,?,?)",
            r["reservation"]["reservationId"],
            pid,
            bid,
            r["reservation"]["seatNo"],
            r["reservation"]["noOfSeats"],
            r["reservation"]["date"]
        )

        cursor.execute(
            "INSERT INTO Payment (PaymentID, ReservationID, Amount, PaymentMode) VALUES (?,?,?,?)",
            r["payment"]["paymentId"],
            r["reservation"]["reservationId"],
            r["payment"]["amount"],
            r["payment"]["paymentMode"]
        )

        count += 1

    sql_conn.commit()
    print("SQL Server insertion successful.")
    print("Number of records inserted into SQL Server:", count)


def view_status():
    print("\n--- VIEW STATUS ---")

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE) as f:
            csv_count = sum(1 for _ in csv.DictReader(f))
        print("CSV Records:", csv_count)
    else:
        print("CSV Records: 0 (file not found)")

    print("MongoDB Records:", mongo_col.count_documents({}))

    cursor.execute("SELECT COUNT(*) FROM Reservation")
    print("SQL Server Records:", cursor.fetchone()[0])


def delete_csv():
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE) as f:
            count = sum(1 for _ in csv.DictReader(f))

        os.remove(CSV_FILE)
        print("CSV file deleted")
        print("CSV records deleted:", count)
    else:
        print("CSV file not found")


def delete_mongodb():
    deleted = mongo_col.delete_many({})
    print("MongoDB records deleted:", deleted.deleted_count)


def delete_sql():
    cursor.execute("DELETE FROM Payment")
    pay = cursor.rowcount

    cursor.execute("DELETE FROM Reservation")
    res = cursor.rowcount

    cursor.execute("DELETE FROM Passenger")
    pas = cursor.rowcount

    cursor.execute("DELETE FROM Bus")
    bus = cursor.rowcount

    cursor.execute("DELETE FROM Route")
    rou = cursor.rowcount

    sql_conn.commit()

    print("SQL Server records deleted:")
    print("Payment:", pay)
    print("Reservation:", res)
    print("Passenger:", pas)
    print("Bus:", bus)
    print("Route:", rou)


# ---------------- MENU ----------------

while True:
    print("""
===== BUS RESERVATION MANAGEMENT SYSTEM =====

1. Load CSV
2. Insert into MongoDB (Denormalized)
3. Load MongoDB Data
4. Insert into SQL Server (Normalized)
5. View Status
6. Delete CSV
7. Delete MongoDB
8. Delete SQL Server
9. Exit
""")

    choice = input("Enter choice: ")

    if choice == "1":
        load_csv()
    elif choice == "2":
        insert_mongodb()
    elif choice == "3":
        load_mongodb_data()
    elif choice == "4":
        insert_sql()
    elif choice == "5":
        view_status()
    elif choice == "6":
        delete_csv()
    elif choice == "7":
        delete_mongodb()
    elif choice == "8":
        delete_sql()
    elif choice == "9":
        break
    else:
        print("Invalid choice")
