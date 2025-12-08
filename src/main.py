import os
import time
from db_manager import DBManager
from feature_extractor import FeatureExtractor

# Configuration
DATA_DIR = "/app/data" # Matches the volume path in docker-compose

def main():
    print("--- Starting Visual Search Engine ---")
    
    
    print("Loading AI Model... (this may take a moment)")
    extractor = FeatureExtractor()
    
    print("Connecting to Database...")
    db = DBManager()

    
    print(f"Scanning directory: {DATA_DIR}")
    
    
    batch_data = []
    BATCH_SIZE = 100 
    count = 0

    # Walk through all subfolders (Categories)
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Get Category from folder name (e.g., /data/airplanes/img1.jpg -> airplanes)
                category = os.path.basename(root)
                filepath = os.path.join(root, filename)

                # Extract Vector
                vector = extractor.extract(filepath)
                
                if vector:
                    # Add to batch
                    batch_data.append((filename, category, vector))
                    count += 1

                # If batch is full, insert into DB
                if len(batch_data) >= BATCH_SIZE:
                    db.insert_batch(batch_data)
                    batch_data = [] # Clear batch
                    print(f"Indexed {count} images...")

    # Insert remaining images
    if batch_data:
        db.insert_batch(batch_data)
    
    print(f"--- Indexing Complete! Total Images: {count} ---")

    
    print("\n--- Running Test Search ---")
    test_results = db.search_similar(vector) 
    for res in test_results:
        print(f"Match: {res[0]} | Category: {res[1]} | Distance: {res[2]:.4f}")

    db.close()

if __name__ == "__main__":
    main()