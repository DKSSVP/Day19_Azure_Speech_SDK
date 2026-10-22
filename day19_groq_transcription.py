import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    Groq,
)

# Load credentials from the project's .env file.
PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "whisper-large-v3-turbo"
AUDIO_FILE = PROJECT_DIR / "test_audio.wav"


def main():
    print("Day 19: Groq Speech Transcription")
    print("-" * 40)

    if not API_KEY:
        print("ERROR: GROQ_API_KEY was not found in .env.")
        sys.exit(1)

    if not AUDIO_FILE.exists():
        print(f"ERROR: Audio file not found: {AUDIO_FILE}")
        print("Create test_audio.wav in the project folder first.")
        sys.exit(1)

    if AUDIO_FILE.stat().st_size == 0:
        print("ERROR: The audio file is empty.")
        sys.exit(1)

    # Groq's transcription upload limit is 25 MB.
    if AUDIO_FILE.stat().st_size > 25 * 1024 * 1024:
        print("ERROR: Audio file exceeds the 25 MB upload limit.")
        sys.exit(1)

    print(f"Audio file: {AUDIO_FILE.name}")
    print(f"Audio size: {AUDIO_FILE.stat().st_size:,} bytes")
    print(f"Model: {MODEL_NAME}")
    print("\nSending audio to Groq...")

    try:
        client = Groq(api_key=API_KEY)

        with AUDIO_FILE.open("rb") as audio:
            result = client.audio.transcriptions.create(
                file=(
                    AUDIO_FILE.name,
                    audio,
                    "audio/wav",
                ),
                model=MODEL_NAME,
                response_format="json",
            )

        transcript = result.text.strip()

        if not transcript:
            print("WARNING: The API returned an empty transcript.")
            sys.exit(1)

        # Save the transcription as a text file.
        text_path = PROJECT_DIR / "day19_transcription.txt"
        text_path.write_text(transcript + "\n", encoding="utf-8")

        # Save the result and metadata as JSON.
        report = {
            "audio_file": AUDIO_FILE.name,
            "model": MODEL_NAME,
            "status": "success",
            "transcription": transcript,
        }

        json_path = PROJECT_DIR / "day19_transcription_report.json"
        json_path.write_text(
            json.dumps(report, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print("\nSUCCESS: Audio transcription completed.")
        print("\nTranscription:")
        print(transcript)
        print(f"\nText saved to: {text_path.name}")
        print(f"Report saved to: {json_path.name}")

    except AuthenticationError:
        print("ERROR: Groq authentication failed. Check GROQ_API_KEY.")
        sys.exit(1)

    except APIConnectionError:
        print("ERROR: Could not connect to Groq. Check your internet connection.")
        sys.exit(1)

    except APIStatusError as error:
        print(f"ERROR: Groq API returned HTTP {error.status_code}.")
        print("Check the API error details and your account limits.")
        sys.exit(1)

    except Exception as error:
        print(f"ERROR: {type(error).__name__}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()