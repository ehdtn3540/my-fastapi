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

    # User의 ID를 기준으로 매핑 
    user_map = {user['id']: user for user in users}

    # Comment의 ID를 기준으로 매핑
    comment_map = {}
    for comment in comments:
        post_id = comment.get('postId')
        if post_id not in comment_map:
            comment_map[post_id] = []
        comment_map[post_id].append(comment)

    # Post에 각각 User, Comment 정보 매칭 
    combined_list = []
    for post in posts:
        post["user"] = user_map.get(post.get("userId"))
        post["comments"] = comment_map.get(post.get("id"), [])
        combined_list.append(post)

    return combined_list
