# src/edit_full_manuscript.py

import os
from llm_interface import generate_from_template
from utils import load_markdown, save_markdown

MANUSCRIPT_PATH = "generated/full_manuscript.md"
EDITED_PATH = "generated/edited_manuscript.md"

def edit_full_manuscript(preview_mode=False):
    print("📖 Compiling full manuscript...")

    manuscript = load_markdown(MANUSCRIPT_PATH)

    print("🪄 Sending manuscript for editing...")

    prompt_vars = {
        "manuscript": manuscript,
    }

    if preview_mode:
        print("⚙️ Preview mode active — using sample edited output.")
        polished = """# Edited Manuscript (Sample)

## Chapter 1: New Beginnings

Aarav stood at the edge of the playground, his cricket bat hanging loosely by his side...

(pretend this is a beautifully edited version)
"""
    else:
        polished = generate_from_template(
            "final_editing_prompt",
            prompt_vars,
            model="gpt-4-1106-preview"
        )

    save_markdown(polished, EDITED_PATH)

if __name__ == "__main__":
    import sys
    preview = "--preview" in sys.argv
    edit_full_manuscript(preview_mode=preview)
