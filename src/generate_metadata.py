import os
from llm_interface import generate_from_template
from utils import load_inputs, save_json, save_markdown

OUTPUT_JSON = "generated/metadata.json"
OUTPUT_MD = "generated/metadata.md"

def generate_metadata(preview_mode=False):
    print("📝 Generating Amazon KDP metadata...")

    inputs = load_inputs()
    prompt_vars = {
        "book_title": inputs.get("Book Title"),
        "life_skill_theme": inputs.get("Life Skill Theme"),
        "tone": inputs.get("Tone"),
        "target_age": inputs.get("Target Age"),
        "genre": inputs.get("Genre Style"),
        "summary": inputs.get("Story Premise"),
    }

    if preview_mode:
        print("⚙️ Preview mode active — using sample metadata.")
        metadata = {
            "title": "Money Magic: Smart Financial Habits for Kids",
            "subtitle": "A Life Skills Adventure for Kids Ages 8–12",
            "description": "Join Aarav and Anaya as they turn pocket money into powerful lessons! Through lemonade stands, save jars, and sugar mishaps, kids learn the magic of spending smart, saving steady, and growing big. A delightful, warm story filled with humor and heart.",
            "keywords": ["kids money", "financial literacy", "chapter book", "entrepreneurship for kids", "life skills", "saving and spending", "money habits"],
            "categories": ["JUVENILE NONFICTION / Business & Economics", "JUVENILE FICTION / Social Themes / Values & Virtues"],
            "age_range": "8–12"
        }
    else:
        metadata = generate_from_template("amazon_metadata_prompt", prompt_vars)
        if isinstance(metadata, str):
            # If LLM response is a string, you may want to parse or wrap it here
            metadata = {"raw_output": metadata}

    save_json(metadata, OUTPUT_JSON)

    # Save a human-readable version too
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        if "raw_output" in metadata:
            f.write(metadata["raw_output"])
        else:
            f.write(f"# {metadata.get('title', 'Untitled')}\n\n")
            f.write(f"**Subtitle:** {metadata.get('subtitle', '')}\n\n")
            f.write(f"**Description:**\n{metadata.get('description', '')}\n\n")
            f.write(f"**Keywords:** {', '.join(metadata.get('keywords', []))}\n\n")
            f.write(f"**Categories:**\n{chr(10).join(metadata.get('categories', []))}\n\n")
            f.write(f"**Age Range:** {metadata.get('age_range', '')}\n")

    print(f"✅ Saved: {OUTPUT_JSON}")
    print(f"✅ Saved: {OUTPUT_MD}")

if __name__ == "__main__":
    import sys
    preview = "--preview" in sys.argv
    generate_metadata(preview_mode=preview)
