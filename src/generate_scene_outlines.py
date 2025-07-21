import os
import json
from utils import load_json, save_json
from llm_interface import generate_from_template

def generate_scene_outlines():
    # Load book-level inputs from data/inputs_from_sheets.json
    book_inputs = load_json("data/inputs_from_sheets.json")

    # Load chapter outline from generated/chapters.json
    chapters_path = "generated/chapters.json"
    if not os.path.exists(chapters_path):
        print(f"❌ Missing chapter outline file at {chapters_path}")
        return

    chapters = load_json(chapters_path)
    scene_outlines = []

    for i, chapter in enumerate(chapters, start=1):
        print(f"\n🎬 Generating scene outline for Chapter {i}: {chapter['title']}")
        inputs = {
            "chapter_number": i,
            "chapter_title": chapter["title"],
            "chapter_summary": chapter["summary"],
            "book_title": book_inputs["book_title"]
        }

        try:
            response = generate_from_template("chapter_scene_breakdown_prompt", inputs)
            scene_outlines.append({
                "chapter_number": i,
                "chapter_title": chapter["title"],
                "scenes": response
            })
        except Exception as e:
            print(f"❌ Error generating scenes for Chapter {i}: {e}")

    # Save result
    os.makedirs("generated/scenes", exist_ok=True)
    save_json(scene_outlines, "generated/scenes/scene_outlines.json")
    print("✅ Scene outlines saved to generated/scenes/scene_outlines.json")

if __name__ == "__main__":
    generate_scene_outlines()
