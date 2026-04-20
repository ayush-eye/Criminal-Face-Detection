import json
import os
import random
import urllib.request

NUM_RECORDS = 50

# Pune areas
pune_areas = [
    "Kothrud, Pune", "Shivajinagar, Pune", "Hinjewadi, Pune", "Hadapsar, Pune",
    "Viman Nagar, Pune", "Kalyani Nagar, Pune", "Wagholi, Pune", "Baner, Pune",
    "Aundh, Pune", "Pimpri, Pune", "Chinchwad, Pune", "Katraj, Pune",
    "Swargate, Pune", "Camp, Pune", "Vishrantwadi, Pune", "Kharadi, Pune"
]

# Marathi/Indian names
first_names = [
    "Rahul", "Suresh", "Ramesh", "Prakash", "Amit", "Santosh", "Arun", "Sunil", "Vijay",
    "Rajesh", "Sachin", "Deepak", "Anil", "Sanjay", "Mahesh", "Nitin", "Vishal", "Vikram",
    "Pravin", "Yogesh", "Sandeep", "Kiran", "Ganesh", "Sagar", "Rakesh", "Dinesh", "Manoj"
]

last_names = [
    "Patil", "Deshmukh", "Jadhav", "Shinde", "Pawar", "Kadam", "Kale", "Gaikwad", "Bhosale",
    "Joshi", "Kulkarni", "Deshpande", "Chavan", "More", "Mane", "Wagh", "Kshirsagar", "Kharat"
]

crimes = [
    "Harassment", "Stalking", "Assault", "Theft", "Cyberbullying",
    "Domestic Violence", "Molestation", "Extortion", "Kidnapping"
]

def generate_data():
    if not os.path.exists("static/images"):
        os.makedirs("static/images")

    criminals = []

    print("Generating dummy data and downloading images...")
    
    for i in range(1, NUM_RECORDS + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        area = random.choice(pune_areas)
        age = random.randint(22, 60)
        crime = random.choice(crimes)
        
        # We will use pravatar for dummy faces (using unique IDs for different faces)
        image_url = f"https://i.pravatar.cc/300?u=criminal_{i}"
        
        image_filename = f"criminal_{i}.jpg"
        image_path = os.path.join("static", "images", image_filename)
        
        try:
            req = urllib.request.Request(
                image_url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded image {i}")
        except Exception as e:
            print(f"Failed to download image {i}: {e}")
            
        criminal = {
            "id": i,
            "name": name,
            "age": age,
            "location": area,
            "crime": crime,
            "image": f"/static/images/{image_filename}"
        }
        
        criminals.append(criminal)
        
    with open("dummy_data.json", "w") as f:
        json.dump(criminals, f, indent=4)
        
    print("Dummy data generation complete!")

if __name__ == "__main__":
    generate_data()
