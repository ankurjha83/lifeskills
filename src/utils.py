import json
import os
import re

INPUT_PATH = "data/inputs_from_sheets.json"
OUTPUT_DIR = "generated"
CHAPTER_JSON = os.path.join(OUTPUT_DIR, "chapters.json")
CHAPTER_MD = os.path.join(OUTPUT_DIR, "chapters.md")

def load_inputs():
    with open("data/inputs_from_sheets.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
    normalized = {
        k.strip().lower().replace(" ", "_").replace("(", "").replace(")", ""): v
        for k, v in raw.items()
    }
    print("📦 Loaded Inputs (normalized):", normalized)
    return normalized

def normalize_keys(d):
    return {k.lower().replace(" ", "_"): v for k, v in d.items()}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {path}")

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

def parse_chapter_response(raw_text):
    """Parse GPT output into structured list of chapters"""
    chapters = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        try:
            # Match formats like "1. Chapter Title – Summary"
            parts = re.split(r"\.\s+", line, maxsplit=1)
            number = int(parts[0])
            rest = parts[1]

            if "–" in rest:
                title, summary = rest.split("–", 1)
            elif "-" in rest:
                title, summary = rest.split("-", 1)
            else:
                title, summary = rest, ""

            chapters.append({
                "chapter_number": number,
                "title": title.strip(),
                "summary": summary.strip()
            })
        except Exception as e:
            print(f"⚠️ Skipped line due to parsing error: {line}")
    return chapters

def generate_chapter_outline():
    inputs = load_inputs()
    print("📖 Generating Chapter Outline...")
    response = generate_from_template("chapter_outline_prompt", inputs)
    chapters = parse_chapter_response(response)
    save_chapters(chapters)

def load_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_markdown(text, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    print(f"✅ Saved: {path}")

if __name__ == "__main__":
    generate_chapter_outline()
