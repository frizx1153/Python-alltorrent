from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.responses import JSONResponse
from app.scrappers.tpb import getTPBTorrentData, searchTPB
from app.scrappers.i1337x import search1337x, get1337xTorrentData
from app.scrappers.nyaa import searchNyaa
from app.scrappers.rarbg import searchRarbg, getRarbgTorrentData
import os

# Create the FastAPI app
app = FastAPI() 

# Set the port (default is 8000)
PORT = int(os.getenv("PORT", 8000))

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CORS
    allow_headers=["*"],  # Allow all headers for CORS
)

# Middleware for error handling
@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(status_code=500, content={'reason': str(exc)})

# Root endpoint to check if the app is working
@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}

# Search endpoint for 1337x
@app.get("/search/1337x")
async def search1337xRoute(
    q: str, 
    sort_type: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), 
    sort_mode: Optional[str] = Query(None, regex="^asc$|^desc$"), 
    page: Optional[int] = Query(1, gt=0), 
    nsfw: Optional[bool] = Query(False)
):
    torrents, totalPages = await search1337x(q, sort_type, sort_mode, page, nsfw)
    return {"torrents": torrents, "totalPages": totalPages}

# Search endpoint for Nyaa
@app.get("/search/nyaa")
async def searchNyaaRoute(
    q: str, 
    sort_type: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), 
    sort_mode: Optional[str] = Query(None, regex="^asc$|^desc$"), 
    page: Optional[int] = Query(1, gt=0)
):
    torrents, totalPages = await searchNyaa(q, sort_type, sort_mode, page)
    return {"torrents": torrents, "totalPages": totalPages}

# Search endpoint for Rarbg
@app.get("/search/rarbg")
async def searchRarbgRoute(
    q: str, 
    sort_type: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), 
    sort_mode: Optional[str] = Query(None, regex="^asc$|^desc$"), 
    page: Optional[int] = Query(1, gt=0), 
    nsfw: Optional[bool] = Query(False)
):
    torrents, totalPages = await searchRarbg(q, sort_type, sort_mode, page, nsfw)
    return {"torrents": torrents, "totalPages": totalPages}

# Search endpoint for TPB (The Pirate Bay)
@app.get("/search/tpb")
async def searchTPBRoute(
    q: str, 
    sort_type: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), 
    sort_mode: Optional[str] = Query(None, regex="^asc$|^desc$"), 
    page: Optional[int] = Query(1, gt=0), 
    nsfw: Optional[bool] = Query(False)
):
    torrents, totalPages = await searchTPB(q, sort_type, sort_mode, page, nsfw)
    return {"torrents": torrents, "totalPages": totalPages}

# Get Torrent data from 1337x
@app.get("/get/1337x")
async def get1337xRoute(link: str):
    return {"data": await get1337xTorrentData(link)}

# Get Torrent data from Rarbg
@app.get("/get/rarbg")
async def getRarbgRoute(link: str):
    return {"data": await getRarbgTorrentData(link)}

# Get Torrent data from TPB (The Pirate Bay)
@app.get("/get/tpb")
async def getTPBRoute(link: str):
    return {"data": await getTPBTorrentData(link)}

