import os
import sys
import random
from collections import defaultdict

# Allow imports from src/
sys.path.append(os.path.dirname(__file__))

from db_manager import DBManager
from feature_extractor import FeatureExtractor


# --------------------------
# CONFIG
# --------------------------

DATA_DIR = "/app/data"  # inside Docker
# DATA_DIR = "data/caltech101"  # if running locally

TRAIN_SPLIT = 0.8
NUM_TEST_IMAGES = 500           # number of unseen test queries
TOP_K = 5


# --------------------------
# LOAD ALL IMAGES
# --------------------------

all_images = []

for root, _, files in os.walk(DATA_DIR):
    for f in files:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            category = os.path.basename(root)
            filepath = os.path.join(root, f)
            all_images.append((filepath, category))

print("Total images found:", len(all_images))


# --------------------------
# SPLIT INTO TRAIN / TEST
# --------------------------

random.shuffle(all_images)

split_idx = int(len(all_images) * TRAIN_SPLIT)
train_images = all_images[:split_idx]
test_images = all_images[split_idx:]

# Only evaluate on a subset for speed
test_images = random.sample(test_images, NUM_TEST_IMAGES)

print(f"Training set size: {len(train_images)}")
print(f"Test set size: {len(test_images)} (random unseen)")


# --------------------------
# INITIALIZE MODEL + DB
# --------------------------

extractor = FeatureExtractor()
db = DBManager()


# --------------------------
# CLEAR OLD DB ENTRIES
# --------------------------

print("\nClearing old DB entries...")
cursor = db.conn.cursor()
cursor.execute("DELETE FROM inventory;")
cursor.close()


# --------------------------
# INDEX TRAINING IMAGES
# --------------------------

print("\nIndexing training images...")

batch = []
BATCH_SIZE = 100
count = 0

for filepath, category in train_images:
    vec = extractor.extract(filepath)

    if vec:
        filename = os.path.basename(filepath)
        batch.append((filename, category, vec))
        count += 1

    if len(batch) >= BATCH_SIZE:
        db.insert_batch(batch)
        batch = []
        print(f"Indexed {count} images...")

if batch:
    db.insert_batch(batch)

print(f"Indexing finished. Total indexed: {count}")


# --------------------------
# EVALUATE ON UNSEEN IMAGES
# --------------------------

print("\nEvaluating on unseen test images...")

correct_top1 = 0
correct_top5 = 0
total = 0

for filepath, true_cat in test_images:
    vec = extractor.extract(filepath)
    results = db.search_similar(vec, limit=TOP_K)

    predicted_top1 = results[0][1]
    predicted_top5 = [r[1] for r in results]

    total += 1
    if predicted_top1 == true_cat:
        correct_top1 += 1

    if true_cat in predicted_top5:
        correct_top5 += 1

    if total % 50 == 0:
        print(f"Evaluated {total}/{NUM_TEST_IMAGES}...")


# --------------------------
# PRINT ACCURACY
# --------------------------

print("\n--- FINAL RESULTS ---")
print("Total test images:", total)
print("Top-1 Accuracy:", correct_top1 / total)
print("Top-5 Accuracy:", correct_top5 / total)
