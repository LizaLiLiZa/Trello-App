""" """
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from config import Config
import asyncio

class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = create_async_engine(str(Config.postgres_url), pool_size=20, max_overflow=0)

Session = async_sessionmaker(engine, expire_on_commit=False)

async def check_connection():
    try:
        # Простой запрос на проверку соединения
        async with engine.connect() as conn:
            result = await conn.execute('SELECT 1')
            print("Соединение с базой данных установлено.")
    except Exception as e:
        print(f"Ошибка при подключении: {e}")
    finally:
        await engine.dispose()  # Закрыть соединение

# Запуск проверки
asyncio.run(check_connection())
