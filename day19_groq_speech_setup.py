import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from groq import APIConnectionError, APIStatusError, AuthenticationError


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
MODEL_NAME = "whisper-large-v3-turbo"


def load_configuration():
    """Load and validate the Groq API key."""
    load_dotenv(ENV_FILE)

    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check the .env file "
            "inside the Day 19 project folder."
        )

    return api_key


def test_groq_connection(api_key):
    """Verify that the Groq API accepts our credentials."""
    client = Groq(api_key=api_key, timeout=20.0)

    print("Testing connection to Groq...")
    model_list = client.models.list()

    available_models = {model.id for model in model_list.data}

    print("\nSUCCESS: Groq API connection is working.")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Groq SDK version: {get_sdk_version()}")
    print(f"Whisper model configured: {MODEL_NAME}")

    if MODEL_NAME in available_models:
        print("Whisper model listed by API: Yes")
    else:
        print(
            "Whisper model listed by API: Not confirmed "
            "in the model list. Check model access before transcription."
        )

    return 0


def get_sdk_version():
    """Return the installed Groq SDK version."""
    from importlib.metadata import version

    return version("groq")


def main():
    try:
        api_key = load_configuration()
        return test_groq_connection(api_key)

    except ValueError as exc:
        print(f"Configuration error: {exc}")
        return 1

    except AuthenticationError:
        print("Authentication failed. Check whether the Groq key is valid.")
        return 1

    except APIConnectionError:
        print("Could not connect to Groq. Check your internet connection.")
        return 1

    except APIStatusError as exc:
        print(f"Groq API returned HTTP status {exc.status_code}.")
        print("Check your API access, quota, and service status.")
        return 1

    except Exception as exc:
        print(f"Unexpected error: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())