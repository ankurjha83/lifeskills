from utils import load_json, save_json
from llm_interface import generate_from_template

def generate_scene_outlines():
    chapters = load_json("generated/chapters.json")
    outlines = []

    for chapter in chapters:
        inputs = {
            "chapter_title": chapter["title"]
        }

        print(f"🎬 Generating scene outline for Chapter {chapter['chapter_number']}: {chapter['title']}")
        response = generate_from_template("scene_outline_prompt", inputs)
        scenes = response.strip().split("\n")

        outlines.append({
            "chapter_number": chapter["chapter_number"],
            "chapter_title": chapter["title"],
            "scenes": [s.strip() for s in scenes if s.strip()]
        })

    save_json(outlines, "generated/scene_outlines.json")

if __name__ == "__main__":
    generate_scene_outlines()
