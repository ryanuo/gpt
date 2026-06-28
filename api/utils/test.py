from markdown import compress_markdown
from summa.summarizer import summarize

with open("test.md", encoding="utf8") as f:
    md = f.read()

new_md = compress_markdown(md)
summary = summarize(
    new_md,
    ratio=0.3,
)

print("原长度:", len(new_md))
print("压缩后:", len(summary))
print(f"压缩率: {(1-len(summary)/len(new_md))*100:.1f}%")

with open("compressed.md", "w", encoding="utf8") as f:
    f.write(summary)