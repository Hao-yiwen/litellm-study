"""
LiteLLM 多模型示例 - DeepSeek
展示 DeepSeek Chat 和 Reasoner 的对比
"""

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()


# DeepSeek 模型配置
MODELS = {
    "deepseek-chat": {
        "model": "deepseek/deepseek-chat",
        "description": "DeepSeek Chat（通用对话）"
    },
    "deepseek-reasoner": {
        "model": "deepseek/deepseek-reasoner",
        "description": "DeepSeek Reasoner（推理模型）"
    },
}


def call_model(model_key: str, prompt: str):
    """调用指定模型"""
    if model_key not in MODELS:
        print(f"未知的模型: {model_key}")
        return None

    config = MODELS[model_key]
    print(f"使用模型: {config['description']}")
    print(f"模型 ID: {config['model']}")
    print("-" * 40)

    try:
        response = completion(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        message = response.choices[0].message

        # Reasoner 模型有 reasoning_content（思考过程）
        reasoning = getattr(message, "reasoning_content", None)
        if reasoning:
            print(f"思考过程: {reasoning}")
            print("-" * 40)

        print(f"回答: {message.content}")
        print(f"Token 使用: {response.usage}")
        return response

    except Exception as e:
        print(f"调用失败: {e}")
        return None


def compare_models(prompt: str):
    """比较 DeepSeek Chat 和 Reasoner"""
    print(f"问题: {prompt}")
    print("=" * 60)

    for key in ["deepseek-chat", "deepseek-reasoner"]:
        config = MODELS[key]
        print(f"\n【{config['description']}】")
        try:
            response = completion(
                model=config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            message = response.choices[0].message

            # Reasoner 模型显示思考过程
            reasoning = getattr(message, "reasoning_content", None)
            if reasoning:
                print(f"[思考过程]\n{reasoning}\n")

            print(f"[回答]\n{message.content}")
        except Exception as e:
            print(f"调用失败: {e}")

        print("-" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("示例 1: 调用 DeepSeek Chat")
    print("=" * 60)
    call_model("deepseek-chat", "用一句话解释什么是机器学习")

    print("\n" + "=" * 60)
    print("示例 2: 调用 DeepSeek Reasoner")
    print("=" * 60)
    call_model("deepseek-reasoner", "用一句话解释什么是深度学习")

    print("\n" + "=" * 60)
    print("示例 3: 对比两个模型的推理能力")
    print("=" * 60)
    compare_models("9.11 和 9.8 哪个大？请解释你的推理过程。")
