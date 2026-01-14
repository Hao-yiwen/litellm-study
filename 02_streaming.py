"""
LiteLLM 流式输出示例 - DeepSeek
展示如何实现实时的流式响应
"""

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()


def streaming_completion():
    """同步流式输出"""
    print("开始流式输出...\n")

    response = completion(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "user", "content": "写一首关于编程的短诗，大约4行。"}
        ],
        stream=True  # 开启流式
    )

    full_response = ""
    for chunk in response:
        # 获取增量内容
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            print(delta_content, end="", flush=True)
            full_response += delta_content

    print("\n\n--- 完整响应 ---")
    print(full_response)


def streaming_with_metadata():
    """流式输出并收集元数据"""
    print("带元数据的流式输出...\n")

    response = completion(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "user", "content": "列出3个学习Python的建议"}
        ],
        stream=True
    )

    chunks_count = 0
    for chunk in response:
        chunks_count += 1
        delta = chunk.choices[0].delta

        # 检查是否有内容
        if delta.content:
            print(delta.content, end="", flush=True)

        # 检查结束原因
        if chunk.choices[0].finish_reason:
            print(f"\n\n结束原因: {chunk.choices[0].finish_reason}")

    print(f"总共接收 {chunks_count} 个 chunks")


if __name__ == "__main__":
    print("=" * 50)
    print("示例 1: 基础流式输出 (DeepSeek)")
    print("=" * 50)
    streaming_completion()

    print("\n" + "=" * 50)
    print("示例 2: 带元数据的流式输出")
    print("=" * 50)
    streaming_with_metadata()
