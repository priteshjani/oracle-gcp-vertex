from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from .db import get_db_connection
from .ai import AIController

app = FastAPI(title="Retail Supermarket Demo API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

ai_controller = AIController()

class Item(BaseModel):
    id: int
    name: str
    category: str
    size: str
    color: str
    price: float
    image_url: str

class SearchRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Supermarket Demo API"}

@app.post("/search", response_model=List[Item])
def search_items(request: SearchRequest):
    """
    Search for items using natural language.
    1. AI interprets the query and generates SQL.
    2. Backend executes SQL against Oracle DB.
    3. Returns list of items.
    """
    user_query = request.query
    print(f"Received query: {user_query}")

    # Step 1: Generate SQL using Vertex AI (Gemini)
    sql_query = ai_controller.generate_sql_query(user_query)
    print(f"Generated SQL: {sql_query}")

    # Step 2: Execute SQL
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Step 3: Format results
        items = []
        for row in rows:
            # Assuming the select * returns columns in order defined in MockCursor
            items.append(Item(
                id=row[0],
                name=row[1],
                category=row[2],
                size=row[3],
                color=row[4],
                price=row[5],
                image_url=row[6]
            ))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
