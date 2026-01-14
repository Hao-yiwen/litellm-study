"""
LiteLLM 豆包 (Doubao) 模型示例
字节跳动火山引擎大模型
"""

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# 豆包模型配置
DOUBAO_CONFIG = {
    "model": "openai/doubao-seed-1-8-251228",
    "api_base": "https://ark.cn-beijing.volces.com/api/v3",
}


def get_api_key():
    return os.environ.get("ARK_API_KEY")


def print_response(response):
    """打印响应，包含思考过程"""
    message = response.choices[0].message

    # 检查是否有思考过程
    reasoning = getattr(message, "reasoning_content", None)
    if reasoning:
        print(f"[思考过程]\n{reasoning}\n")
        print("-" * 40)

    print(f"[回答]\n{message.content}")


def basic_chat():
    """基础对话"""
    response = completion(
        model=DOUBAO_CONFIG["model"],
        api_base=DOUBAO_CONFIG["api_base"],
        api_key=get_api_key(),
        messages=[
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ],
        # max_tokens=200,
        max_completion_tokens=1000,
        extra_body={
            "reasoning_effort": "minimal",
            # "max_completion_tokens": 65535,
        }
    )

    print_response(response)
    return response


def reasoning_chat():
    """推理问题 - 展示思考过程"""
    response = completion(
        model=DOUBAO_CONFIG["model"],
        api_base=DOUBAO_CONFIG["api_base"],
        api_key=get_api_key(),
        messages=[
            {"role": "user", "content": "9.11 和 9.8 哪个大？请解释你的推理过程。"}
        ],
        max_tokens=500
    )

    print_response(response)
    return response


def vision_chat():
    """图片理解（多模态）"""
    response = completion(
        model=DOUBAO_CONFIG["model"],
        api_base=DOUBAO_CONFIG["api_base"],
        api_key=get_api_key(),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
                        }
                    },
                    {"type": "text", "text": "这是哪里？描述一下图片内容"}
                ]
            }
        ],
        max_tokens=300
    )

    print_response(response)
    return response


def streaming_chat():
    """流式输出"""
    print("豆包流式输出...\n")

    response = completion(
        model=DOUBAO_CONFIG["model"],
        api_base=DOUBAO_CONFIG["api_base"],
        api_key=get_api_key(),
        messages=[
            {"role": "user", "content": "写一首关于北京的短诗"}
        ],
        stream=True
    )

    for chunk in response:
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            print(delta_content, end="", flush=True)

    print()


if __name__ == "__main__":
    print("=" * 50)
    print("示例 1: 基础对话")
    print("=" * 50)
    basic_chat()

    # print("\n" + "=" * 50)
    # print("示例 2: 推理问题（展示思考过程）")
    # print("=" * 50)
    # reasoning_chat()

    # print("\n" + "=" * 50)
    # print("示例 3: 图片理解（多模态）")
    # print("=" * 50)
    # vision_chat()

    # print("\n" + "=" * 50)
    # print("示例 4: 流式输出")
    # print("=" * 50)
    # streaming_chat()
