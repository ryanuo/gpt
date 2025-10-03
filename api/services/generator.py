from os import getenv
from ..utils import handle_ai_response
from .shared_client import client
import requests


def openai_chat_completion(model, messages, temperature=0.7, api_key=None):
    """
    调用 OpenAI Chat Completions 接口
    """
    url = (
        getenv("API_URL") + "/chat/completions"
    ) or "https://api.openai.com/v1/chat/completions"
    print("Using API URL:", url)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or getenv('API_KEY')}",
    }
    data = {"model": model, "messages": messages, "temperature": temperature}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def openai_models_list(api_key=None):
    """
    获取 OpenAI 可用模型列表
    """
    url = getenv("API_URL") + "/models" or "https://api.openai.com/v1/models"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or getenv('API_KEY')}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def select_client():
    if getenv("PROVIDER") == "custom":
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
