import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_user_prompt(prompt):
    system_prompt = (
        "You're a music discovery assistant. Given a user's natural language prompt, "
        "extract their intent as structured JSON. The JSON should include:\n"
        "- role: one of ['primary_artist', 'featured_artist', 'producer', 'writer']\n"
        "- name: the person's name\n"
        "- genre: optional (null if not specified)\n"
        "- decade: optional (null if not specified)\n"
        "- vibe: optional (null if not specified)\n"
        "- result_count: always set to 10\n\n"
        "Respond ONLY with the JSON object."
    )

    user_message = f"Prompt: {prompt}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
        max_tokens=200
    )

    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except Exception as e:
        return {"error": "Failed to parse OpenAI response", "raw": content}
