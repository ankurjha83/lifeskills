import os
import json
import time
from openai import OpenAI
from config_reader import get_openai_key


client = OpenAI(api_key=get_openai_key())

TEMPLATE_PATH = "config/prompt_templates.json"

def load_prompt_template(template_name):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        templates = json.load(f)
    if template_name not in templates:
        raise ValueError(f"Prompt template '{template_name}' not found in {TEMPLATE_PATH}")
    return templates[template_name]

def format_prompt(template, variables):
    try:
        # Convert all variables to strings, join lists
        clean_vars = {
            k: ", ".join(v) if isinstance(v, list) else str(v)
            for k, v in variables.items()
        }
        return template.format(**clean_vars)
    except KeyError as e:
        raise ValueError(f"Missing variable in template: {e}")

def generate_from_template(template_name, variables, model="gpt-3.5-turbo", temperature=0.7, max_retries=3):
    template = load_prompt_template(template_name)
    prompt = format_prompt(template, variables)

    # ✅ Log the final prompt sent to LLM
    print(f"\n📝 Final Prompt Sent to LLM ({template_name}):\n{'-'*50}\n{prompt}\n{'-'*50}\n")

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            wait_time = 5 * (attempt + 1)
            print(f"⚠️ Error on attempt {attempt+1}: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

    raise RuntimeError("❌ Failed after max retries.")
