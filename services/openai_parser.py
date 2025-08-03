import os
import time
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_user_prompt(prompt, retries=3):
    for attempt in range(retries):
        try:
            print(f"[DEBUG] Sending prompt to OpenAI:\n{prompt}\n")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're a helpful assistant that understands user music intent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            print(f"[ERROR] OpenAI API error: {e}")
            if attempt < retries - 1:
                time.sleep(1.5)  # wait before retry
            else:
                return "Sorry, something went wrong on the server. Please try again later."