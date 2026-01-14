"""
LiteLLM 工具调用 (Function Calling) 示例 - DeepSeek
展示如何定义和处理工具调用
"""

import os
import json
from dotenv import load_dotenv
from litellm import completion

load_dotenv()


# 定义工具函数
def get_weather(location: str, unit: str = "celsius") -> dict:
    """模拟获取天气信息"""
    # 实际应用中这里会调用真实的天气 API
    weather_data = {
        "北京": {"temp": 15, "condition": "晴"},
        "上海": {"temp": 18, "condition": "多云"},
        "广州": {"temp": 25, "condition": "阴"},
    }

    data = weather_data.get(location, {"temp": 20, "condition": "未知"})
    temp = data["temp"] if unit == "celsius" else data["temp"] * 9/5 + 32

    return {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "condition": data["condition"]
    }


def calculate(expression: str) -> dict:
    """计算数学表达式"""
    try:
        result = eval(expression)  # 注意：生产环境不要使用 eval
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"expression": expression, "error": str(e)}


# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，如：2+2、10*5"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 可用函数映射
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate
}


def process_tool_call(user_message: str):
    """处理包含工具调用的对话"""
    messages = [{"role": "user", "content": user_message}]

    print(f"用户: {user_message}\n")

    # 第一次调用：让模型决定是否使用工具
    response = completion(
        model="deepseek/deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if not tool_calls:
        # 模型没有调用工具，直接返回响应
        print(f"助手: {response_message.content}")
        return

    # 处理工具调用
    messages.append(response_message)

    print(f"模型请求调用 {len(tool_calls)} 个工具:")

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        print(f"  - {function_name}({function_args})")

        # 执行函数
        function_to_call = available_functions[function_name]
        function_result = function_to_call(**function_args)

        print(f"    结果: {function_result}")

        # 将函数结果添加到消息中
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_result, ensure_ascii=False)
        })

    # 第二次调用：让模型根据工具结果生成最终响应
    print("\n生成最终响应...")
    final_response = completion(
        model="deepseek/deepseek-chat",
        messages=messages
    )

    print(f"\n助手: {final_response.choices[0].message.content}")


if __name__ == "__main__":
    print("=" * 50)
    print("示例 1: 天气查询 (DeepSeek)")
    print("=" * 50)
    process_tool_call("北京今天天气怎么样？")

    print("\n" + "=" * 50)
    print("示例 2: 数学计算")
    print("=" * 50)
    process_tool_call("帮我计算 125 * 8 + 50")

    print("\n" + "=" * 50)
    print("示例 3: 普通对话（不触发工具）")
    print("=" * 50)
    process_tool_call("你好，介绍一下你自己")
