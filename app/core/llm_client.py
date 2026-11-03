from groq import Groq

from app.core.config import GROQ_API_KEY, validate_config


def get_groq_client() -> Groq:
    validate_config()
    return Groq(api_key=GROQ_API_KEY)