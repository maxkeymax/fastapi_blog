import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from blog.database import SessionLocal
from blog.models import Blog


def clear_blogs_database():
    """
    Очищает все блоги из базы данных.
    База данных: SQLite
    Путь к БД: ./blog.db
    """
    db_path = os.path.join(root_dir, 'blog.db')
    print(f"Очистка базы данных по пути: {db_path}")
    
    db = SessionLocal()
    try:
        db.query(Blog).delete()
        db.commit()
        print("База данных успешно очищена")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при очистке базы данных: {e}")
    finally:
        db.close() 