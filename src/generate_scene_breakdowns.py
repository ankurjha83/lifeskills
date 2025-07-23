import os
import json
from pathlib import Path
from llm_interface import generate_from_template
from utils import load_inputs

SCENE_OUTLINES_PATH = "generated/scenes/scene_outlines.json"
SCENE_DIR = "generated/scenes"


def parse_scenes_text(scenes_text):
    scenes = []
    scene_blocks = scenes_text.strip().split("\n\n")
    for block in scene_blocks:
        lines = block.strip().split("\n")
        scene_data = {}
        for line in lines:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if "title" in key:
                scene_data["title"] = value
            elif "setting" in key:
                scene_data["setting"] = value
            elif "emotional tone" in key:
                scene_data["emotional_tone"] = value
            elif "learning" in key:
                scene_data["learning_or_struggle"] = value
            elif "word count" in key:
                scene_data["word_count"] = value

        # Infer scene number from order
        scene_data["scene_number"] = len(scenes) + 1
        if scene_data:
            scenes.append(scene_data)
    return scenes


def generate_scene_breakdowns():
    inputs = load_inputs()
    print("\U0001f9e0 Generating scene breakdowns with setting, emotion, and learning...")

    with open(SCENE_OUTLINES_PATH, "r", encoding="utf-8") as f:
        scene_outline_chapters = json.load(f)

    for chapter in scene_outline_chapters:
        chapter_number = chapter["chapter_number"]
        raw_scenes_text = chapter["scenes"]
        parsed_scenes = parse_scenes_text(raw_scenes_text)

        chapter_output_dir = os.path.join(SCENE_DIR, f"chapter_{chapter_number}")
        Path(chapter_output_dir).mkdir(parents=True, exist_ok=True)

        scene_outputs = []
        for scene in parsed_scenes:
            try:
                print(f"    \U0001f50d Scene {scene['scene_number']}: {scene['title']}")
                prompt_vars = {
                    "book_title": inputs.get("Book Title"),
                    "main_characters": inputs.get("Main Character(s)", []),
                    "tone": inputs.get("Tone"),
                    "scene_title": scene["title"],
                    "setting": scene["setting"],
                    "emotional_tone": scene["emotional_tone"],
                    "learning_or_struggle": scene["learning_or_struggle"],
                    "scene_word_count": scene["word_count"],
                    "chapter_number": chapter_number
                }
                # Scene breakdown generation can be enhanced later if needed
                # For now we just store the parsed structure
                scene_outputs.append(scene)
            except Exception as e:
                print(f"    ❌ Error in scene: {e}")

        # Save parsed scenes
        with open(os.path.join(chapter_output_dir, "scenes.json"), "w", encoding="utf-8") as f:
            json.dump(scene_outputs, f, indent=2)
            print(f"    ✅ Saved: {os.path.join(chapter_output_dir, 'scenes.json')}")


if __name__ == "__main__":
    generate_scene_breakdowns()
