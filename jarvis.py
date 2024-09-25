# Example Python code to integrate GPT-4 with Google Sheets

import openai
import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import whisper
import sounddevice as sd
import numpy as np

# Use your own API key for GPT-4 and Google Sheets
openai_api_key = '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'
google_sheets_credentials_json = '/home/d3f4ult/ffmpeg/sector9/sector9-407818-55432b251486.json'
# together.ai 000013657471bd0af161d000c19c45289ac274592e75af4541a7c709974e0000

# Initialize OpenAI GPT-4 (simulated for this example)
openai.api_key = openai_api_key

# Initialize Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(google_sheets_credentials_json, scope)
client = gspread.authorize(creds)

# Function to capture voice input and return as text using Whisper
def capture_voice_input_whisper():
    model = whisper.load_model("base")
    sample_rate = 16000
    # Record audio from the microphone
    duration = 5  # seconds
    print("Recording...")
    #recording = sd.rec(int(duration * model.sample_rate), samplerate=model.sample_rate, channels=1, dtype='float32')
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    audio = np.array(recording).flatten()
    # Transcribe audio
    result = model.transcribe(audio)
    return result["text"]

# Example function to add a row to a Google Sheet
def add_row_to_sheet(sheet_name, row_data):
    sheet = client.open(sheet_name).sheet1
    sheet.append_row(row_data)

# Example of processing a conversation and logging it in Google Sheets
def log_conversation_in_sheet(conversation, sheet_name):
    # Process the conversation with GPT-4 (simulated for this example)
    response = openai.Completion.create(engine="davinci", prompt=conversation, max_tokens=150)
    processed_data = [conversation, response.choices[0].text.strip()]

    # Log the processed data in Google Sheets
    add_row_to_sheet(sheet_name, processed_data)

# Example usage with voice input
voice_input = capture_voice_input_whisper()
print("You said: " + voice_input)
log_conversation_in_sheet(voice_input, "JarvisDatabase")

# Example usage
# conversation = "What's the weather like today?"
# log_conversation_in_sheet(conversation, "JarvisDatabase")
# this is a test

# Note: This code is for illustration purposes. Replace the API keys and sheet details with your own.
# The interaction with GPT-4 is simulated as direct API interaction is not available in this environment.
