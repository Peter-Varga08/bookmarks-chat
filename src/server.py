import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import polars as pl

from vectordb.index import init_store
from vectordb.utils import search_text

app = FastAPI()
vectorstore = init_store()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including OPTIONS
    allow_headers=["*"],  # Allow all headers
)


class Body(BaseModel):
    text: str


@app.post("/search")
async def search(text: Body) -> str:
    result: pl.DataFrame = search_text(vectorstore, text.text)
    return json.dumps(result["URL"].to_list())


if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=6789, reload=True)
