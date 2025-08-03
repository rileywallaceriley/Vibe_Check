def parse_prompt(prompt):
    prompt = prompt.lower().strip()
    roles = {
        "songs featuring": "featured_artist",
        "songs produced by": "producer",
        "songs written by": "writer",
        "songs by": "primary_artist"
    }

    for phrase, role in roles.items():
        if phrase in prompt:
            name = prompt.replace(phrase, "").strip()
            return {"name": name.title(), "role": role}

    return {"name": prompt.title(), "role": "primary_artist"}