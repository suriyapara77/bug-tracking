# 🐛 Bug Tracker

A modern, Flask-based bug tracking application with AI-powered chatbot integration. Manage issues, track team assignments, and visualize your workflow with an intuitive calendar view.

## ✨ Features

- **Issue Management**: Create, read, update, and delete issues with detailed descriptions
- **Priority & Status Tracking**: Organize issues by priority (High, Medium, Low) and status (Open, In-Progress, Closed)
- **Team Assignment**: Assign issues to team members with role-based organization
- **Calendar View**: Visualize issues on a weekly calendar organized by due dates
- **AI Chatbot Assistant**: Get instant help with natural language queries powered by OpenAI
- **Search & Filter**: Quickly find issues by title, status, assignee, or priority
- **RESTful API**: Full API support for programmatic access
- **Sample Data**: Pre-seeded with sample users and issues for quick testing

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite (with SQLAlchemy ORM)
- **AI Integration**: OpenAI API (GPT-3.5-turbo)
- **Frontend**: HTML, CSS, JavaScript
- **CORS**: Flask-CORS for API access

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (optional, for chatbot functionality)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r bug_tracker/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `bug_tracker/` directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///bug_tracker.db
OPENAI_API_KEY=your-openai-api-key-here
```

**Environment Variables:**
- `SECRET_KEY`: Flask secret key (required for production, defaults to dev key if not set)
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- `OPENAI_API_KEY`: OpenAI API key for chatbot functionality (optional)

> **Note:** The `.env` file is gitignored and should never be committed to version control.

### 5. Run the application

**Using Flask CLI (recommended):**
```bash
cd bug_tracker
flask run
```

**Or using Python directly:**
```bash
cd bug_tracker
python app.py
```

### 6. Access the application

Open your browser and navigate to:
