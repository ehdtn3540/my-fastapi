from fastapi import APIRouter
from core.clients import http_client

# JsonPlaceHolder API
router = APIRouter(prefix="/jsonplaceholder", tags=["jsonplaceholder"])

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

@router.get("/combined_posts")
async def get_combined_posts():
    posts    = await get_posts()
    comments = await get_comments()
    users    = await get_users()

    combined_list = []
    combined_list.append(posts[0])
    combined_list.append(comments[0])
    combined_list.append(users[0])

    return combined_list
