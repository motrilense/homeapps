from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI()

# Simple in-memory list to store user text entries
text_storage = []


class TextEntry(BaseModel):
    text: str


# API Endpoint to add a new text entry
@app.post("/api/entries")
async def add_entry(entry: TextEntry):
    stripped_text = entry.text.strip()
    if not stripped_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text_storage.append(stripped_text)
    return {"message": "Success"}


# API Endpoint to get all entries sorted alphabetically
@app.get("/api/entries")
async def get_entries():
    return sorted(text_storage, key=str.lower)


# Serve the HTML frontend at the root URL
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(index_path, "r", encoding="utf-8") as file:
        return file.read()
