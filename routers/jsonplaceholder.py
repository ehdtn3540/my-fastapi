from fastapi import APIRouter
from core.clients import http_client
import asyncio

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
    posts, comments, users = await asyncio.gather(
        get_posts(),
        get_comments(),
        get_users()
    )

    combined_list = []
    for post in posts:
        post_comments = []
        for comment in comments:
            if post.get("id") == comment.get("postId"):
                post_comments.append(comment)
        for user in users:
            if post.get("userId") == user.get("id"):
                post["user"] = user
        post["comments"] = post_comments
        combined_list.append(post)

    return combined_list
