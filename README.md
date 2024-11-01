# text-to-speech
Create audio files from .txt.

Create audi files from txt files (UTF-8) using OpenAI API. Optimized for academic texts as it does a little tiny bit of text pre-processing (skipping references etc). You can get more information on available OpenAI voiceover voices here: https://platform.openai.com/docs/guides/text-to-speech You need an OpenAI API key: https://platform.openai.com/docs/overview.
For now, the script only allows for .txt file input in UTF-8. So if you have a .docx file, first save it as .txt in UTF-8 encoding. And obviously it is not good practice to store your API key in the script. You could, but it is better that you use the credentials file for that.

Use case: I mostly transform papers I write into audio to listen to them for proofreading. I find it easier to detect errors and logical breaches in my argumentation by listening to what I wrote instead of trying to re-read the same paragraphs for the 10000st time.
