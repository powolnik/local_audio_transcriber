import whisper
import os
import glob

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
try:
   model = whisper.load_model(m_name)
except Exception as e:
   print(f"Error loading model: {e}")
   exit()

audio_file = handle_input("filename")
print(audio_file)
# try:
result = model.transcribe(audio_file)
# except Exception as e:
#    print(f"Error transcribing audio: {e}")
#    exit()

# text = result["text"]

# Speaker Identification and Prefixing Logic
# speaker_number = 1
# last_announced_speaker :int
# last_timestamp = -1
# pause_threshold = 2  # seconds

def x():
   i = 0
   txt = ""
   for segment in result["segments"]:
      if txt == "": txt+="all segments: \n\n"
      i += 1
      # print("Loop: "+str(i)) 
      # print(""+segment["text"])
      # if 'timestamp' in segment:
      # current_timestamp = segment['timestamp']
      # if true:
         # speaker_number += 1
      #   prefix = f"Speaker {speaker_number}: "
      # prefix = ""+speaker_number

      txt += "\nSegment: " + str(i) + segment['text'] + "\n\n\n"
   i = 0
   return txt 
string = x()

# Optional: Add line breaks after each segment for readability
# if segment != result["segments"][-1]:
#    string += "\n"

print(string)

base_name = os.path.splitext(audio_file)[0]
output_file = f"{base_name}_{m_name}.txt"

try:
   with open(output_file, "w", encoding="utf-8") as f:
      f.write(string)
except UnicodeEncodeError:
   with open(output_file, "w", encoding="cp1252") as f:
      f.write(string.encode('cp1252', 'replace').decode('cp1252'))