# src/generate_scene_drafts.py

import os
import json
from pathlib import Path
from llm_interface import generate_from_template
from utils import load_inputs

SCENE_DIR = "generated/scenes"

# Sample content for preview mode
PREVIEW_SCENE_DRAFT = """It was just another ordinary Tuesday, or so I thought. The rooftop garden glowed golden under the setting sun, and I was pretending to water Mom's tulsi plant while secretly watching Anaya talk to Grandpa. She was showing off her trophy for the hundredth time.

I wanted to be happy. I really did. But every 'Wow!' from Grandpa felt like a pin poking my balloon of pride. I had drawn a full comic book last week. Nobody clapped. Nobody even noticed.

That's when the idea came to me. If no one saw what I did, maybe I needed to do something... bigger. Something no one could ignore.

I didn't know it yet, but that thought would lead me straight into the biggest emotional muddle of my life."""

def generate_scene_drafts(preview_mode=False):
    inputs = load_inputs()
    print("✏️ Generating full scene drafts...")

    for chapter_folder in sorted(os.listdir(SCENE_DIR)):
        chapter_path = os.path.join(SCENE_DIR, chapter_folder)
        scenes_json = os.path.join(chapter_path, "scenes.json")

        if not os.path.exists(scenes_json):
            print(f"  ⚠️ Skipping {chapter_folder} – scenes.json not found.")
            continue

        with open(scenes_json, "r", encoding="utf-8") as f:
            scenes = json.load(f)

        for scene in scenes:
            scene_num = scene.get("scene_number")
            scene_title = scene.get("title")
            print(f"  ✍️ Scene {scene_num}: {scene_title}")

            prompt_vars = {
                "book_title": inputs.get("Book Title"),
                "main_characters": inputs.get("Main Character(s)", []),
                "tone": inputs.get("Tone"),
                "scene_title": scene.get("title"),
                "setting": scene.get("setting"),
                "emotional_tone": scene.get("emotional_tone"),
                "learning_or_struggle": scene.get("learning_or_struggle"),
                "scene_word_count": scene.get("word_count", "600"),
                "chapter_number": chapter_folder.split("_")[-1]
            }

            try:
                if preview_mode:
                    print("    ⚙️ Preview mode active – using sample scene draft.")
                    draft = PREVIEW_SCENE_DRAFT
                else:
                    draft = generate_from_template("scene_draft_prompt", prompt_vars)

                scene_filename = os.path.join(chapter_path, f"scene_{scene_num}.md")
                with open(scene_filename, "w", encoding="utf-8") as f:
                    f.write(draft.strip() + "\n")

                print(f"    ✅ Saved: {scene_filename}")

            except Exception as e:
                print(f"    ❌ Error in {chapter_folder} scene {scene_num}: {e}")

if __name__ == "__main__":
    import sys
    preview = "--preview" in sys.argv
    generate_scene_drafts(preview_mode=preview)
