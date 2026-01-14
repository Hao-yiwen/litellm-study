"""
LiteLLM 异步调用示例 - DeepSeek
展示 acompletion 的使用方式
"""

import os
import asyncio
from dotenv import load_dotenv
from litellm import acompletion

load_dotenv()


async def async_basic():
    """基础异步调用"""
    response = await acompletion(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "user", "content": "用一句话解释什么是异步编程"}
        ]
    )

    print("异步调用结果:")
    print(response.choices[0].message.content)
    return response


async def async_streaming():
    """异步流式输出"""
    print("异步流式输出...\n")

    response = await acompletion(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "user", "content": "简述 Python asyncio 的核心概念"}
        ],
        stream=True
    )

    async for chunk in response:
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            print(delta_content, end="", flush=True)

    print()


async def concurrent_requests():
    """并发多个请求"""
    print("并发发送3个请求...\n")

    messages_list = [
        [{"role": "user", "content": "Python 的优点是什么？用一句话回答"}],
        [{"role": "user", "content": "JavaScript 的优点是什么？用一句话回答"}],
        [{"role": "user", "content": "Rust 的优点是什么？用一句话回答"}],
    ]

    # 创建并发任务
    tasks = [
        acompletion(
            model="deepseek/deepseek-chat",
            messages=messages,
            max_tokens=100
        )
        for messages in messages_list
    ]

    # 并发执行
    responses = await asyncio.gather(*tasks)

    languages = ["Python", "JavaScript", "Rust"]
    for lang, response in zip(languages, responses):
        print(f"{lang}: {response.choices[0].message.content}")
        print()


async def main():
    print("=" * 50)
    print("示例 1: 基础异步调用 (DeepSeek)")
    print("=" * 50)
    await async_basic()

    print("\n" + "=" * 50)
    print("示例 2: 异步流式输出")
    print("=" * 50)
    await async_streaming()

    print("\n" + "=" * 50)
    print("示例 3: 并发请求")
    print("=" * 50)
    await concurrent_requests()


if __name__ == "__main__":
    asyncio.run(main())
