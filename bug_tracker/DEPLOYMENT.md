# Vercel Deployment Guide

## Prerequisites

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

## Deployment Steps

1. **Navigate to the bug_tracker directory:**
   ```bash
   cd bug_tracker
   ```

2. **Set Environment Variables in Vercel Dashboard:**
   - Go to your project settings on Vercel
   - Navigate to Environment Variables
   - Add the following:
     - `SECRET_KEY`: Your Flask secret key (generate a strong random key)
     - `DATABASE_URL`: (Optional) For production, use PostgreSQL or another cloud database
     - `OPENAI_API_KEY`: (Optional) Your OpenAI API key for chatbot functionality
     - `VERCEL`: Set to `1` (Vercel sets this automatically, but you can verify)

3. **Deploy:**
   ```bash
   vercel
   ```
   
   For production deployment:
   ```bash
   vercel --prod
   ```

## Important Notes

### Database Considerations

⚠️ **SQLite Limitations on Vercel:**
- Vercel's file system is read-only except for `/tmp`
- Data in `/tmp` is **ephemeral** and will be lost on each cold start
- SQLite databases will be reset every time the serverless function restarts

**Recommended Solutions:**
1. **Use a Cloud Database** (Recommended for production):
   - PostgreSQL (via Vercel Postgres, Supabase, or Neon)
   - MongoDB Atlas
   - PlanetScale (MySQL)
   - Any other cloud database service

2. **Update DATABASE_URL** in Vercel environment variables:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

### File Structure

The deployment uses:
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function handler
- `app.py` - Your Flask application
- `requirements.txt` - Python dependencies

### Static Files

Static files (CSS, JS) and templates are automatically served by Vercel.

## Troubleshooting

1. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Vercel will automatically install dependencies

2. **Database Issues:**
   - If using SQLite, data will be lost on cold starts
   - Switch to a cloud database for production

3. **Environment Variables:**
   - Make sure all required environment variables are set in Vercel dashboard
   - Redeploy after adding new environment variables

## Alternative Deployment Options

If you need persistent SQLite or better Flask support, consider:
- **Railway** - Great for Flask apps with SQLite
- **Render** - Easy Flask deployment
- **Fly.io** - Good for containerized apps
- **Heroku** - Traditional PaaS option

