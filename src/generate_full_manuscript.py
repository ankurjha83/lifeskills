# src/generate_full_manuscript.py

import os
import json

CHAPTERS_JSON = "generated/chapters.json"
CHAPTERS_DIR = "generated/chapters_draft"
OUTPUT_FILE = "generated/full_manuscript.md"

def compile_manuscript():
    print("📖 Compiling full manuscript...")

    with open(CHAPTERS_JSON, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    full_text = "# Manuscript\n\n"

    for chapter in chapters:
        num = chapter["chapter_number"]
        title = chapter["title"]
        chapter_file = os.path.join(CHAPTERS_DIR, f"chapter_{num}.md")

        if not os.path.exists(chapter_file):
            raise FileNotFoundError(f"Missing draft for Chapter {num}: {title}")

        with open(chapter_file, "r", encoding="utf-8") as f:
            chapter_text = f.read().strip()

        full_text += f"## Chapter {num}: {title}\n\n{chapter_text}\n\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_text.strip())

    print(f"✅ Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    compile_manuscript()
