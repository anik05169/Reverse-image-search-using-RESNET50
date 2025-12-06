import sys
import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5433"   

from db_manager import DBManager
from feature_extractor import FeatureExtractor



class ResultItem(BaseModel):
    filename: str
    category: str
    distance: float

class SearchResponse(BaseModel):
    results: List[ResultItem]



app = FastAPI(title="Reverse Image Search API")

extractor = FeatureExtractor()
db = DBManager()


search_example = {
    "results": [
        {
            "filename": "img_001.jpg",
            "category": "airplanes",
            "distance": 0.0234
        },
        {
            "filename": "img_050.jpg",
            "category": "motorbikes",
            "distance": 0.0456
        }
    ]
}



@app.post(
    "/search",
    response_model=SearchResponse,
    responses={
        200: {
            "description": "Closest image matches",
            "content": {
                "application/json": {
                    "example": search_example
                }
            }
        },
        422: {
            "description": "Validation Error (file missing or invalid)",
        }
    },
)
async def search_image(file: UploadFile = File(...)):
    
    temp_path = "temp_query.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    vector = extractor.extract(temp_path)

    results = db.search_similar(vector, limit=6)

    formatted = [
        {
            "filename": r[0],
            "category": r[1],
            "distance": float(r[2])
        }
        for r in results
    ]

    return {"results": formatted}

@app.get("/")
def home():
    return {"status": "OK", "message": "Reverse Image Search API running"}