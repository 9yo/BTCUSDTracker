import asyncio
import datetime
import json
import requests
import websockets

data = None
BROADCAST_INTERVAL = 1
READ_INTERVAL = 5


async def get_data():
    global data
    # URL для получения данных
    url = "https://blockchain.info/ticker"

    while True:
        # Выполнение HTTP-запроса
        response = requests.get(url)

        # Проверка успешности выполнения запроса
        if response.status_code == 200:
            # Получение данных из ответа
            response_json = response.json()

            # Формирование объекта с данными и временной меткой
            data = {
                "timestamp": int(datetime.datetime.now().timestamp()),
                "data": response_json["USD"]
            }

            print('DATA UPDATED', data['timestamp'])

        await asyncio.sleep(READ_INTERVAL)


async def send_data():
    # Создание веб-сокет сервера
    async with websockets.serve(handler.handle, "0.0.0.0", 9000):
        while True:
            if data:
                print('BROADCASTING')
                # Отправка данных клиентам
                await handler.broadcast(json.dumps(data))

            await asyncio.sleep(BROADCAST_INTERVAL)


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
        if path != '/test':
            print(f'Aborting connection by using wrong path - {path}')
            await websocket.close(code=1003, reason='Forbidden')
            return

        print('New client connected')
        # Регистрация нового клиента
        await self.register(websocket)

        try:
            # Бесконечный цикл чтения сообщений от клиента
            async for message in websocket:
                print(message)
                pass
        finally:
            # Удаление клиента из списка
            await self.unregister(websocket)


handler = WebSocketHandler()


# запуск корутин
async def main():
    while True:
        await asyncio.gather(send_data(), get_data())


# запуск программы
if __name__ == "__main__":
    asyncio.run(main())
