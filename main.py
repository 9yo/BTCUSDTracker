import asyncio
import datetime
import json
import requests
import websockets


async def get_data():
    # URL для получения данных
    url = "https://blockchain.info/ticker"

    # Выполнение HTTP-запроса
    response = requests.get(url)

    # Проверка успешности выполнения запроса
    if response.status_code == 200:
        # Получение данных из ответа
        data = response.json()

        # Формирование объекта с данными и временной меткой
        result = {
            "timestamp": int(datetime.datetime.now().timestamp()),
            "data": data["USD"]
        }

        return result
    else:
        # В случае ошибки возвращаем None
        return None


async def send_data():
    # Создание веб-сокет сервера
    async with websockets.serve(handler, "0.0.0.0", 9000):
        while True:
            # Получение данных
            data = await get_data()
            print(data)
            if data is not None:
                # Отправка данных клиентам
                await handler.broadcast(json.dumps(data))

            # Задержка в 5 секунд
            await asyncio.sleep(5)


class WebSocketHandler:
    def __init__(self):
        self.clients = set()

    async def register(self, websocket):
        self.clients.add(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def broadcast(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handle(self, websocket, path):
        # Регистрация нового клиента
        await self.register(websocket)

        try:
            # Бесконечный цикл чтения сообщений от клиента
            async for message in websocket:
                pass
        finally:
            # Удаление клиента из списка
            await self.unregister(websocket)


handler = WebSocketHandler()

asyncio.run(send_data())

