import time
import requests
from typing import Generator, List
import uuid
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from db_operations import clear_blogs_database
from blog.schemas import BlogBase
import multiprocessing

# Константы для API
API_BASE_URL = "http://localhost:8000"
BLOG_ENDPOINT = f"{API_BASE_URL}/blog"
LOGIN_ENDPOINT = f"{API_BASE_URL}/login"

processes_quantity = multiprocessing.cpu_count()

def get_auth_token():
    auth_data = {
        "username": "user_3@example.com",
        "password": "user_3"
    }
    auth_response = requests.post(LOGIN_ENDPOINT, data=auth_data)
    auth_token = auth_response.json().get("access_token")
    return auth_token


def blog_generator() -> BlogBase:
    title = str(uuid.uuid4())
    print(f'Генерация блога: {title}')
    time.sleep(0.1)
    return BlogBase(
        title=title,
        body=str(uuid.uuid4())
    )


def save_blog_to_db(blog_data: BlogBase, auth_token: str = None) -> bool:
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    try:
        blog_dict = blog_data.model_dump()
        
        response = requests.post(
            BLOG_ENDPOINT,
            headers=headers,
            json=blog_dict
        )
        if response.status_code != 201:
            print(f"Ошибка сохранения блога: {blog_data.title}")
            return False
        else:
            print(f"**Блог сохранен: {blog_data.title}**")
        return True
    except Exception as e:
        print(f"Ошибка сохранения блога: {e}")
        return False


def main():
    clear_blogs_database()
    blogs_quantity = 50
    threads_quantity = 20
    start_time = time.perf_counter()
    auth_token = get_auth_token()
    
    manager = multiprocessing.Manager()
    blog_queue = manager.Queue()
    
    print(f'Начало генерации и сохранения блогов в количестве {blogs_quantity}')
    blogs = []
    
    with ThreadPoolExecutor(max_workers=threads_quantity) as thread_executor:
        futures = [
            thread_executor.submit(lambda: save_blog_to_db(blog_queue.get(), auth_token))
            for _ in range(blogs_quantity)
        ]
                
        with ProcessPoolExecutor(max_workers=processes_quantity) as process_executor:
            futures = [
                process_executor.submit(blog_queue.put, blog_generator())
                for _ in range(blogs_quantity)
            ]

            for future in futures:
                blogs.append(future.result())
        
        for _ in range(threads_quantity):
            blog_queue.put(None)
        
        for future in futures:
            future.result()
        
    print(f'Окончание генерации и сохранения блогов, '
          f'прошло времени: {(time.perf_counter() - start_time):.2f} сек'
    )
    
if __name__ == "__main__":
    main()
