import tkinter as tk
from tkinter import filedialog, messagebox
import os
import whisper
import re  # Import the regular expression library

VALID_MODELS = ["base", "medium", "tiny", "large-v2"]
DEFAULT_MODEL = "base"
SPEAKER_KEYWORDS = ["hello", "speaker", "moderator"]  # Reduced keywords for combined approach
PAUSE_THRESHOLD = 2  # seconds - adjust as needed


def get_model_name():
    return model.get() if model.get() in VALID_MODELS else DEFAULT_MODEL


def load_whisper_model(model_name):
    try:
        model = whisper.load_model(model_name)
        return model
    except Exception as e:
        messagebox.showerror("Error", f"Error loading model: {e}")
        return None


def transcribe_audio(model, audio_file):
    try:
        result = model.transcribe(audio_file)
        return result
    except Exception as e:
        messagebox.showerror("Error", f"Error transcribing audio: {e}")
        return None


def format_transcription_output_combined(transcription_result):
    formatted_text = ""
    speaker_number = 1
    last_speaker = None
    last_timestamp = 0

    for segment in transcription_result["segments"]:
        text = segment["text"].lower()
        start_time = segment["start"]

        potential_new_speaker = False

        # Check for pause
        if start_time - last_timestamp > PAUSE_THRESHOLD:
            potential_new_speaker = True

        # Confirm with keywords if there's a pause
        if potential_new_speaker:
            for keyword in SPEAKER_KEYWORDS:
                if re.search(r"^\s*" + re.escape(keyword) + r"\b", text):
                    new_speaker = f"Speaker {speaker_number}"
                    if last_speaker != new_speaker:
                        formatted_text += f"\n{new_speaker}: "
                        speaker_number += 1
                        last_speaker = new_speaker
                    break  # Stop checking keywords after finding one
            else:
                # Pause but no keyword, might be same speaker continuing
                if last_speaker is None:
                    formatted_text += "\nModerator: "
                    last_speaker = "Moderator"
                elif last_speaker == "Moderator":
                    formatted_text += "\nModerator: "
                else:
                    formatted_text += f"\n{last_speaker}: "

        # Add the segment text.
        formatted_text += segment["text"] + " "
        last_timestamp = segment["end"]

    return formatted_text


def save_transcription_to_file(text_to_save, audio_file_path, model_name):
    base_name = os.path.splitext(audio_file_path)[0]
    output_file = f"{base_name}_{model_name}.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text_to_save)
    except UnicodeEncodeError:
        print(f"Warning: UnicodeEncodeError encountered. Trying 'cp1252' encoding.")
        with open(output_file, "w", encoding="cp1252") as f:
            f.write(text_to_save.encode('cp1252', 'replace').decode('cp1252'))


def transcribe():
    model_name = get_model_name()
    if not model_name:
        return

    model = load_whisper_model(model_name)
    if not model:
        return

    audio_file_path = filedialog.askopenfilename(title="Select an audio file",
                                                 filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
    if not audio_file_path:
        return

    transcription_result = transcribe_audio(model, audio_file_path)
    if not transcription_result:
        return

    formatted_text = format_transcription_output_combined(transcription_result)
    text.delete('1.0', tk.END)  # Clear the Text widget
    text.insert(tk.INSERT, formatted_text)

    save_transcription_to_file(formatted_text, audio_file_path, model_name)
    messagebox.showinfo("Success",
                        f"Transcription saved to: {os.path.splitext(audio_file_path)[0]}_{model_name}.txt")


root = tk.Tk()
root.title("Whisper Transcriber")

model = tk.StringVar(value=DEFAULT_MODEL)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Select a model:")
label.grid(row=0, column=0, sticky='w')

model_menu = tk.OptionMenu(frame, model, *VALID_MODELS)
model_menu.grid(row=0, column=1, sticky='ew')

transcribe_button = tk.Button(frame, text="Transcribe", command=transcribe)
transcribe_button.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky='ew')

text = tk.Text(root, width=80, height=25)
text.pack(padx=10, pady=10)

root.mainloop()
