import requests
from typing import Generator
import uuid

def get_auth_token():
    auth_data = {
        "username": "your_username",
        "password": "your_password"
    }
    auth_response = requests.post("http://localhost:8000/login", data=auth_data)
    auth_token = auth_response.json().get("access_token")
    return auth_token


def blog_generator(num_posts: int) -> Generator[dict, None, None]:
    for _ in range(num_posts):
        yield {
            "title": str(uuid.uuid4()),
            "content": str(uuid.uuid4())
        }


def main():
    pass
    

if __name__ == "__main__":
    main()
