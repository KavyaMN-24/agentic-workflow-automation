from app.core.config import GROQ_MODEL, validate_config
from app.core.llm_client import get_groq_client


def main():
    validate_config()
    client = get_groq_client()

    print("Groq configuration loaded successfully.")
    print(f"Model: {GROQ_MODEL}")
    print(f"Client type: {type(client).__name__}")


if __name__ == "__main__":
    main()