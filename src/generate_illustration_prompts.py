# src/generate_illustration_prompts.py

import os
import json
from pathlib import Path
from utils import load_inputs, save_json

CHAPTER_JSON = "generated/chapters.json"
OUTPUT_PATH = "generated/illustration_prompts.json"


def generate_illustration_prompts():
    inputs = load_inputs()
    book_title = inputs.get("Book Title")
    life_skill = inputs.get("Life Skill Theme")
    tone = inputs.get("Tone")
    genre = inputs.get("Genre Style")
    cultural_setting = inputs.get("Cultural Setting")

    with open(CHAPTER_JSON, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    prompts = {
        "book_cover": f"Create a vibrant, cartoon-style book cover illustration for a middle-grade chapter book titled '{book_title}'. Follow Kindle Direct Publishing (KDP) guidelines for size and bleed. Avoid human figures; focus on objects, setting, or symbols that reflect the theme: '{life_skill}'. Style: flat 2D, soft gradients, rounded shapes, playful and clean.",

        "a_plus_headline": f"Design a compelling visual headline panel for the Amazon A+ content that communicates the core value of the book. Include a catchy tagline like 'Unlocking Emotional Intelligence Through Story'. Style should be engaging for both kids and parents.",

        "a_plus_characters": f"Create a character lineup illustration for the Amazon A+ content page showing the main characters of the story in expressive poses. Ensure each character reflects their personality in clothing, posture, and expression. Style: middle-grade, friendly, clean outlines.",

        "a_plus_life_skill": f"Design an A+ content visual that highlights the key life skill: '{life_skill}'. It should include metaphors or scenes showing a child navigating big feelings or resolving conflict. Use icons or simplified scenes to make the message clear to parents.",

        "a_plus_quote": f"Create an illustration that visualizes a heartfelt or funny quote from the book. Style it like a spotlight panel for the Amazon A+ content — with warm, emotional art.",

        "a_plus_cta": f"Design a panel that encourages parents to buy the book. Text example: 'Give Your Child the Gift of Emotional Intelligence'. Include visual cues like stars, books, kids reading."
    }

    # Chapter-level illustration prompts
    prompts["chapters"] = []
    for ch in chapters:
        chapter_number = ch.get("chapter_number")
        title = ch.get("title")
        summary = ch.get("summary")

        prompts["chapters"].append({
            "chapter_number": chapter_number,
            "title": title,
            "prompt": f"Illustrate a key moment from Chapter {chapter_number} titled '{title}'. The image should reflect the tone '{tone}' and genre '{genre}'. Use expressive visual storytelling to capture the emotional or plot highlight from this chapter: {summary}."
        })

    save_json(prompts, OUTPUT_PATH)
    print(f"✅ Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_illustration_prompts()
