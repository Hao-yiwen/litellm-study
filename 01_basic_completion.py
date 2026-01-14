"""
LiteLLM 基础调用示例 - DeepSeek
展示最简单的 completion 调用方式
"""

import os
from dotenv import load_dotenv
from litellm import completion

# 加载环境变量
load_dotenv()


def basic_completion():
    """基础的 chat completion 调用"""
    try:
        response = completion(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个有帮助的助手。"},
                {"role": "user", "content": "用一句话介绍 Python 编程语言。"}
            ],
            temperature=0.7,
            max_tokens=100
        )

        # 获取响应内容
        content = response.choices[0].message.content
        print("模型回复:", content)

        # 查看使用的 token 数量
        print(f"\nToken 使用: {response.usage}")

        return response

    except Exception as e:
        print(f"调用出错: {e}")
        return None


def completion_with_params():
    """带更多参数的调用"""
    response = completion(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "user", "content": "生成3个创意项目名称"}
        ],
        temperature=1.0,      # 更高的随机性
        max_tokens=200,       # 最大生成长度
        top_p=0.9,           # 核采样
        frequency_penalty=0.5,  # 减少重复
        presence_penalty=0.5,   # 鼓励新话题
    )

    print("创意项目名称:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    print("=" * 50)
    print("示例 1: 基础调用 (DeepSeek)")
    print("=" * 50)
    basic_completion()

    print("\n" + "=" * 50)
    print("示例 2: 带参数调用")
    print("=" * 50)
    completion_with_params()
