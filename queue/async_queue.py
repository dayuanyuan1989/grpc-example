import asyncio

# 创建一个事件循环
loop = asyncio.get_event_loop()

# 创建一个异步队列
async_queue = asyncio.Queue()

# 同步函数
def sync_function(data):
    # 使用 run_until_complete 在同步函数中往异步队列发送数据
    loop.run_until_complete(async_queue.put(data))
    data = loop.run_until_complete(async_queue.get())
    print(f"Received data: {data}")

# 测试同步函数
sync_function("Hello, asyncio.Queue!")

# 关闭事件循环
loop.close()
