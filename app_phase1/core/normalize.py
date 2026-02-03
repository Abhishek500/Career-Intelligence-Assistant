SKILL_ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "tf": "tensorflow"
}


def normalize_skill_name(name: str) -> str:
    name = name.lower().strip()
    return SKILL_ALIASES.get(name, name)
