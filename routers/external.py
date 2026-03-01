from fastapi import APIRouter
from core.clients import http_client

# JsonPlaceHolder API
router = APIRouter(prefix="/api", tags=["external"])

@router.get("/posts")
async def get_posts():
    response = await http_client.client.get("https://jsonplaceholder.typicode.com/posts")
    return response.json()

@router.get("/comments")
async def get_comments():
    response = await http_client.client.get("https://jsonplaceholder.typicode.com/comments")
    return response.json()

@router.get("/users")
async def get_users():
    response = await http_client.client.get("https://jsonplaceholder.typicode.com/users")
    return response.json()
