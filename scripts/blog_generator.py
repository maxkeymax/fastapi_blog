import time
import requests
from typing import Generator
import uuid

# Константы для API
API_BASE_URL = "http://localhost:8000"
BLOG_ENDPOINT = f"{API_BASE_URL}/blog"
LOGIN_ENDPOINT = f"{API_BASE_URL}/login"


def get_auth_token():
    auth_data = {
        "username": "user_3@example.com",
        "password": "user_3"
    }
    auth_response = requests.post(LOGIN_ENDPOINT, data=auth_data)
    auth_token = auth_response.json().get("access_token")
    return auth_token


def blog_generator(num_posts: int) -> Generator[dict, None, None]:
    for _ in range(num_posts):
        yield {
            "title": str(uuid.uuid4()),
            "body": str(uuid.uuid4())
        }


def save_blog_to_db(blog_data: dict, auth_token: str = None) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    try:
        response = requests.post(
            BLOG_ENDPOINT,
            headers=headers,
            json=blog_data
        )
        if response.status_code != 201:
            print(f"Failed to save blog: {blog_data}")
            return False
        else:
            print(f"Blog saved: {blog_data}")
        return True
    except Exception as e:
        print(f"Error saving blog: {e}")
        return False


def main():
    blogs_quantity = 5
    count = 0
    start_time = time.perf_counter()
    auth_token = get_auth_token()
    blogs = blog_generator(blogs_quantity)
    
    for blog in blogs:
        save_blog_to_db(blog, auth_token)
        count += 1
        print(f'Прошло времени: {(time.perf_counter() - start_time):.2f} секунд')
    
    print(f'Всего прошло времени: {(time.perf_counter() - start_time):.2f} секунд')
    print(f'Всего постов сохранено: {count}')


if __name__ == "__main__":
    main()
