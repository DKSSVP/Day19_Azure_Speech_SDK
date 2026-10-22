# Day 19 – Speech Transcription Setup and Configuration

## 1. Objective

Configure and test a cloud-based speech transcription workflow using the Groq API and the Whisper speech recognition model.

**Note:** The original task specifies Azure Speech SDK. This implementation uses Groq, following the team's confirmed API approach.

## 2. Technologies Used

- Python
- Groq API
- Groq Python SDK
- Whisper model: `whisper-large-v3-turbo`
- python-dotenv
- Windows PowerShell
- Git and GitHub

## 3. Environment Setup

- Created and used a Python virtual environment.
- Installed the required Python packages.
- Stored the Groq API key in the `.env` file.
- Verified that the API key was configured without displaying the secret.
- Tested the Groq API connection successfully.

## 4. Implementation

Created the following Python files:

- `day19_groq_speech_setup.py` – validates the Groq API connection and checks model availability.
- `day19_groq_transcription.py` – sends the test audio file to the Groq transcription API and saves the result.

## 5. Test Procedure

1. Generated a short WAV audio file using Windows text-to-speech.
2. Verified that the audio file existed and was not empty.
3. Sent the audio file to Groq using the `whisper-large-v3-turbo` model.
4. Retrieved the transcription response.
5. Saved the recognized text and JSON report.

## 6. Expected Output Files

- `test_audio.wav` – generated test audio.
- `day19_transcription.txt` – recognized speech.
- `day19_transcription_report.json` – transcription result and metadata.

## 7. Connection Test Results

The Groq API connection test completed successfully.

- API authentication: Successful
- Model availability check: Successful
- Python environment: Configured
- Audio transcription: Record the result after running the transcription script.

## 8. Security

- API credentials are stored in `.env`.
- The `.env` file must not be committed to GitHub.
- The `.venv/` directory must not be committed.
- The JSON report must be reviewed to ensure it contains no secrets.

## 9. Conclusion

The Groq API connection and model availability were verified. The speech transcription workflow is prepared for testing with a generated WAV audio file. The transcription result should be confirmed before marking the entire workflow as complete.