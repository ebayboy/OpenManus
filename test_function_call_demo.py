import json

from openai import OpenAI

# 1. 设置 OpenAI API Key

llm = OpenAI(
    base_url="http://gpt-proxy.jd.com/gateway/common/",
    api_key="a84d65a3-3882-4637-b6cb-58921899cd9c",
)


# 2. 定义工具（函数）列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：北京",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位",
                    },
                },
                "required": ["location"],
            },
        },
    }
]


# 3. 模拟的天气函数（实际开发中这里应该调用真实API）
def get_current_weather(location, unit="celsius"):
    """模拟天气数据返回"""
    weather_data = {
        "location": location,
        "temperature": "22" if unit == "celsius" else "72",
        "unit": unit,
        "forecast": ["晴朗", "微风"],
    }
    return json.dumps(weather_data)


# 4. 主对话函数
def run_conversation():
    # 用户消息
    user_message = "北京现在的天气怎么样？"

    # 第一步：发送用户消息给模型
    response = llm.chat.completions.create(
        model="gpt-4o-0806",  # 或 gpt-4-1106-preview
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
        tool_choice="auto",  # 让模型决定是否调用函数
    )

    response_message = response.choices[0].message

    # 第二步：检查模型是否想调用函数
    if response_message.tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
        }

        # 第三步：调用模型请求的函数
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # 执行对应的本地函数
            function_response = available_functions[function_name](
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )

            # 第四步：将函数返回发送给模型
            second_response = llm.chat.completions.create(
                model="gpt-4o-0806",
                messages=[
                    {"role": "user", "content": user_message},
                    response_message,
                    {
                        "role": "tool",
                        "content": function_response,
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                    },
                ],
            )

            return second_response.choices[0].message.content

    return response_message.content


# 5. 执行对话
print(run_conversation())
