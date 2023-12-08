import asyncio
from queue import Queue

# 同步队列
sync_queue = Queue()
sync_queue.put(None)
sync_queue.put("a")

# 异步函数
async def async_function():
    while True:
        # 使用 run_in_executor 在异步函数中读取同步队列
        item = await asyncio.get_event_loop().run_in_executor(None, sync_queue.get)
        if item is None:
            continue
        print(f"Async Function: Got item from sync queue: {item}")

# 启动异步函数
asyncio.run(async_function())
