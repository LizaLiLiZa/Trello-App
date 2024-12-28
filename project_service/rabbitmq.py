import aio_pika
import asyncio
from loguru import logger
from config import Config

# Функция для получения асинхронного соединения с RabbitMQ
async def get_connection() -> aio_pika.Connection:
    connection = await aio_pika.connect_robust(
        host=str(Config.rmq_host),  # Преобразуем в строку
        port=Config.rmq_port,
        login=Config.rmq_user,
        password=Config.rmq_password,
    )
    return connection

# Асинхронная функция для обработки входящих сообщений
async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        logger.info(f"Received message: {message.body.decode()}")

# Асинхронная функция для подключения к RabbitMQ и прослушивания очереди
async def listen_for_messages():
    connection = await get_connection()  # Получаем асинхронное соединение
    async with connection:
        channel = await connection.channel()  # Создаем канал

        # Объявляем очередь, если она не существует
        queue = await channel.declare_queue(Config.mq_routing_key, durable=True)

        # Подключаем обработчик сообщений
        await queue.consume(on_message, no_ack=False)

        logger.info(f"Listening for messages on queue: {Config.mq_routing_key}")
        try:
            # Асинхронно ожидаем получения сообщений
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Listening task was cancelled")
