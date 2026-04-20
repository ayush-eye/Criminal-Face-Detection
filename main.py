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

# Pre-calculate hashes for "accurate" simulation
known_criminals_by_hash = {}

def index_criminals():
    global known_criminals_by_hash
    print("Indexing criminal hashes for accurate detection simulation...")
    for criminal in criminals_data:
        # Construct path from the image field (remove leading slash)
        img_path = criminal["image"].lstrip("/")
        if os.path.exists(img_path):
            try:
                with open(img_path, "rb") as f:
                    content = f.read()
                    file_hash = hashlib.md5(content).hexdigest()
                    known_criminals_by_hash[file_hash] = criminal
            except Exception as e:
                print(f"Error indexing {img_path}: {e}")
    print(f"Indexed {len(known_criminals_by_hash)} criminal images.")

index_criminals()

@app.get("/api/criminals")
def get_all_criminals():
    return {"status": "success", "data": criminals_data}

@app.post("/api/criminals/detect")
async def detect_criminal(file: UploadFile = File(...)):
    """
    Simulated AI face detection.
    First checks for an exact image match (hash), then falls back to 
    deterministic random matching for unknown images.
    """
    criminals = load_data()
    if not criminals:
        return {"status": "error", "message": "No data available"}
        
    # Read file content
    content = await file.read()
    file_hash_hex = hashlib.md5(content).hexdigest()
    
    # 1. CHECK FOR EXACT MATCH (Realism)
    if file_hash_hex in known_criminals_by_hash:
        matched_criminal = known_criminals_by_hash[file_hash_hex]
        return {
            "status": "success",
            "match": True,
            "confidence": round(random.uniform(98.5, 99.9), 2), # High confidence for exact match
            "record_type": "exact_match",
            "data": matched_criminal
        }

    # 2. FALLBACK TO DETERMINISTIC SIMULATION
    file_hash_int = int(file_hash_hex, 16)
    local_random = random.Random(file_hash_int)
    
    # Simulate an 80% chance of finding a "similar" match
    match_found = local_random.random() < 0.8
    
    if match_found:
        matched_criminal = local_random.choice(criminals)
        return {
            "status": "success",
            "match": True,
            "confidence": round(local_random.uniform(75.5, 95.0), 2),
            "record_type": "similar_match",
            "data": matched_criminal
        }
    else:
        return {
            "status": "success",
            "match": False,
            "message": "No match found in the database."
        }
