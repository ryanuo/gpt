from .shared_client import client
import requests
from ..config import api_key, api_url, is_custom_provider


def handle_ai_response(completion_content) -> str:
    if completion_content.find("chatkf123") != -1:
        completion_content = "sorry, please retry later...."
    elif completion_content.find("Upgrade for higher rate limits") != -1:
        completion_content = "sorry, please retry later...."
    return completion_content


def openai_chat_completion(model, messages, temperature=0.7):
    """
    调用 OpenAI Chat Completions 接口
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {"model": model, "messages": messages, "temperature": temperature}
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def select_client():
    if is_custom_provider():
        return openai_chat_completion

    return client.chat.completions.create


def extract_content(completion):
    """
    提取 completion 返回的内容，兼容 dict 和 OpenAI SDK 对象。
    """
    try:
        # SDK 对象: 有 .choices
        return completion.choices[0].message.content
    except AttributeError:
        # dict: 用键访问
        return completion["choices"][0]["message"]["content"]


def generate_completion_with_client(model, message):
    cliented = select_client()
    completion = cliented(model=model, messages=message)
    return handle_ai_response(extract_content(completion))


def generate_image_with_client(prompt):
    # 使用 g4f 客户端生成图像
    return client.images.generate(model="flux", prompt=prompt, response_format="url")
