# 💈 Barber Booking Telegram Bot

A Telegram-based booking system for a barbershop with full appointment management, FSM-based flow, and admin notifications.

---

## 🚀 Features

- 📅 Step-by-step booking system (FSM)
- 👨‍💼 Multiple barbers support
- ⏰ Time slot validation (no double bookings)
- 🧾 Personal user appointments list
- ❌ Appointment cancellation
- 🔔 Admin notifications on new bookings
- 📊 Basic admin statistics panel

---

## 🧠 Architecture

The project is structured using a modular layered architecture:

- **bot/** — Telegram handlers (UI layer)
- **services/** — business logic (booking, notifications)
- **db/** — database layer (SQLite queries)
- **utils/** — helper functions
- **config/** — environment configuration

This separation allows scalability and easy maintenance.

---

## 🛠 Tech Stack

- Python 3.11+
- Aiogram 3.x
- SQLite (aiosqlite)
- FSM (Finite State Machine)

---

## ⚙️ Installation

```bash
git clone https://github.com/funnyvoidd/barber-bot
cd barber-bot
pip install -r requirements.txt
```
---
## 🔐 Environment variables

Create ```.env``` file:
```
BOT_TOKEN=your_token_here
ADMIN_ID=your_telegram_id
```
---

## ▶️ Run bot

```bash
python main.py
```

## 📊 Admin features

Admins can:

* View all bookings
* Check statistics
* Receive real-time booking notifications

---

## 📌 Project purpose

This project was built as a portfolio backend case demonstrating:

* FSM workflow design
* Async Python architecture
* Modular backend structure
* Telegram bot development
* SQLite data modeling

---

## 📷 Future improvements

* PostgreSQL migration
* Redis caching
* Full admin CRM dashboard
* Booking status system (pending/confirmed/canceled)
* Web admin panel (FastAPI)
