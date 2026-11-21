"""从 ryanuo.cc/sitemap.json 生成文章概括，写入 summaries.json。

纯本地 summa 生成，除拉取 sitemap 外无网络依赖。已生成过的条目会跳过，
可增量重跑。生成参数 SUMMARY_RATIO 可按需调整（越小越短，质量越一般）。
"""

import json
import sys
from pathlib import Path

import requests
from summa.summarizer import summarize

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from api.utils.markdown import compress_markdown  # noqa: E402

SITEMAP_URL = "https://ryanuo.cc/sitemap.json"
SUMMARIES_FILE = PROJECT_ROOT / "summaries.json"
SUMMARY_RATIO = 0.05


def main():
    data = requests.get(SITEMAP_URL, timeout=30).json()
    items = data["items"]

    summaries = {}
    if SUMMARIES_FILE.exists():
        summaries = json.loads(SUMMARIES_FILE.read_text(encoding="utf-8"))

    for i, item in enumerate(items, 1):
        url = item["url"]
        if url in summaries:
            continue  # 已生成过，跳过

        try:
            content = compress_markdown(
                summarize(item["text"], ratio=SUMMARY_RATIO)
            )
        except Exception:
            content = ""
        if not content:
            # 短文 summa 无句可抽，回退用 sitemap 自带的 summary
            content = compress_markdown(item.get("summary", "") or "")
        summaries[url] = content
        print(f"[{i}/{len(items)}] {url} ({len(content)} 字)")

    SUMMARIES_FILE.write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"完成：共 {len(summaries)} 条，写入 {SUMMARIES_FILE}")


if __name__ == "__main__":
    main()
