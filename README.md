# QuizMaster_V2

![QuizMaster V2](https://img.shields.io/badge/Vue.js-Frontend-brightgreen?style=for-the-badge\&logo=vue.js)
![QuizMaster V2](https://img.shields.io/badge/Flask-Backend-blue?style=for-the-badge\&logo=flask)
![QuizMaster V2](https://img.shields.io/badge/SQLite-Database-lightgrey?style=for-the-badge\&logo=sqlite)

## 📖 Overview

**QuizMaster V2** is a modernized and feature-rich **quiz management system** rebuilt with a **Vue.js frontend** and a robust **Flask backend**.
It’s designed to deliver **seamless learning assessments**, **dynamic quiz creation**, and **real-time performance insights** for educators and learners.

---

## 🚀 New & Enhanced Features

### 🛠 Admin Panel

* Full **CRUD operations**:

  * Subjects, Chapters, Quizzes, Questions
* **Vue-powered dashboard** with:

  * Interactive quiz analytics
  * Real-time stats updates
* Modal & API-based entity creation (no reloads)

### 👨‍🎓 User Portal

* Modern **Vue.js UI**
* Secure **JWT-based authentication**
* Explore quizzes dynamically with **single-page navigation**
* Attempt quizzes with:

  * Timer & progress tracking
  * Instant results & feedback
* Historical performance dashboard with charts

### ⚡ Performance Upgrades

* API-driven architecture (**RESTful endpoints**)
* **Optimized DB schema** with cascades & indexes
* **Frontend state management** via Vuex/Pinia

---

## 🧰 Tech Stack

| Layer        | Technologies Used                                           |
| ------------ | ----------------------------------------------------------- |
| 🖥️ Frontend | Vue.js 3, Vue Router, Vuex/Pinia, Axios, Bootstrap/Tailwind |
| ⚙️ Backend   | Flask, Flask-RESTful, Flask-JWT-Extended                    |
| 💾 Database  | SQLite (dev), PostgreSQL/MySQL (prod-ready)                 |
| 📊 Charts    | Chart.js & ECharts                                          |
| 🛡️ Security | JWT Auth, Password Hashing, Role-Based Access               |
| 🔐 Session   | Token-based auth for SPA                                    |

---

## 🏗️ Project Structure

```plaintext
📦 QuizMaster_V2/
 ┣ 📜 backend/
 ┃ ┣ 📜 app.py              # Flask app entry
 ┃ ┣ 📜 routes/             # API endpoints
 ┃ ┣ 📜 models/             # DB models
 ┃ ┣ 📜 utils/              # Auth, helpers
 ┃ ┗ 📜 requirements.txt
 ┣ 📜 frontend/
 ┃ ┣ 📜 src/
 ┃ ┃ ┣ 📜 components/       # Vue components
 ┃ ┃ ┣ 📜 views/            # Page views
 ┃ ┃ ┣ 📜 store/            # Vuex/Pinia state
 ┃ ┃ ┗ 📜 router.js
 ┃ ┗ 📜 package.json
 ┣ 📜 README.md
 ┣ 📂 instance/             # SQLite DB (dev)
```

---

## 🧬 Database Schema Overview

* **User**

  * `id`, `username`, `password`, `role`, `scores[]`
* **Subject**

  * `id`, `name`, `description`, `chapters[]`
* **Chapter**

  * `id`, `name`, `subject_id`, `quizzes[]`
* **Quiz**

  * `id`, `title`, `duration`, `chapter_id`, `questions[]`, `scores[]`
* **Question**

  * `id`, `statement`, `options[]`, `correct_option`, `quiz_id`
* **Score**

  * `id`, `user_id`, `quiz_id`, `score`, `total_questions`, `timestamp`

---

## ⚙️ Installation Guide

### 🐍 Backend Setup

```bash
# Clone repo
git clone https://github.com/repo-sumit/QuizMaster_V2.git
cd QuizMaster_V2/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

### 🌐 Frontend Setup

```bash
cd QuizMaster_V2/frontend

# Install dependencies
npm install

# Run Vue dev server
npm run serve
```

### 🔗 Access

* Backend API → `http://127.0.0.1:5000/`
* Frontend App → `http://localhost:8080/`

---

## 🖥️ System Flow

```plaintext
Admin:
  Create Subject → Add Chapter → Add Quiz → Add Questions → Monitor Analytics
User:
  Register/Login → Browse Subjects → Attempt Quiz → View Results & Performance
```

---

## 🔐 Security

* **JWT-based auth** with refresh tokens
* **Role-based access control** (Admin/User)
* **CORS enabled** for secure frontend-backend communication

---

## 👨‍💻 Developer Notes

* Recommended: Use **SQLite** for dev and **Postgres/MySQL** in production
* Modular architecture for **scalability**
* Backend & frontend run independently for easy deployment

---

## Seed Data (JSON)

The backend automatically seeds default subjects, chapters, quizzes, and questions when the database is empty.

- Seed file: `backend/seed_data.json`
- Trigger: First run with no subjects in the database
- Reset: Delete `quizmaster.db` and restart the backend to re-seed

---

## UI Highlights

- Admin and student dashboards include subject sorting and filtering controls.
- Student dashboard includes a "Practice Mix" generator for quick test runs.
- Focus sprint timer and notes help keep study sessions organized.

## ❤️ Acknowledgements

Built with passion using **Flask + Vue.js**.
Designed for educators, learners, and future-ready assessments.
