# src/generate_chapter_drafts.py

import os
from pathlib import Path
import sys

SCENE_DIR = "generated/scenes"
OUTPUT_DIR = "generated/chapters_draft"

def get_scene_files(chapter_path):
    return sorted(
        [f for f in os.listdir(chapter_path) if f.startswith("scene_") and f.endswith(".md")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )

def compile_chapter_draft(chapter_number, scene_files, chapter_path):
    lines = []
    for filename in scene_files:
        with open(os.path.join(chapter_path, filename), "r", encoding="utf-8") as f:
            lines.append(f.read().strip())
            lines.append("\n\n---\n\n")  # separator between scenes
    return "".join(lines)

def generate_chapter_drafts():
    print("📚 Compiling chapter drafts from scenes...")

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    chapters = sorted(
        [d for d in os.listdir(SCENE_DIR) if d.startswith("chapter_")],
        key=lambda x: int(x.split("_")[1])
    )

    for chapter_dir in chapters:
        chapter_number = int(chapter_dir.split("_")[1])
        chapter_path = os.path.join(SCENE_DIR, chapter_dir)

        scene_files = get_scene_files(chapter_path)

        if not scene_files:
            print(f"❌ ERROR: Chapter {chapter_number} has no scene files. Please generate scenes before compiling.")
            sys.exit(1)

        draft = compile_chapter_draft(chapter_number, scene_files, chapter_path)

        output_file = os.path.join(OUTPUT_DIR, f"chapter_{chapter_number}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(draft.strip() + "\n")

        print(f"✅ Saved: {output_file}")

if __name__ == "__main__":
    generate_chapter_drafts()
