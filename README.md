# Reverse-image-search-using-RESNET50
A reverse image search system using ResNet50 to extract image embeddings and PostgreSQL (pgvector) for vector similarity search. FastAPI handles image upload, embedding generation, storage, and retrieval of visually similar images.

Link to caltech101 dataset: https://www.kaggle.com/datasets/imbikramsaha/caltech-101

Tech Stack:

Backend: FastAPI (Python)

Vector DB: PostgreSQL + pgvector (via Docker)

Model: ResNet50 (2048-D image embeddings)

UI: Streamlit

Dataset: Caltech-101

Directory structur:

project-root/
├── backend/
│   ├── api.py
│
├── data/
│   ├── raw/256_categories
│   └── uploads/
│
├── docker/
│   ├── Dockerfile
│   └── init.sql
│
├── src/
│   ├── db_manager.py
│   ├── eval_retrieval.py
│   ├── eval_unseen_split.py
│   ├── feature_extractor.py
│   ├── frontend.py
│   └── main.py
│
├── docker-compose.yml
├── requirements.txt
└── temp_query.jpg


How to run locally:

Step 0 -- Clone the repo

Step 1 -- Install Python + Create Virtual Environment, install packages

Step 2 -- Download Dataset (Caltech101)

Place it inside:

/data/raw/caltech101/

Step 3 -- Start PostgreSQL + pgvector via Docker
on terminal:
```bash
docker compose up -d
```
This connects to the PostgreSQL server with the pgvector extension
Verify:

```bash
docker ps
```

Step 4 -- Index Dataset Into PostgreSQL

(Feature extraction + vector insertion)

The indexing script is: src/eval_unseen_split.py

run on terminal
```bash
python src/eval_unseen_split.py
```

this indexes 80% of the images to the psql db and randomly selects 500 images from the remaining 20% of the images 
for evaluation

Step 5 -- Run FastAPI Backend (Local)

```bash
uvicorn backend.api:app --reload --port 8000
```
The webpage on your browser: http://localhost:8000/docs

Step 6 -- Run Streamlit frontend

```bash
streamlit run src/frontend.py
```

This will run the webpage locally and you can input an image and get similar images as output
