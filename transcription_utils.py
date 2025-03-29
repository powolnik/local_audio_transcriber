import whisper
import os
from typing import Optional, Dict, Any

def load_whisper_model(model_name: str) -> Optional[whisper.Whisper]:
    """
    Loads a Whisper model.

    Args:
        model_name: The name of the Whisper model to load (e.g., "base", "medium").

    Returns:
        The loaded Whisper model, or None if loading fails.
    """
    try:
        model = whisper.load_model(model_name)
        return model
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return None

def transcribe_audio(model: whisper.Whisper, audio_file: str) -> Optional[Dict[str, Any]]:
    """
    Transcribes audio using a Whisper model.

    Args:
        model: The Whisper model to use.
        audio_file: The path to the audio file to transcribe.

    Returns:
        A dictionary containing the transcription results, or None if transcription fails.
    """
    try:
        result = model.transcribe(audio_file)
        return result
    except Exception as e:
        print(f"Error transcribing audio {audio_file}: {e}")
        return None

def format_transcription_output_combined(transcription_result: Dict[str, Any]) -> str:
    """
    Formats the combined transcription output.

    Args:
        transcription_result: The raw transcription result dictionary.

    Returns:
        A formatted string containing the transcription.
    """
    # Placeholder for formatting logic.  Replace with actual formatting.
    if transcription_result and "text" in transcription_result:
        return transcription_result["text"]
    else:
        return ""

def save_transcription_to_file(text_to_save: str, audio_file_path: str, model_name: str) -> None:
    """
    Saves the transcription to a file.

    Args:
        text_to_save: The transcription text to save.
        audio_file_path: The path to the original audio file.
        model_name: The name of the Whisper model used.
    """
    base_name = os.path.splitext(audio_file_path)[0]
    output_file = f"{base_name}_{model_name}.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text_to_save)
        print(f"Transcription saved to {output_file}")
    except Exception as e:
        print(f"Error saving transcription to file: {e}")
