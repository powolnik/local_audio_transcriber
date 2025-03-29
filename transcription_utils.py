from typing import Optional, Dict, Any
import whisper
import os
import re

def load_whisper_model(model_name: str) -> Optional[whisper.Whisper]:
    """Loads the Whisper model.

    Args:
        model_name: The name of the Whisper model to load.

    Returns:
        The loaded Whisper model, or None if the model could not be loaded.
    """
    try:
        model = whisper.load_model(model_name)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def transcribe_audio(model: whisper.Whisper, audio_file: str) -> Optional[Dict[str, Any]]:
    """Transcribes the audio file using the Whisper model.

    Args:
        model: The loaded Whisper model.
        audio_file: The path to the audio file.

    Returns:
        A dictionary containing the transcription result, or None if the transcription failed.
    """
    try:
        result = model.transcribe(audio_file)
        return result
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def format_transcription_output_combined(transcription_result: Dict[str, Any]) -> str:
    """Formats the transcription output into a combined string.

    Args:
        transcription_result: The dictionary containing the transcription result.

    Returns:
        The formatted transcription string.
    """
    segments = transcripion_result["segments"]
    text = ""
    for segment in segments:
        text += segment["text"] + " "
    return text


def save_transcription_to_file(text_to_save: str, audio_file_path: str, model_name: str) -> None:
    """Saves the transcription text to a file.

    Args:
        text_to_save: The text to save.
        audio_file_path: The path to the audio file.
        model_name: The name of the Whisper model used.
    """
    base_name = os.path.splitext(audio_file_path)[0]
    output_file = f"{base_name}_{model_name}.txt"
    with open(output_file, "w") as f:
        f.write(text_to_save)