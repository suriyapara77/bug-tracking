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
```
http://localhost:5000
```

## 🚀 Deployment

This project can be deployed to any platform that supports Flask applications (Heroku, Railway, Render, etc.).

### Deploying to Render

Render is a cloud platform that makes it easy to deploy Flask applications. Follow these steps:

#### Prerequisites
- A GitHub account with your code pushed to a repository
- A Render account (sign up at [render.com](https://render.com))

#### Step-by-Step Deployment

1. **Create a PostgreSQL Database (Optional but Recommended)**
   - Log in to your Render dashboard
   - Click "New +" → "PostgreSQL"
   - Give it a name (e.g., `bug-tracker-db`)
   - Select a free tier plan
   - Note the `Internal Database URL` - you'll need this later

2. **Create a Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `bug-tracker` (or your preferred name)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r bug_tracker/requirements.txt`
     - **Start Command**: `cd bug_tracker && gunicorn app:app --bind 0.0.0.0:$PORT`
     - **Root Directory**: Leave empty (or set to repository root)

3. **Set Environment Variables**
   In the Render dashboard, add these environment variables:
   - `SECRET_KEY`: Generate a strong random key (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DATABASE_URL`: (If you created a PostgreSQL database) Copy the `Internal Database URL` from your database service
   - `OPENAI_API_KEY`: (Optional) Your OpenAI API key for chatbot functionality
   - `FLASK_APP`: `app.py`
   - `PYTHON_VERSION`: `3.11.0`

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Wait for the build to complete (usually 2-5 minutes)
   - Your app will be available at `https://your-app-name.onrender.com`

#### Using render.yaml (Alternative Method)

If you prefer using the `render.yaml` file (already included in this repo):

1. Push your code to GitHub
2. In Render dashboard, click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and configure the service
5. Review and apply the configuration
6. Set any additional environment variables (like `OPENAI_API_KEY`)

#### Environment Variables

For production deployment on Render, set these environment variables:

- `SECRET_KEY`: Your Flask secret key (required - Render can auto-generate this)
- `DATABASE_URL`: Automatically provided by Render if you link a PostgreSQL database
- `OPENAI_API_KEY`: (Optional) Your OpenAI API key for chatbot
- `FLASK_APP`: `app.py`
- `PYTHON_VERSION`: `3.11.0`

### Important Notes

⚠️ **Database Considerations:**
- SQLite is suitable for development only
- For production on Render, use PostgreSQL (free tier available)
- The `config.py` automatically handles PostgreSQL URL conversion
- Render provides the `DATABASE_URL` automatically when you link a database

⚠️ **Free Tier Limitations:**
- Render free tier services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading for production use

### Other Deployment Platforms

This project can also be deployed to:
- **Heroku**: Similar process, uses Procfile
- **Railway**: Supports Python apps with minimal configuration
- **AWS/GCP/Azure**: Requires more setup but offers more control
