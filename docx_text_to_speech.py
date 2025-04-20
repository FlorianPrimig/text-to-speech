# script to transform docx files into audio; it is optimized for acamdemic texts with sources in brackets, references and footnotes
from pathlib import Path
import re
import subprocess

# Ensure dependencies are installed
subprocess.run(['pip3', 'install', '-U', 'openai'])
subprocess.run(['pip3', 'install', 'python-docx'])

# Import OpenAI and credentials
try:
    import credentials
except ImportError:
    raise ImportError("credentials.py not found. Make sure it contains OPENAI_API_KEY.")
from openai import OpenAI
import docx
print(docx.__file__)



# OpenAI API client
client = OpenAI(api_key=credentials.OPENAI_API_KEY) #have an "credetials.py" file in the same directory with only one line: OPENAI_API_KEY = 'yourKey'

# --- Text cleaning functions ---

def remove_text_in_brackets(text):
    return re.sub(r'\(.*?\)', '', text)

def remove_references_section(text):
    pattern = r'(?im)^\s*(references|literature)\s*$.*'
    return re.sub(pattern, '', text, flags=re.DOTALL)

def remove_footnotes(text):
    text = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+', '', text)  # Superscripts
    text = re.sub(r'(?m)^\s*\d{1,2}\.\s+.*$', '', text)  # Numbered footnotes
    return text

# --- Read .docx ---

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = [p.text for p in doc.paragraphs]
    return '\n'.join(full_text)

# --- Audio generation ---

def generate_audio_from_text(input_text, output_file):
    input_text = remove_text_in_brackets(input_text)
    input_text = remove_references_section(input_text)
    input_text = remove_footnotes(input_text)

    fname = f'{output_file}.mp3'
    max_length = 4000  # Max chunk size

    chunks = [input_text[i:i + max_length] for i in range(0, len(input_text), max_length)]

    with open(fname, "wb") as audio_file:
        for chunk in chunks:
            response = client.audio.speech.create(
                model="tts-1", #gpt-4o-mini-tts has good price/performance but tts-1 is slightly cheaper and works just as fine for most cases
                voice="echo",
                input=chunk,
                speed=1.0
            )
            audio_file.write(response.content)

# --- Run script ---

if __name__ == "__main__":
    input_file = "yourfile.docx"
    input_text = read_docx(input_file)
    generate_audio_from_text(input_text, "your preferred file name audio")
