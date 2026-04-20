from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import random

import os

app = FastAPI(title="Criminal Face Detection API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure data exists on startup (useful for Render deployment)
if not os.path.exists("dummy_data.json"):
    try:
        from generate_dummy_data import generate_data
        generate_data()
    except Exception as e:
        print("Could not generate dummy data:", e)

# Ensure static folder exists before mounting
if not os.path.exists("static"):
    os.makedirs("static")

# Mount static folder to serve images
app.mount("/static", StaticFiles(directory="static"), name="static")

def load_data():
    try:
        with open("dummy_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

criminals_data = load_data()

@app.get("/api/criminals")
def get_all_criminals():
    return {"status": "success", "data": criminals_data}

@app.post("/api/criminals/detect")
async def detect_criminal(file: UploadFile = File(...)):
    """
    Dummy endpoint for face detection.
    In a real scenario, this would use a ML model to extract face embeddings
    and match them against a database. Here we just return a random match from our dummy data 
    or a "no match found" response.
    """
    criminals = load_data()
    if not criminals:
        return {"status": "error", "message": "No data available"}
        
    # Simulate processing time
    # Simulate an 80% chance of finding a match
    match_found = random.random() < 0.8
    
    if match_found:
        matched_criminal = random.choice(criminals)
        return {
            "status": "success",
            "match": True,
            "confidence": round(random.uniform(75.5, 99.9), 2),
            "data": matched_criminal
        }
    else:
        return {
            "status": "success",
            "match": False,
            "message": "No match found in the database."
        }
