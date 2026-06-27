# Deployment Guide

Deploy CodeMind to production using Vercel (frontend) and Railway (backend).

## Prerequisites

- Git repository (push your code to GitHub first)
- Vercel account
- Railway account
- Supabase project (see [SUPABASE_SETUP.md](./SUPABASE_SETUP.md))
- API keys (Anthropic + OpenAI)

## Part 1: Deploy Backend to Railway

Railway is perfect for FastAPI apps - automatic deployments, built-in Redis, and generous free tier.

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `codemind` repository
6. Select the `backend` directory as root

### Step 2: Configure Build Settings

Railway should auto-detect Python, but verify:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `/backend`

### Step 3: Add Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

### Step 4: Add Redis (Optional but Recommended)

1. In your Railway project, click "New"
2. Select "Database" → "Redis"
3. Railway will auto-add `REDIS_URL` to your environment
4. Backend will automatically use it

### Step 5: Deploy

1. Click "Deploy"
2. Wait 2-3 minutes for build
3. Copy your Railway domain (e.g., `codemind-production.up.railway.app`)
4. Test: `https://your-domain.railway.app/health`

## Part 2: Deploy Frontend to Vercel

Vercel is optimized for React/Vite apps with automatic deployments.

### Step 1: Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Add New Project"
4. Import your `codemind` repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 2: Add Environment Variables

In Vercel project settings → **Environment Variables**:

```bash
VITE_API_URL=https://your-railway-backend.railway.app/api/v1
```

### Step 3: Deploy

1. Click "Deploy"
2. Wait 1-2 minutes
3. Your app will be live at: `https://codemind.vercel.app` (or custom domain)

## Part 3: Connect Frontend to Backend

### Update CORS Settings

In `backend/app/core/config.py`, add your Vercel domain:

```python
class Settings(BaseSettings):
    # ...
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://codemind.vercel.app",  # Add your Vercel domain
        "https://*.vercel.app",  # Allow preview deployments
    ]
```

Commit and push - Railway will auto-redeploy.

## Part 4: Set Up Custom Domain (Optional)

### For Frontend (Vercel)

1. In Vercel project → **Settings** → **Domains**
2. Add your domain (e.g., `codemind.com`)
3. Update DNS records as instructed
4. SSL is automatic

### For Backend (Railway)

1. In Railway project → **Settings** → **Domains**
2. Add custom domain (e.g., `api.codemind.com`)
3. Update DNS with CNAME record
4. SSL is automatic

## Part 5: CI/CD (Automatic Deployments)

Both platforms auto-deploy on push to `main`:

### Railway
- Push to `main` → Backend redeploys automatically
- View logs in Railway dashboard

### Vercel
- Push to `main` → Frontend redeploys automatically
- Pull requests get preview deployments
- View logs in Vercel dashboard

## Monitoring & Debugging

### Backend Logs (Railway)

```bash
# View live logs
railway logs

# Or in dashboard: Project → Deployments → View Logs
```

### Frontend Logs (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# View logs
vercel logs
```

### Health Checks

Add these endpoints to monitor:

- **Backend**: `https://api.codemind.com/health`
- **Frontend**: `https://codemind.com` (should load)

## Cost Breakdown

### Free Tier Limits

**Railway:**
- $5/month free credit
- ~500 hours/month execution
- Perfect for MVP

**Vercel:**
- 100GB bandwidth/month free
- Unlimited sites
- Great for frontend

**Supabase:**
- 500MB database free
- 50MB file storage
- 2GB bandwidth/month

**Total MVP cost: $0/month** ✅

### When You Scale

If you exceed free tiers:

- **Railway**: ~$5-10/month (backend + Redis)
- **Vercel**: Free (unless >100GB bandwidth)
- **Supabase**: ~$25/month (Pro tier for more resources)
- **APIs**: OpenAI ~$0.02/10k queries, Claude ~$3/1M tokens

**Estimated at 1,000 users/month: ~$10-15/month**

## Environment-Specific Settings

### Development
```bash
ENV=development
DEBUG=true
```

### Production
```bash
ENV=production
DEBUG=false
LOG_LEVEL=WARNING
```

## Rollback Deployments

### Railway
1. Go to **Deployments**
2. Find previous working deployment
3. Click "Redeploy"

### Vercel
1. Go to **Deployments**
2. Find previous deployment
3. Click "Promote to Production"

## Troubleshooting

### "CORS error" in browser
- Check `allowed_origins` includes your Vercel domain
- Verify `VITE_API_URL` points to Railway backend
- Check Railway logs for actual error

### "503 Service Unavailable"
- Railway might be deploying - wait 30s
- Check Railway logs for crashes
- Verify environment variables are set

### "Database connection failed"
- Check `SUPABASE_URL` and `SUPABASE_KEY`
- Test Supabase connection directly
- Verify pgvector extension is enabled

### Build fails on Railway
- Check `requirements.txt` for typos
- Verify Python version (Railway uses 3.11 by default)
- Check Railway build logs for specific error

### Build fails on Vercel
- Verify `package.json` has correct scripts
- Check for TypeScript errors in build logs
- Ensure all dependencies are in `package.json`

## Security Checklist

Before going live:

- [ ] All API keys in environment variables (not in code)
- [ ] `.env` files in `.gitignore`
- [ ] CORS restricted to your domains only
- [ ] HTTPS enabled (automatic on Railway/Vercel)
- [ ] Rate limiting configured
- [ ] Supabase RLS (Row Level Security) enabled if needed
- [ ] No service keys exposed to frontend

## Next Steps After Deployment

1. ✅ Backend deployed on Railway
2. ✅ Frontend deployed on Vercel
3. ✅ APIs connected and working
4. ⏭️ Monitor logs and errors
5. ⏭️ Set up analytics (optional)
6. ⏭️ Add more code examples to database
7. ⏭️ Share on Twitter/LinkedIn!

## Resources

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)
