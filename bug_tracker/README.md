# Bug Tracker

A Flask-based bug tracking application with issue management and chatbot integration.

## Setup Instructions

1. **Create and activate a virtual environment:**

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   
   Create a `.env` file in the root directory (copy from `.env.example` if available):
   ```bash
   SECRET_KEY=your-secret-key-here-change-in-production
   DATABASE_URL=sqlite:///bug_tracker.db
   OPENAI_API_KEY=your-openai-api-key-here
   ```
   
   **Note:** The `.env` file is gitignored and should never be committed to version control.
   
   Environment variables:
   - `SECRET_KEY`: Flask secret key (required for production, defaults to dev key if not set)
   - `DATABASE_URL`: Database URL (optional, defaults to SQLite if not set)
   - `OPENAI_API_KEY`: Your OpenAI API key for chatbot functionality (optional)

4. **Run the application:**
   
   Using Flask CLI (recommended):
   ```bash
   flask run
   ```
   
   Or using Python directly:
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Open your browser and navigate to `http://localhost:5000`
   - The database will be automatically seeded with sample data on first run

## Project Structure

```
bug_tracker/
 ├── app.py                 # Main Flask application
 ├── models.py             # Database models
 ├── config.py             # Configuration settings
 ├── routes/
 │    ├── issues.py        # Issue-related routes
 │    ├── chatbot.py       # Chatbot API routes
 │    └── __init__.py
 ├── static/
 │    └── styles.css       # CSS styles
 ├── templates/
 │    ├── index.html       # Home page
 │    ├── calendar.html    # Calendar view
 │    └── issue_form.html  # Issue creation form
 └── requirements.txt      # Python dependencies
```

## Features

- Create, read, update, and delete issues
- Calendar view for issues with due dates
- Chatbot integration with OpenAI
- RESTful API for issue management
- Search and filter functionality
- Sample seed data (users: Alex, Maddy, Sarah, John, Emily)

## Sample Data

The application automatically seeds the database with sample data on first run:
- **Users**: Alex (Developer), Maddy (QA Engineer), Sarah (Project Manager), John (Developer), Emily (Designer)
- **Issues**: 14 sample issues with various statuses, priorities, assignees, and due dates spread across the current week

## Testing Features

After starting the app, you can test:
- **CRUD Operations**: Create, read, update, and delete issues
- **Search**: Filter issues by title, status, and assignee
- **Status Updates**: Change issue status using the Status button
- **Chatbot**: Ask "What is Alex working on?" to see Alex's assigned issues
- **Calendar**: View the weekly calendar to see issues organized by due date

