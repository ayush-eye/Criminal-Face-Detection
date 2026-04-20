from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import random

import os
import hashlib

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
    Deterministic dummy endpoint for face detection.
    In a real scenario, this would use a ML model to extract face embeddings.
    Here we use the file hash to ensure the same image always yields the same result.
    """
    criminals = load_data()
    if not criminals:
        return {"status": "error", "message": "No data available"}
        
    # Read file content to generate a deterministic seed
    content = await file.read()
    file_hash = int(hashlib.md5(content).hexdigest(), 16)
    
    # Create a local random instance for determinism
    local_random = random.Random(file_hash)
    
    # Simulate processing time
    # 80% chance of finding a match (deterministic per image)
    match_found = local_random.random() < 0.8
    
    if match_found:
        matched_criminal = local_random.choice(criminals)
        return {
            "status": "success",
            "match": True,
            "confidence": round(local_random.uniform(75.5, 99.9), 2),
            "data": matched_criminal
        }
    else:
        return {
            "status": "success",
            "match": False,
            "message": "No match found in the database."
        }
