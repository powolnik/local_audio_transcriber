import whisper
import os
# import glob #Not used

from transcription_utils import load_whisper_model, transcribe_audio, format_transcription_output_combined, save_transcription_to_file

m_name :str = "" #= "amsterdam.mp3"
valid_inputs = ["mname", "filename"]
valid_models = ["base", "medium", "tiny", "large-v2"]

def handle_input(input_to_handle: str) -> str:
 if (input_to_handle == "mname"):
   print(f"INPUT one of {', '.join(valid_models)}\n or press enter to run 'base'\n")
   name = input("... : ")
   return name if name in valid_models else "base"
 elif (input_to_handle == "filename"):
   file_name = input("Enter the path to the .mp3 file (relative to script location): ")
   file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),file_name)
   return os.path.abspath(file_path)
 else:
   print("unknown input name")
   return "P:/AI/transcriber/amsterdam.mp3"

m_name = handle_input("mname")
print(m_name)

model = load_whisper_model(m_name)
if model is None:
  exit()

audio_file = handle_input("filename")
print(audio_file)

result = transcribe_audio(model, audio_file)

if result is None:
  exit()

text = format_transcription_output_combined(result)

# Optional: Add line breaks after each segment for readability
# if segment != result["segments"][-1]:
#   string += "\n"

print(text)

save_transcription_to_file(text, audio_file, m_name)
