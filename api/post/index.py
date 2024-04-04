# 存储文章数据的 JSON 文件路径
import json
import os
import requests

json_file_path = os.path.join(os.path.dirname(__file__), "articles.json")


def webhook_post():
    # 获取 JSON 数据
    data = requests.get("https://mr90.top/sitemap.json").json()
    # 创建一个空的字典对象，用于存储 URL 和文本内容的映射关系
    url_text_map = {}
    # 遍历每个条目
    for item in data["items"]:
        # 提取 URL 和文本内容，并存储到字典中
        url = item["url"]
        text = item.get("text", "")  # 如果 text 字段不存在，则默认为空字符串
        url_text_map[url] = text
        # 将收到的 JSON 数据保存到文件中
    with open(json_file_path, "w") as f:
        json.dump(url_text_map, f, indent=2)
        f.close()
    return {
        "message": "JSON url_text_map received and saved successfully.",
        "code": 200,
    }


def get_url_post_text(url) -> str:
    # 获取 JSON 数据
    data = requests.get("https://mr90.top/sitemap.json").json()
    # 遍历每个条目
    for item in data["items"]:
        # 提取 URL 和文本内容，并存储到字典中
        if item["url"] == url:
            return item["text"]
