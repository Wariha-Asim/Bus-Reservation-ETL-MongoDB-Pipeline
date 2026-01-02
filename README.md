# Bus-Reservation-ETL-MongoDB-Pipeline

This project demonstrates a complete ETL process for a Bus Reservation dataset.  
Data is extracted from CSV, transformed, loaded into MongoDB (denormalized), and then integrated with SQL Server in normalized form.  
It highlights real-world data cleaning, transformation, and NoSQL → SQL migration concepts.

---

## 🚀 Features

- Extract data from CSV (Bus Reservation dataset)
- Transform & clean raw data
- Load denormalized data into MongoDB
- Prepare normalized data for SQL Server
- Demonstrates ETL best practices
- Simple, readable Python code — great for learning

---

## 🛠️ Tech Stack

- **Python**
- **MongoDB**
- **SQL Server**
- CSV (source dataset)

---

## 📂 Project Structure

Bus-Reservation-ETL-MongoDB-Pipeline
│
├── BRMS_100_Records.csv # Source dataset
├── db_creation.py # MongoDB connection & setup
├── final.py # ETL processing logic
└── project queries.sql # SQL queries for normalized data

---

## 🔄 ETL Flow (High-Level)

1️⃣ **Extract** – Read bus reservation data from CSV  
2️⃣ **Transform** – Clean & structure data  
3️⃣ **Load (NoSQL)** – Save denormalized data to MongoDB  
4️⃣ **Migrate (SQL)** – Prepare normalized tables for SQL Server

---

## ▶️ How to Run

### 1️⃣ Install dependencies
pip install pymongo

sql
Copy code

### 2️⃣ Start MongoDB (local)

MongoDB must be running on:

mongodb://localhost:27017/


### 3️⃣ Run database setup
python db_creation.py



### 4️⃣ Run ETL script
python final.py


---

## 🗄️ SQL Queries

All SQL examples are included in:

project queries.sql

These can be executed in SQL Server after ETL completes.

---

## 🔐 Best Practices Used

- No credentials stored in code  
- Environment-variable support for MongoDB URI  
- Clear separation of ETL logic and setup scripts  

---

## 📌 Notes

- Default MongoDB DB: **BRMSFinal1**  
- Collection name: **brms_denorm**  
- You can replace the CSV with a larger dataset if needed.

---

---

🎉 **Feel free to fork, improve, and experiment!**
