# 🎓 Smart Student Management System

A full-stack web application built with **Python Flask** for managing student records with analytics, search, and an AI-style chatbot assistant.

> Built as a university project — deployed live on Vercel.

---

## 🌐 Live Demo

🔗 **[View Live App]()** ← *(replace with your Vercel URL)*


## ✨ Features

- ➕ **Add Student** — with full input validation (unique ID, name, age, grade A–F, marks 0–100)
- 👥 **View All Students** — clean table with color-coded marks progress bars
- 🔍 **Search** — search by student ID or partial name (case-insensitive)
- ✏️ **Update** — edit any student field with pre-filled form
- 🗑️ **Delete** — with confirmation dialog to prevent accidents
- 📊 **Analytics Dashboard** — average marks, top performer, pass rate, grade distribution charts
- 🤖 **Chatbot Assistant** — keyword-based bot that guides users on how to use the app
- 💾 **File Storage** — all data stored in `students.txt` using Python file I/O

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **Flask** | Web framework — handles routes and requests |
| **Jinja2** | Template engine — renders dynamic HTML |
| **HTML / CSS** | Frontend structure and styling |
| **JavaScript** | Chatbot, toast notifications, async form submissions |
| **Chart.js** | Analytics charts (doughnut + bar chart) |
| **Google Fonts** | Plus Jakarta Sans — premium typography |
| **File I/O (TXT)** | Persistent student data storage |
| **Git & GitHub** | Version control and source hosting |
| **Vercel** | Cloud deployment and live hosting |

---

## 📁 Project Structure

```
smart-sms/
│
├── app.py                  # Main Flask app — all routes and logic
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── .gitignore              # Files excluded from Git
│
└── templates/
    ├── base.html           # Master layout (sidebar, navbar, chatbot)
    ├── index.html          # Dashboard with stats
    ├── add.html            # Add student form
    ├── students.html       # All students table
    ├── search.html         # Search page
    ├── update.html         # Edit student form
    └── analytics.html      # Charts and analytics
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-sms.git
cd smart-sms
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

---

## ☁️ Deployment (Vercel)

This app is configured for one-click Vercel deployment.

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → **Add New Project**
3. Import this GitHub repository
4. Click **Deploy** — no extra settings needed

> ⚠️ Note: Vercel uses a serverless environment. Data saved to `students.txt` is stored in `/tmp/` and resets between cold starts. This is fine for demo/portfolio purposes.

---

## 📊 Analytics Features

The analytics page shows:

- 📈 **Average Marks** across all students
- 🏆 **Top Performer** — student with highest marks
- ⚠️ **Below Average Count** — students scoring below average
- ⬆️⬇️ **Highest & Lowest** marks
- ✅ **Pass Rate** — percentage of students with marks ≥ 50
- 🎂 **Average Age** of all students
- 🥧 **Grade Distribution** — doughnut chart (A–F)
- 📊 **Marks per Student** — color-coded bar chart

---

## 🤖 Chatbot

The built-in chatbot assistant answers questions like:

- *"How do I add a student?"*
- *"How do I search for a student?"*
- *"What does analytics show?"*
- *"How do I delete a student?"*

It uses **keyword matching** in Python — no external AI API needed.

---

## ✅ Input Validation Rules

| Field | Rule |
|---|---|
| **ID** | Must be a positive integer and unique |
| **Name** | Cannot be empty or purely numeric |
| **Age** | Must be an integer greater than 0 |
| **Grade** | Must be a single letter: A, B, C, D, E, or F |
| **Marks** | Must be an integer between 0 and 100 |

---

## 👨‍💻 Author

**Muhammad Nofil**
- GitHub: (https://github.com/nofilmemon0811)
- LinkedIn: (https://www.linkedin.com/in/nofil-memon-/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ **If you found this project helpful, give it a star!**
