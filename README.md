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
##🚀 How to Run Locally
1. Clone the Repository
Bash

git clone [https://github.com/MRoshaan/flashsale-concurrency-engine.git](https://github.com/MRoshaan/flashsale-concurrency-engine.git)
cd flashsale-concurrency-engine
2. Set up Virtual Environment
Bash

python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Configure Database
Create a .env file in the root directory (this file is ignored by Git for security). Add your MySQL credentials:

Code snippet

DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/flashsale_db
5. Run the Server
Bash

uvicorn app.main:app --reload
🧪 Simulation: The "Attack" Script
To prove the system works, this project includes a stress-test script (attack.py) that launches 20 concurrent threads trying to buy an item with only 5 units in stock.

Keep the server running in Terminal 1.

Open a new terminal, activate the environment, and run:

Bash

python attack.py
Expected Result: You will see exactly 5 "Sold!" messages and 15 "Out of Stock" failures. If the locking implementation were broken, you would see 20 "Sold!" messages.
---
## 📂 Project Structure
```bash
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
