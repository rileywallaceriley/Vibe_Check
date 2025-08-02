def extract_artist(prompt):
    if "songs featuring" in prompt:
        return prompt.split("songs featuring")[-1].strip()
    return prompt.strip()
