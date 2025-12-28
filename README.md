# ⚡ FlashSale Concurrency Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green) ![MySQL](https://img.shields.io/badge/Database-MySQL-orange) ![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)

A robust, high-concurrency backend API built with **FastAPI** and **MySQL**. This project demonstrates how to handle **Race Conditions** in inventory systems (like Black Friday sales) using **ACID transactions** and **Pessimistic Locking**.

---

## 🧐 The Problem: Race Conditions
In a high-traffic environment, if multiple users try to buy the last item at the exact same millisecond, a standard "Read-Modify-Write" approach fails.
1. **User A** reads stock: 1
2. **User B** reads stock: 1 (before User A updates it)
3. **User A** buys item. (Stock -> 0)
4. **User B** buys item. (Stock -> -1)

**Result:** The system oversells inventory, leading to data corruption and business loss.

## 🛠 The Solution: Pessimistic Locking
This engine solves the problem by implementing **Row-Level Locking** using SQLAlchemy's `with_for_update()`.
* When a user attempts to buy an item, the database **locks** that specific product row.
* Other concurrent requests are forced to wait in a queue until the lock is released.
* This ensures that stock checks and updates happen atomically (one at a time).

---

## ⚙️ Tech Stack
* **Framework:** Python / FastAPI
* **Database:** MySQL (Relational / ACID Compliant)
* **ORM:** SQLAlchemy (Implemented `SELECT ... FOR UPDATE`)
* **Validation:** Pydantic Schemas
* **Testing:** Multi-threaded Python script to simulate concurrent attacks.

---

## 🚀 Run Locally

1. **Clone the Repository**
    ```bash
    git clone [https://github.com/MRoshaan/flashsale-concurrency-engine.git](https://github.com/MRoshaan/flashsale-concurrency-engine.git)
    cd flashsale-concurrency-engine
    ```

2. **Create & Activate Virtual Environment**
    ```bash
    python -m venv venv
    
    # Windows
    .\venv\Scripts\activate
    
    # macOS / Linux
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    Create a `.env` file in the project root:
    ```ini
    DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/flashsale_db
    ```

5. **Run the Server**
    ```bash
    uvicorn app.main:app --reload
    ```

---

## 🧪 Concurrency Stress Test (Proof of Correctness)
To prove that the locking works, this project includes a stress-test script (`attack.py`).

### Scenario
* **Stock available:** 5 units
* **Concurrent buyers:** 20 threads

### Run the Test
1. Keep the FastAPI server running.
2. Open a new terminal.
3. Activate the virtual environment.
4. Run the script:
    ```bash
    python attack.py
    ```

### ✅ Expected Output
```text
5 successful purchases (Sold!)
15 failures (Out of Stock)
## 📂 Project Structure
```bash
---
flashsale_engine/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI Endpoints
│   ├── database.py      # DB Connection & Session
│   ├── models.py        # SQLAlchemy Tables
│   └── schemas.py       # Pydantic Validators
│
├── .env                 # Environment Variables (Ignored by Git)
├── attack.py            # Concurrency Stress Test Script
└── requirements.txt     # Dependencies
