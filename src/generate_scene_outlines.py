import json
import os
from pathlib import Path
from utils import load_inputs, save_json
from prompts import chapter_scene_breakdown_prompt
from llm import get_llm_response

# ✅ Define locally instead of importing
def load_chapters(path="generated/chapters.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_scene_output(raw_output):
    scenes = []
    current_scene = {}
    for line in raw_output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Scene") and "Title" in line:
            if current_scene:
                scenes.append(current_scene)
                current_scene = {}
            key, value = line.split(":", 1)
            current_scene["title"] = value.strip()
        elif "Setting:" in line:
            current_scene["setting"] = line.split(":", 1)[1].strip()
        elif "Emotional Tone:" in line:
            current_scene["emotional_tone"] = line.split(":", 1)[1].strip()
        elif "Learning:" in line:
            current_scene["learning"] = line.split(":", 1)[1].strip()
        elif "Word Count:" in line:
            current_scene["word_count"] = line.split(":", 1)[1].strip()
    if current_scene:
        scenes.append(current_scene)

    # Validate that each scene has all fields
    complete_scenes = [s for s in scenes if all(k in s for k in ["title", "setting", "emotional_tone", "learning", "word_count"])]
    return complete_scenes if complete_scenes else None

def generate_scene_outlines():
    print("\n📦 Loaded Inputs (normalized):", load_inputs())

    inputs = load_inputs()
    chapters = load_chapters()
    Path("generated/scenes").mkdir(parents=True, exist_ok=True)

    print("🎬 Generating scene outlines for each chapter...")
    print(f"Loaded {len(chapters)} chapters.")

    for idx, chapter in enumerate(chapters[:1], 1):  # Only process 1 for now
        chapter_title = chapter["title"]
        chapter_summary = chapter["summary"]
        print(f"  📘 Chapter {idx}: {chapter_title}")

        success = False
        for attempt in range(3):
            print(f"\n📝 Final Prompt Sent to LLM (chapter_scene_breakdown_prompt):\n" + "-" * 50)
            prompt = chapter_scene_breakdown_prompt.format(
                chapter_number=idx,
                chapter_title=chapter_title,
                chapter_summary=chapter_summary,
            )
            print(prompt + "\n" + "-" * 50)

            llm_response = get_llm_response(prompt)
            os.makedirs(f"generated/scenes/chapter_{idx}", exist_ok=True)
            with open(f"generated/scenes/chapter_{idx}/raw_llm_output.txt", "w", encoding="utf-8") as f:
                f.write(llm_response)

            scenes = parse_scene_output(llm_response)
            if scenes:
                save_json(scenes, f"generated/scenes/chapter_{idx}/scenes.json")
                log_to_pipeline("scene_outlines", chapter_title, True)
                success = True
                break
            else:
                print(f"    ❌ Attempt {attempt + 1}: Incomplete scene data. Retrying...")

        if not success:
            print(f"    🚫 Failed to generate valid scenes for Chapter {idx} after 3 retries.")
            log_to_pipeline("scene_outlines", chapter_title, False)

if __name__ == "__main__":
    generate_scene_outlines()
