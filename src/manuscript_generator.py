import json
import os
import re
from pathlib import Path
from llm_interface import generate_from_template

INPUT_PATH = "data/inputs_from_sheets.json"
OUTPUT_DIR = "generated"
OVERVIEW_FILE = os.path.join(OUTPUT_DIR, "overview.md")
CHAPTER_JSON = os.path.join(OUTPUT_DIR, "chapters.json")
CHAPTER_MD = os.path.join(OUTPUT_DIR, "chapters.md")


def load_inputs():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_markdown(text, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    print(f"✅ Saved: {path}")


def generate_book_overview():
    inputs = load_inputs()
    print("📚 Generating Book Overview...")
    overview = generate_from_template("book_overview_prompt", inputs)
    save_markdown(overview, OVERVIEW_FILE)


def parse_chapter_response(raw_text):
    chapters = []
    for line in raw_text.split("\n"):
        if line.strip() and line.strip()[0].isdigit():
            try:
                parts = line.strip().split(":", 1)
                number = int(parts[0].strip())
                rest = parts[1].strip()
                # Split the rest into title and summary
                if "–" in rest:
                    title, summary = rest.split("–", 1)
                elif "-" in rest:
                    title, summary = rest.split("-", 1)
                else:
                    title, summary = rest, ""
                # Clean up title if it starts with "Chapter X:"
                title = re.sub(r"^Chapter\s+\w+:\s*", "", title, flags=re.IGNORECASE).strip()
                chapters.append({
                    "chapter_number": number,
                    "title": title.strip(),
                    "summary": summary.strip()
                })
            except Exception:
                print(f"⚠️ Skipped line due to parsing error: {line}")
    return chapters


def save_chapters(chapters):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CHAPTER_JSON, "w", encoding="utf-8") as f:
        json.dump(chapters, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {CHAPTER_JSON}")

    with open(CHAPTER_MD, "w", encoding="utf-8") as f:
        for ch in chapters:
            f.write(f"### Chapter {ch['chapter_number']}: {ch['title']}\n")
            f.write(f"{ch['summary']}\n\n")
    print(f"✅ Saved: {CHAPTER_MD}")


def generate_chapter_outline():
    inputs = load_inputs()
    print("📖 Generating Chapter Outline...")
    response = generate_from_template("chapter_outline_prompt", inputs)
    chapters = parse_chapter_response(response)
    save_chapters(chapters)


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
                "title": number_title[1].strip(),
                "setting": "",
                "emotional_tone": "",
                "learning_or_struggle": "",
                "word_count": ""
            }

        elif line.lower().startswith("setting:"):
            current_scene["setting"] = line.split(":", 1)[1].strip()

        elif line.lower().startswith("emotional tone:"):
            current_scene["emotional_tone"] = line.split(":", 1)[1].strip()

        elif "learn" in line.lower() or "struggle" in line.lower():
            current_scene["learning_or_struggle"] = line.split(":", 1)[1].strip()

        elif "word count" in line.lower():
            current_scene["word_count"] = line.split(":", 1)[1].strip()

    if current_scene:
        scenes.append(current_scene)

    return scenes


def generate_scene_breakdowns():
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
            "book_title": inputs["Book Title"],
            "target_age": inputs["Target Age"],
            "life_skill_theme": inputs["Life Skill Theme"],
            "chapter_title": chapter_title,
            "chapter_summary": chapter_summary,
            "chapter_number": chapter_num,
            "scene_word_count": inputs.get("Scene Word Count Goal", "600")
        }

        raw_response = generate_from_template("chapter_scene_breakdown_prompt", prompt_vars)
        scenes = parse_scene_response(raw_response)

        chapter_scene_dir = os.path.join(OUTPUT_DIR, "scenes", f"chapter_{chapter_num}")
        Path(chapter_scene_dir).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(chapter_scene_dir, "scenes.json"), "w", encoding="utf-8") as f:
            json.dump(scenes, f, indent=2, ensure_ascii=False)

        with open(os.path.join(chapter_scene_dir, "scenes.md"), "w", encoding="utf-8") as f:
            for scene in scenes:
                f.write(f"#### Scene {scene['scene_number']}: {scene['title']}\n")
                f.write(f"- 📍 Setting: {scene['setting']}\n")
                f.write(f"- 🎭 Tone: {scene['emotional_tone']}\n")
                f.write(f"- 🎓 Learning: {scene['learning_or_struggle']}\n")
                f.write(f"- ✍️ Word Count: {scene['word_count']}\n\n")

        print(f"    ✅ Saved: chapter_{chapter_num}/scenes.json and scenes.md")


if __name__ == "__main__":
    generate_book_overview()
    generate_chapter_outline()
    generate_scene_breakdowns()
