import requests


def get_url_post_text(url) -> str:
    # 获取 JSON 数据
    data = requests.get("https://ryanuo.cc/sitemap.json").json()
    # 遍历每个条目
    for item in data["items"]:
        # 提取 URL 和文本内容，并存储到字典中
        if item["url"] == url:
            return item["text"]
