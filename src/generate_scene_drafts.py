import os
import json
from pathlib import Path
from llm_interface import generate_from_template
from utils import load_inputs

SCENE_DIR = "generated/scenes"  # Adjust if your scenes folder path differs

def generate_scene_drafts():
    inputs = load_inputs()
    print("📦 Loaded Inputs (normalized):", inputs)

    protagonist_name = inputs.get("Main Character(s)", "Aarav")
    if isinstance(protagonist_name, list):
        protagonist_name = protagonist_name[0]  # Just pick first if list
    protagonist_age = inputs.get("target_age", "10").split("–")[0]  # Use lower bound age approx

    setting = inputs.get("cultural_setting", "modern Indian school and home life")

    print("✏️ Generating full scene drafts...")

    # For each chapter folder, e.g. chapter_1, chapter_2 ...
    for chapter_folder in sorted(os.listdir(SCENE_DIR)):
        chapter_path = os.path.join(SCENE_DIR, chapter_folder)
        scenes_json_path = os.path.join(chapter_path, "scenes.json")

        if not os.path.exists(scenes_json_path):
            print(f"  ⚠️ Skipping {chapter_folder} – scenes.json not found.")
            continue

        # Load scenes list
        with open(scenes_json_path, "r", encoding="utf-8") as f:
            scenes = json.load(f)

        print(f"  📖 Processing {chapter_folder} with {len(scenes)} scenes")

        previous_scene_summaries = []
        for scene in scenes:
            scene_num = scene.get("scene_number", "Unknown")
            scene_title = scene.get("title", "Untitled")
            print(f"  ✍️ Scene {scene_num}: {scene_title}")

            # Build accumulated previous scene summary section
            if previous_scene_summaries:
                previous_scene_summary_section = (
                    "Previous scenes summary:\n- " + "\n- ".join(previous_scene_summaries)
                )
            else:
                previous_scene_summary_section = ""

            # Prepare variables for prompt
            prompt_vars = {
                "book_title": inputs.get("book_title", "My Book"),
                "scene_title": scene_title,
                "scene_setting": scene.get("setting", ""),
                "scene_tone": scene.get("emotional_tone", ""),
                "scene_lesson": scene.get("learning_or_struggle", ""),
                "protagonist_name": protagonist_name,
                "protagonist_age": protagonist_age,
                "previous_scene_summary_section": previous_scene_summary_section,
                "scene_word_count": scene.get("word_count", "600"),
                "setting": setting,
            }

            try:
                draft = generate_from_template("scene_expansion_prompt", prompt_vars)
                scene_filename = os.path.join(chapter_path, f"scene_{scene_num}.md")
                with open(scene_filename, "w", encoding="utf-8") as f:
                    f.write(draft.strip() + "\n")
                print(f"    ✅ Saved: {scene_filename}")

                # Append current scene lesson for next context
                previous_scene_summaries.append(scene.get("learning_or_struggle", ""))

            except Exception as e:
                print(f"    ❌ Error in {chapter_folder} scene {scene_num}: {e}")

if __name__ == "__main__":
    generate_scene_drafts()
