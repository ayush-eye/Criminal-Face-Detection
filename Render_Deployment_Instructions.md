# Render Deployment Instructions

To deploy the **Criminal Face Detection API** to Render, follow these exact steps:

1. Create a new **Web Service** on [Render.com](https://render.com).
2. Connect your GitHub repository that contains this `Criminal Detection` folder.
3. Configure the service:
   - **Environment**: Python 3 (I've added `.python-version` to pin 3.11.9)
   - **Root Directory**: `Criminal Detection` (if it's in a subdirectory of your repo)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set the **Environment Variables** (Optional):
   - By default no variables are needed. The API works out of the box!
5. Click **Create Web Service**.

### Auto-generation of Data
The API has been updated to automatically intercept if `dummy_data.json` is missing and triggers the `generate_dummy_data.py` script. It will transparently create the 50 fake criminal entries and download the avatars securely during the very first startup on Render.

### Connecting to Frontend

Once deployed on Render, update your React `.env` (or change the fallback in `CriminalDetection.jsx`) to point to your new Render URL:
`VITE_CRIMINAL_API_URL=https://your-app-name.onrender.com`
