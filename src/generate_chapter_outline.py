# src/generate_chapter_outline.py

import os
import json
import re
from llm_interface import generate_from_template
from utils import load_inputs, save_markdown

OUTPUT_DIR = "generated"
CHAPTER_JSON = os.path.join(OUTPUT_DIR, "chapters.json")
CHAPTER_MD = os.path.join(OUTPUT_DIR, "chapters.md")

def parse_chapter_response(raw_text):
    chapters = []
    for line in raw_text.split("\n"):
        if not line.strip():
            continue

        # Match patterns like:
        # 1. Chapter One: Title – Summary
        # 1. Title – Summary
        match = re.match(r"^\s*(\d+)[\.\)]?\s*(.*)", line.strip())
        if not match:
            print(f"⚠️ Skipped line due to no number match: {line}")
            continue

        chapter_number = int(match.group(1))
        content = match.group(2)

        # Try to split by dash or en-dash or colon
        for sep in [" – ", " - ", " — ", ":", "–", "-"]:
            if sep in content:
                parts = content.split(sep, 1)
                title = parts[0].strip()
                summary = parts[1].strip()
                break
        else:
            print(f"⚠️ Skipped line due to no separator: {line}")
            continue

        chapters.append({
            "chapter_number": chapter_number,
            "title": title,
            "summary": summary
        })

    return chapters

def generate_chapter_outline():
    inputs = load_inputs()
    print("📖 Generating Chapter Outline...")

    response = generate_from_template("chapter_outline_prompt", inputs)
    chapters = parse_chapter_response(response)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CHAPTER_JSON, "w", encoding="utf-8") as f:
        json.dump(chapters, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {CHAPTER_JSON}")

    with open(CHAPTER_MD, "w", encoding="utf-8") as f:
        for ch in chapters:
            f.write(f"### Chapter {ch['chapter_number']}: {ch['title']}\n")
            f.write(f"{ch['summary']}\n\n")
    print(f"✅ Saved: {CHAPTER_MD}")

if __name__ == "__main__":
    generate_chapter_outline()
