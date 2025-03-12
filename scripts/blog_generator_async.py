import time
import uuid
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

import requests
import aiohttp

from db_operations import clear_blogs_database
from blog.schemas import BlogBase

# Константы для API
API_BASE_URL = "http://localhost:8000"
BLOG_ENDPOINT = f"{API_BASE_URL}/blog"
LOGIN_ENDPOINT = f"{API_BASE_URL}/login"

processes_quantity = multiprocessing.cpu_count()

def get_auth_token() -> str:
    auth_data = {
        "username": "user_1@example.com",
        "password": "user_1"
    }
    auth_response = requests.post(LOGIN_ENDPOINT, data=auth_data)
    auth_token = auth_response.json().get("access_token")
    return auth_token


def blog_generator(n: int, queue: multiprocessing.Queue) -> None:
    for _ in range(n):
        title = str(uuid.uuid4())
        print(f'Генерация блога: {title}')
        time.sleep(0.1)
        blog = BlogBase(title=title, body=str(uuid.uuid4()))
        queue.put(blog)
    queue.put(None)


async def save_blog_to_db_async(
        blog_data: BlogBase,
        session: aiohttp.ClientSession,
        auth_token: str = None
) -> bool:
    
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    async with session.post(
        BLOG_ENDPOINT,
        headers=headers,
        json=blog_data.model_dump()
    ) as response:
        if response.status != 201:
            print(f"Ошибка сохранения блога: {blog_data.title}")
            return False
        else:
            print(f"Блог сохранен: {blog_data.title}")
            return True


async def main():
    clear_blogs_database()
    blogs_quantity = 50
    start_time = time.perf_counter()
    auth_token = get_auth_token()
    
    manager = multiprocessing.Manager()
    blog_queue = manager.Queue()
    
    print(f'Начало генерации и сохранения блогов в количестве {blogs_quantity} шт.')
    blogs = []
    
    loop = asyncio.get_running_loop()
    
    with ProcessPoolExecutor(max_workers=processes_quantity) as executor:
        loop.run_in_executor(
            executor,
            blog_generator,
            blogs_quantity,
            blog_queue
        )
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            while True:
                blog = await loop.run_in_executor(None, blog_queue.get)
                if blog is None:
                    break
                blogs.append(blog)
                task = asyncio.create_task(save_blog_to_db_async(
                    blog,
                    session,
                    auth_token
                ))
                tasks.append(task)

            await asyncio.gather(*tasks)
            
    print(f'Окончание генерации и сохранения блогов, '
          f'прошло времени: {(time.perf_counter() - start_time):.2f} сек'
    )
    print(f'Успешно сохранено блогов: {len(blogs)} из {blogs_quantity}')


if __name__ == "__main__":
    asyncio.run(main())
