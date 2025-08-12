# Flask API with Supabase

A simple Flask API that manages consultation finalized status using Supabase.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Supabase credentials:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
```

3. Run the application:
```bash
python app.py
```

## Deployment to Render

### Step 1: Prepare Your Repository
- Push your code to GitHub/GitLab
- Make sure all files are committed (app.py, requirements.txt, Procfile, runtime.txt)

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" and select "Web Service"
3. Connect your GitHub/GitLab repository
4. Configure the service:
   - **Name**: `your-app-name`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### Step 3: Set Environment Variables
In your Render dashboard, go to Environment and add:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_KEY`: Your Supabase service key

### Step 4: Deploy
Click "Create Web Service" and wait for deployment to complete.

## API Endpoints

- `GET /api/finalized` - Get consultation finalized status
- `POST /api/finalized` - Update consultation finalized status
- `GET /admin` - Admin interface to toggle status

## Notes
- The free tier sleeps after 15 minutes of inactivity
- First request after sleep may take 30-60 seconds
- Your app will be available at: `https://your-app-name.onrender.com`
