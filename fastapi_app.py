from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from main import NewsAggregatorManager
from typing import Optional

app = FastAPI()

# Allow CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsQuery(BaseModel):
    query: str
    region: Optional[str] = None  # Optional, not used in current workflow but for future
    category: Optional[str] = None

@app.post("/news")
async def get_news(news_query: NewsQuery):
    mgr = NewsAggregatorManager()
    # For now, just use the query; region/category can be used for future extensions
    result = await mgr.get_news_summary(news_query.query)
    return result

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True) 