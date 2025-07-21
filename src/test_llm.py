from llm_interface import generate_from_template

variables = {
    "book_title": "Smart Choices",
    "target_age": "8–10",
    "life_skill_theme": "Decision making",
    "setting": "a school in Bangalore",
    "main_characters": "a curious boy, his best friend, and a funny principal",
    "chapter_count": "3"
}

output = generate_from_template(
    template_name="book_overview_prompt",
    variables=variables,
    model="gpt-3.5-turbo",          # Lowest-cost chat model
)

print("\n🧪 GPT OUTPUT:\n")
print(output)
