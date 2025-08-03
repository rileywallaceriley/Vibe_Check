import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_user_prompt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you're using GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant that interprets music-related playlist prompts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=200
    )
    return response['choices'][0]['message']['content'].strip()
