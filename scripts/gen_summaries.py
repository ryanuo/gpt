"""从 ryanuo.cc/sitemap.json 生成文章概括，写入 summaries.json。

优先使用 sitemap 自带的 summary（作者手写，质量最好）；缺失时用本地 summa
兜底（先过滤代码行，避免抽出代码片段）。已生成过的条目会跳过，可增量重跑。
"""

import json
import re
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

# 明显的代码/命令行特征，用于从正文中过滤出可读句子
CODE_PATTERNS = re.compile(r"[{};]|->|::|&&|\|\||^\s*(#|//|>|@|\||-{3,}|={3,})")


def extract_prose(text: str) -> str:
    """过滤代码行、URL 行，只保留可读的说明性句子。"""
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or CODE_PATTERNS.search(line):
            continue
        if line.startswith(("http://", "https://")):
            continue
        lines.append(line)
    return " ".join(lines)


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

        # 优先 sitemap 自带摘要
        content = compress_markdown(item.get("summary", "") or "")
        if not content:
            # 兜底：本地 summa，先过滤代码行
            try:
                content = compress_markdown(
                    summarize(extract_prose(item["text"]), ratio=SUMMARY_RATIO)
                )
            except Exception:
                content = ""
        summaries[url] = content
        print(f"[{i}/{len(items)}] {url} ({len(content)} 字)")

    SUMMARIES_FILE.write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"完成：共 {len(summaries)} 条，写入 {SUMMARIES_FILE}")


if __name__ == "__main__":
    main()
