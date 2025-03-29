import whisper
import os
import re # Import the regular expression library

VALID_MODELS = ["base", "medium", "tiny", "large-v2"]
DEFAULT_MODEL = "base"
SPEAKER_KEYWORDS = ["hello", "speaker", "moderator"] # Reduced keywords for combined approach
PAUSE_THRESHOLD = 2 # seconds - adjust as needed

def get_model_name_from_user():
   """Prompts the user for a model name and returns it."""
   print(f"Select a model ({', '.join(VALID_MODELS)}) or press Enter for '{DEFAULT_MODEL}':")
   name = input("... : ").strip()
   return name if name in VALID_MODELS else DEFAULT_MODEL

def get_audio_file_path_from_user():
   """Prompts the user for the audio file path and returns the absolute path."""
   filename = input("Enter the path to the .mp3 file (relative to script location): ").strip()
   filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
   return os.path.abspath(filepath)

def load_whisper_model(model_name):
   """Loads the whisper model and handles potential errors."""
   try:
       model = whisper.load_model(model_name)
       return model
   except Exception as e:
       print(f"Error loading model: {e}")
       return None

def transcribe_audio(model, audio_file):
   """Transcribes the audio file and handles potential errors."""
   try:
       result = model.transcribe(audio_file)
       return result
   except Exception as e:
       print(f"Error transcribing audio: {e}")
       return None

def format_transcription_output_combined(transcription_result):
 """
 Formats the transcription with speaker identification using a combination
 of pause and keyword detection. Indicates speaker only once at the beginning.
 """
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
         break # Stop checking keywords after finding one
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
# declare hello world function AI!
def save_transcription_to_file(text_to_save, audio_file_path, model_name):
   """Saves the transcription text to a file, handling potential encoding issues."""
   base_name = os.path.splitext(audio_file_path)[0]
   output_file = f"{base_name}_{model_name}.txt"
   try:
       with open(output_file, "w", encoding="utf-8") as f:
           f.write(text_to_save)
   except UnicodeEncodeError:
       print(f"Warning: UnicodeEncodeError encountered. Trying 'cp1252' encoding.")
       with open(output_file, "w", encoding="cp1252") as f:
           f.write(text_to_save.encode('cp1252', 'replace').decode('cp1252'))

if __name__ == "__main__":
   model_name = get_model_name_from_user()
   if not model_name:
       exit()

   model = load_whisper_model(model_name)
   if not model:
       exit()

   audio_file_path = get_audio_file_path_from_user()
   if not audio_file_path:
       exit()

   transcription_result = transcribe_audio(model, audio_file_path)
   if not transcription_result:
       exit()

   formatted_text = format_transcription_output_combined(transcription_result)
   print(formatted_text)

   save_transcription_to_file(formatted_text, audio_file_path, model_name)
   print(f"Transcription saved to: {os.path.splitext(audio_file_path)[0]}_{model_name}.txt")
