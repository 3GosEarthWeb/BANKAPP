# 🏦 ORiem Capital – Backend API

A secure, scalable backend for **ORiem Capital**, a modern digital banking platform with customer accounts, internal transfers, bill payments, card management, loans, audit logs, and admin tools. Built with **FastAPI**, **PostgreSQL**, and **JWT authentication**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-brightgreen)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 📚 Table of Contents

- [🏦 ORiem Capital – Backend API](#-oriem-capital--backend-api)
  - [📚 Table of Contents](#-table-of-contents)
  - [🚀 Core Features](#-core-features)
  - [⚙️ Tech Stack](#️-tech-stack)
  - [🗂️ Project Structure](#️-project-structure)
  - [🛠️ Getting Started](#️-getting-started)
  - [🔐 Authentication](#-authentication)
  - [📬 Example API Routes](#-example-api-routes)
  - [🧪 Testing](#-testing)
  - [🐳 Docker Support](#-docker-support)
  - [🧠 Roadmap](#-roadmap)
  - [📄 License](#-license)
  - [💬 Support](#-support)

---

## 🚀 Core Features

- ✅ JWT-based user & admin authentication
- ✅ Customer bank account creation (Savings / Current)
- ✅ Internal fund transfers & transaction history
- ✅ Full loan lifecycle (Apply, Approve, Track, Repay)
- ✅ **Bill payments** (electricity, data, TV, etc.)
- ✅ **Debit card management** (block, activate, limits)
- ✅ **Profile management** (update email, address, phone)
- ✅ **Notifications & alerts** (transactions, login, loans)
- ✅ **Audit logging** for sensitive actions
- ✅ **Admin control panel** (users, accounts, loans, logs)
- ✅ Role-based access (Customer, Admin)
- ✅ Modular FastAPI architecture with PostgreSQL
- ✅ Docker-ready setup

---

## ⚙️ Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Framework   | FastAPI            |
| Language    | Python 3.10+       |
| Database    | PostgreSQL         |
| ORM         | SQLAlchemy         |
| Auth        | OAuth2 / JWT       |
| Security    | Bcrypt, RBAC       |
| Hosting     | Uvicorn / Docker   |

---

## 🗂️ Project Structure

```text
oriem_capital_backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│
│   ├── models/
│   │   ├── user_model.py
│   │   ├── account_model.py
│   │   ├── transaction_model.py
│   │   ├── loan_model.py
│   │   ├── card_model.py
│   │   ├── bill_model.py
│   │   └── audit_model.py
│
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── account_schema.py
│   │   ├── transaction_schema.py
│   │   ├── loan_schema.py
│   │   ├── bill_schema.py
│   │   ├── card_schema.py
│   │   └── profile_schema.py
│
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── account_service.py
│   │   ├── transaction_service.py
│   │   ├── loan_service.py
│   │   ├── card_service.py
│   │   ├── bill_service.py
│   │   └── profile_service.py
│
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── account_router.py
│   │   ├── transaction_router.py
│   │   ├── loan_router.py
│   │   ├── card_router.py
│   │   ├── bill_router.py
│   │   ├── profile_router.py
│   │   └── admin_router.py
│
│   ├── core/
│   │   ├── jwt_handler.py
│   │   └── security.py
│
│   ├── dependencies/
│   │   └── auth_dependencies.py
│
├── .env.example
├── requirements.txt
├── Dockerfile
├── README.md
```

---

## 🛠️ Getting Started

Follow the same setup steps as before:
git clone https://github.com/your-org/oriem_capital_backend.git
cd oriem_capital_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

---

## 🔐 Authentication

Uses JWT Bearer tokens and RBAC. Users must include tokens in the header:

Authorization: Bearer <access_token>

---

## 📬 Example API Routes

| Endpoint                              | Method | Description                                |
|---------------------------------------|--------|--------------------------------------------|
| `/api/auth/register`                 | POST   | Register a new user                        |
| `/api/auth/login`                    | POST   | Login and receive access token             |
| `/api/accounts/`                     | GET    | Get customer bank accounts                 |
| `/api/accounts/create`               | POST   | Open a new account                         |
| `/api/transactions/transfer`         | POST   | Transfer money to another account          |
| `/api/transactions/history`          | GET    | View transaction history                   |
| `/api/loans/apply`                   | POST   | Submit a loan request                      |
| `/api/loans/status`                  | GET    | View loan application status               |
| `/api/bills/pay`                     | POST   | Pay a bill (TV, electricity, airtime, etc) |
| `/api/bills/history`                 | GET    | View past bill payments                    |
| `/api/cards/request`                 | POST   | Request new debit card                     |
| `/api/cards/block`                   | POST   | Block a lost/stolen card                   |
| `/api/profile/update`                | PUT    | Update user profile                        |
| `/api/notifications`                 | GET    | View user alerts and notifications         |
| `/api/admin/users`                   | GET    | Admin: View all users                      |
| `/api/admin/loans`                   | GET    | Admin: Manage loan applications            |
| `/api/audit/`                        | GET    | Admin: View audit trail                    |

---

## 🧪 Testing

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Postman: Import `/openapi.json`
- Curl example:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Doe", "email": "john@example.com", "password": "Test@1234"}'
```

---

## 🐳 Docker Support

```bash
docker build -t oriem-capital-backend .
docker run -p 8000:8000 --env-file .env oriem-capital-backend
```

---

## 🧠 Roadmap

- [ ] Multi-currency wallets  
- [ ] Recurring bill payments  
- [ ] Mobile money / QR payments  
- [ ] Budgeting & financial insights  
- [ ] PDF statement generation  
- [ ] Customer support mailbox  
- [ ] React frontend integration  
- [ ] PWA & mobile app version  

---

## 📄 License

Licensed under the [MIT License](./LICENSE)

---

## 💬 Support

- 🐛 Open [GitHub Issues](https://github.com/your-org/oriem_capital_backend/issues)
- 📧 Email: `support@oriemcapital.com`
- ❤️ Pull requests welcome!
