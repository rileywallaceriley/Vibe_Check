import openai
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_user_prompt(prompt):
    system_message = {
        "role": "system",
        "content": (
            "You are a music data parser. Based on the user prompt, extract and return:\n"
            "- artist_name\n"
            "- decade (optional)\n"
            "- intent_type (one of: songs_by, songs_featuring, songs_produced_by, songs_written_by)\n\n"
            "Respond in valid JSON. No extra text. Example:\n"
            "{\n"
            "  \"artist_name\": \"Black Rob\",\n"
            "  \"decade\": \"2000s\",\n"
            "  \"intent_type\": \"songs_featuring\"\n"
            "}"
        ),
    }

    user_message = {"role": "user", "content": prompt}

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[system_message, user_message],
        temperature=0,
        max_tokens=200,
        response_format="json",
    )

    return response.choices[0].message.content
