# flake8: noqa: E501

import asyncio


async def taks_with_limit(semaphore, task_content, task):
    async with semaphore:
        await task(task_content)


async def executor_taks(limit, list_content, task):
    semaphore = asyncio.Semaphore(limit)

    # Cria e executa uma tarefa para cada documento com o limite de paralelismo
    tasks = [taks_with_limit(semaphore, task, content) for content in list_content]

    await asyncio.gather(*tasks)
