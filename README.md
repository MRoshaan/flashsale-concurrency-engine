# FlashSale Engine API

A High-Concurrency backend built with FastAPI and MySQL that prevents overselling inventory during high-traffic events (e.g., Black Friday).

## The Problem (Race Conditions)
In a naive implementation, if multiple users buy an item simultaneously, the database reads the stock before it updates, resulting in overselling.
- **Test:** Simulating 20 concurrent users for 5 items.
- **Result:** System sold 20 items (Oversold by 15).

## The Solution (Pessimistic Locking)
Implemented **Row-Level Locking** using SQLAlchemy's `with_for_update()`.
- This enforces serialized access to the database rows.
- **Result:** System correctly sold exactly 5 items and rejected the rest.

## Tech Stack
- **Python / FastAPI**: Core Logic
- **MySQL**: ACID Compliant Database
- **SQLAlchemy**: ORM with Locking support