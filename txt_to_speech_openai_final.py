from pathlib import Path
import re
import subprocess
# Importing credentials from the credentials module
try:
    import credentials
except ImportError:
    raise ImportError("credentials.py not found. Make sure it's in the same directory.")

subprocess.run(['pip3', 'install', '-U', 'openai'])
from openai import OpenAI

my_api_key = credentials.OPENAI_API_KEY #put your api key in the seperate credentials file and leave them there

client = OpenAI(api_key=my_api_key)

def remove_text_in_brackets(text):
    return re.sub(r'\(.*?\)', '', text)

def generate_audio_from_text(input_text, output_file):
    input_text = remove_text_in_brackets(input_text)  # Remove text in brackets
    fname = f'{output_file}.mp3'

    # Maximum length of text per request
    max_length = 4000

    # Split the input text into chunks
    chunks = [input_text[i:i+max_length] for i in range(0, len(input_text), max_length)]

    # Generate audio for each chunk and append to the output file
    with open(fname, "wb") as audio_file:
        for chunk in chunks:
            response = client.audio.speech.create(
                model="tts-1",
                voice="echo", #there are different voices available. See here: https://platform.openai.com/docs/guides/text-to-speech
                input=chunk,
                speed=1.0
            )
            audio_file.write(response.content)

if __name__ == "__main__":
    input_file = "yourtxtfile.txt"  # Change this to your input file name
    with open(input_file, "r", encoding="utf-8") as file:
        input_text = file.read()
    generate_audio_from_text(input_text, "output") #change to the prefered name of your output file
