import os
import json
import re
import sys
from pathlib import Path
from llm_interface import generate_from_template
from utils import load_inputs

CHAPTER_JSON = "generated/chapters.json"
SCENE_DIR = "generated/scenes"

def parse_scene_response(raw_text):
    scenes = []
    current_scene = {}

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r"^\d+[\.\)]\s", line):
            if current_scene:
                scenes.append(current_scene)
            number_title = re.split(r"\s", line, maxsplit=1)
            current_scene = {
                "scene_number": int(number_title[0].strip(".)")),
                "title": number_title[1].strip() if len(number_title) > 1 else "",
                "setting": "",
                "emotional_tone": "",
                "learning_or_struggle": "",
                "word_count": ""
            }
        elif line.lower().startswith("setting:"):
            current_scene["setting"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("emotional tone:"):
            current_scene["emotional_tone"] = line.split(":", 1)[1].strip()
        elif "learns" in line.lower() or "lesson" in line.lower() or "struggles" in line.lower():
            current_scene["learning_or_struggle"] = line.split(":", 1)[1].strip()
        elif "word count" in line.lower():
            current_scene["word_count"] = line.split(":", 1)[1].strip()

    if current_scene:
        scenes.append(current_scene)
    return scenes

def generate_scene_breakdowns(preview_mode=False):
    inputs = load_inputs()
    print("🎬 Generating scene outlines for each chapter...")

    with open(CHAPTER_JSON, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    for chapter in chapters:
        chapter_num = chapter["chapter_number"]
        chapter_title = chapter["title"]
        chapter_summary = chapter["summary"]
        print(f"  📘 Chapter {chapter_num}: {chapter_title}")

        prompt_vars = {
            "book_title": inputs.get("Book Title"),
            "target_age": inputs.get("Target Age"),
            "life_skill_theme": inputs.get("Life Skill Theme"),
            "chapter_title": chapter_title,
            "chapter_summary": chapter_summary,
            "chapter_number": chapter_num,
            "scene_word_count": inputs.get("Scene Word Count Goal", "600")
        }

        try:
            if preview_mode:
                print("    ⚙️ Preview mode active — using sample text.")
                raw = """1. The Curious Beginning
Setting: Rooftop garden at sunset  
Emotional Tone: Curious and hopeful  
What the protagonist learns or struggles with: Wonders can begin in the most ordinary places  
Word Count: 600"""
            else:
                raw = generate_from_template("chapter_scene_breakdown_prompt", prompt_vars)

            print("    🔍 Raw GPT output:\n", raw)

            scenes = parse_scene_response(raw)
            print("    🧩 Parsed scenes:", scenes)

            chapter_path = os.path.join(SCENE_DIR, f"chapter_{chapter_num}")
            Path(chapter_path).mkdir(parents=True, exist_ok=True)

            with open(os.path.join(chapter_path, "scenes.json"), "w", encoding="utf-8") as f:
                json.dump(scenes, f, indent=2, ensure_ascii=False)

            with open(os.path.join(chapter_path, "scenes.md"), "w", encoding="utf-8") as f:
                for s in scenes:
                    f.write(f"#### Scene {s.get('scene_number', '?')}: {s.get('title', 'Untitled')}\n")
                    f.write(f"- 📍 Setting: {s.get('setting', 'Unknown')}\n")
                    f.write(f"- 🎭 Tone: {s.get('emotional_tone', 'Neutral')}\n")
                    f.write(f"- 🎓 Learning: {s.get('learning_or_struggle', 'N/A')}\n")
                    f.write(f"- ✍️ Word Count: {s.get('word_count', 'N/A')}\n\n")

            print(f"    ✅ Saved: chapter_{chapter_num}/scenes.json and scenes.md")

        except Exception as e:
            print(f"    ❌ Error generating scenes for Chapter {chapter_num}: {e}")

if __name__ == "__main__":
    preview_mode = "--preview" in sys.argv
    generate_scene_breakdowns(preview_mode=preview_mode)
