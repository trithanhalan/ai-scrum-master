# 🤖 AI Scrum Master

**AI Scrum Master** is a full-stack automation solution designed to replace or assist the traditional Scrum Master role by leveraging the power of AI. The system automates Agile workflows, facilitates standups, updates tasks, identifies blockers, and integrates seamlessly with developer tools—all through an intuitive interface and powerful backend.

> Built with FastAPI, React, and OpenAI integration, this project showcases how generative AI can drive efficient project management in Agile teams.

---

## 📌 Table of Contents

* [Features](#features)
* [Architecture Overview](#architecture-overview)
* [Project Structure](#project-structure)
* [Technologies Used](#technologies-used)
* [Getting Started](#getting-started)
* [Environment Variables](#environment-variables)
* [Running Tests](#running-tests)
* [Deployment Guide](#deployment-guide)
* [Contributing](#contributing)
* [License](#license)

---

## ✨ Features

* ✅ **AI Standup Automation** – Uses LLMs to facilitate and summarize daily standups.
* 📋 **Task Tracking & Updates** – Connects to ticket systems (e.g., JIRA APIs planned) to track statuses and identify blockers.
* 🧠 **OpenAI-Powered Analysis** – Generates smart recommendations and daily summaries.
* ⚙️ **FastAPI Backend** – Async-ready backend with REST API.
* 🌐 **React Frontend** – Intuitive dashboard for managing Agile workflows.
* 🔐 **.env Configuration** – Secure handling of secrets via `.env` files.

---

## 🏗️ Architecture Overview

```
                ┌──────────────────────────────────────────────┐
                │     React Frontend │◄──────────────────────────────────────────────┐
                └──────────────────────────────────────────────┘
                         │
                         ▼
                 API Calls (REST)
                         ▼
                ┌───────────────────────────────────────┐   Interacts with   ┌─────────────────────────┐
                │    FastAPI Backend  │◄──────────────────────────────────────────┐ OpenAI GPT API │
                └───────────────────────────────────────┘                    └─────────────────────────┘
                         │
                         ▼
                Business Logic, Scrum Flow
                         │
                         ▼
                Database / Task System

   (Future) Integration with GitHub, Jira, Slack, Zoom APIs
```

---

## 📁 Project Structure

```
ai-scrum-master/
|
├── backend/                        # FastAPI backend
│   ├── main.py                     # Entry point
│   ├── routers/                    # Route handlers
│   ├── services/                   # Core logic
│   ├── models/                     # Data schemas
│   ├── .env                        # Secrets (not tracked)
│   └── .env.example                # Template for .env
│
├── frontend/                       # React UI
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Pages like Dashboard
│   │   └── services/               # Axios/Fetch services
│   ├── public/
│   └── yarn.lock
│
├── tests/                          # Pytest files
├── backend_test.py                 # Backend endpoint tests
├── openai_integration_test.py      # OpenAI logic test
├── test_result.md                  # Test output
├── README.md                       # Project docs
└── .gitignore                      # Git ignore file
```

---

## 🛠️ Technologies Used

| Layer          | Stack                                       |
| -------------- | ------------------------------------------- |
| Frontend       | React.js, Axios, Bootstrap                  |
| Backend        | Python, FastAPI, Pydantic, Uvicorn          |
| AI Integration | OpenAI GPT-4 API                            |
| Testing        | PyTest, Requests                            |
| DevOps         | GitHub Actions (planned), Docker (optional) |
| Package Mgmt   | pip, yarn                                   |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Node.js & Yarn
* OpenAI API Key

### Clone the Repository

```bash
git clone https://github.com/trithanhalan/ai-scrum-master.git
cd ai-scrum-master
```

---

## ⚙️ Environment Variables

Create a `.env` file in the `backend/` directory.

### Sample `.env.example`:

```env
# backend/.env.example
OPENAI_API_KEY=your_openai_api_key_here
PORT=8000
HOST=127.0.0.1
```

---

## 💻 Running the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
yarn install
yarn start
```

---

## ✅ Running Tests

```bash
# Test backend routes
python backend_test.py

# Test OpenAI Integration
python openai_integration_test.py
```

Test output will appear in `test_result.md`.

---

## ☁️ Deployment Guide (Optional)

### Docker (Basic Backend Setup)

```Dockerfile
FROM python:3.9
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment (e.g. Netlify, Vercel)

```bash
cd frontend
yarn build
# Upload build/ folder to hosting service
```

---

## 🤝 Contributing

### Steps

1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Create a Pull Request

### Guidelines

* Use clear and meaningful commit messages.
* Keep pull requests focused.
* Comment complex logic.
* Follow coding conventions used in the repo.

---

## 📜 License

**MIT License © 2025 Tri Thanh Alan**

This project is open source and free to use or modify. Help improve the productivity of Agile teams with AI!

---
