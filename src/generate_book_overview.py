# src/generate_book_overview.py

import os
from llm_interface import generate_from_template
from utils import load_inputs, save_markdown

OUTPUT_PATH = "generated/overview.md"

def generate_book_overview():
    inputs = load_inputs()
    print("📚 Generating Book Overview...")
    overview = generate_from_template("book_overview_prompt", inputs)
    save_markdown(overview, OUTPUT_PATH)

if __name__ == "__main__":
    generate_book_overview()
