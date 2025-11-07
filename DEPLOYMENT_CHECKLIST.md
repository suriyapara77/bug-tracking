# 🚀 Deployment Readiness Checklist

This document verifies that the RL-TEST project is ready for deployment to Vercel.

## ✅ Pre-Deployment Checklist

### 1. Project Structure
- [x] `vercel.json` exists at root level
- [x] `bug_tracker/api/index.py` exists and is configured
- [x] `bug_tracker/requirements.txt` contains all dependencies
- [x] `.gitignore` exists at root level
- [x] `.vercelignore` exists (optional but recommended)

### 2. Configuration Files

#### vercel.json
- [x] Correctly points to `bug_tracker/api/index.py`
- [x] Uses `@vercel/python` builder
- [x] Routes configured to handle all requests

#### API Handler (bug_tracker/api/index.py)
- [x] Properly imports the Flask app
- [x] Sets VERCEL environment variable
- [x] Exports handler for Vercel

#### Config (bug_tracker/config.py)
- [x] Handles Vercel environment
- [x] Uses `/tmp` for SQLite on Vercel
- [x] Falls back to local database for development

### 3. Dependencies

#### requirements.txt
- [x] Flask==3.0.0
- [x] Flask-SQLAlchemy==3.1.1
- [x] Flask-CORS==4.0.0
- [x] openai>=1.12.0

### 4. Environment Variables

Before deploying, ensure these are set in Vercel Dashboard:

#### Required:
- `SECRET_KEY` - Flask secret key (generate a strong random key)
- `VERCEL` - Set to `1` (usually set automatically by Vercel)

#### Optional:
- `DATABASE_URL` - For production, use PostgreSQL or another cloud database
  - **Important**: SQLite on Vercel is ephemeral (data lost on cold starts)
  - Recommended: Use Vercel Postgres, Supabase, Neon, or MongoDB Atlas
- `OPENAI_API_KEY` - For chatbot functionality

### 5. Database Considerations

⚠️ **Critical**: SQLite on Vercel has limitations:
- Data stored in `/tmp` is **ephemeral**
- Database resets on each cold start
- **Not suitable for production** with persistent data

**Recommended Solutions:**
1. Use a cloud database (PostgreSQL, MongoDB, etc.)
2. Update `DATABASE_URL` environment variable
3. Update `config.py` if using a different database adapter

### 6. Static Files & Templates

- [x] Static files in `bug_tracker/static/`
- [x] Templates in `bug_tracker/templates/`
- [x] Flask app configured with correct paths
- [x] Vercel will serve these through Flask

### 7. Routes & Blueprints

- [x] Main routes in `bug_tracker/routes/issues.py`
- [x] Chatbot routes in `bug_tracker/routes/chatbot.py`
- [x] Blueprints properly registered in `app.py`

## 📋 Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables
Go to Vercel Dashboard → Your Project → Settings → Environment Variables:
- Add `SECRET_KEY` (generate a strong random key)
- Add `OPENAI_API_KEY` (if using chatbot)
- Add `DATABASE_URL` (if using cloud database)
- Verify `VERCEL` is set to `1` (usually automatic)

### 4. Deploy
```bash
# From project root
vercel
```

For production:
```bash
vercel --prod
```

### 5. Verify Deployment
- [ ] Application loads at deployed URL
- [ ] Static files (CSS) load correctly
- [ ] Templates render properly
- [ ] API endpoints respond correctly
- [ ] Database operations work (if configured)

## 🔍 Post-Deployment Verification

### Test These Endpoints:
1. **Homepage**: `https://your-app.vercel.app/`
2. **Calendar**: `https://your-app.vercel.app/calendar`
3. **Chatbot**: `https://your-app.vercel.app/chat`
4. **API - Issues**: `https://your-app.vercel.app/issues`
5. **API - Users**: `https://your-app.vercel.app/users`

### Common Issues & Solutions

#### Issue: Import errors
- **Solution**: Ensure all dependencies are in `requirements.txt`
- **Solution**: Check that `bug_tracker/api/index.py` correctly adds parent directory to path

#### Issue: Static files not loading
- **Solution**: Verify Flask app has correct `static_folder` configuration
- **Solution**: Check that static files are in `bug_tracker/static/`

#### Issue: Database not persisting
- **Solution**: Switch to cloud database (PostgreSQL, MongoDB, etc.)
- **Solution**: Update `DATABASE_URL` environment variable

#### Issue: Environment variables not working
- **Solution**: Set variables in Vercel Dashboard
- **Solution**: Redeploy after adding new environment variables

## 📝 Notes

- The project structure is ready for Vercel deployment
- All necessary configuration files are in place
- Remember to use a cloud database for production
- Test thoroughly after deployment

## 🎯 Next Steps

1. Set environment variables in Vercel Dashboard
2. Deploy using `vercel --prod`
3. Test all functionality
4. Monitor logs for any issues
5. Consider setting up a production database if not already done

