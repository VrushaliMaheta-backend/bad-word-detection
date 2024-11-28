import os
import pickle
import tempfile
from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr
from fastapi import HTTPException

file_name = os.getcwd() + "/bad_word_classifier.pkl"

def bad_word_prediction(text):
    with open(file_name,"rb") as file:
        model = pickle.load(file)
    
    prediction = model.predict([text])

    if prediction[0] == 1:
        return "Phrase has bad words!!"
    else:
        return "No bad words detect!!It's clean text"

def convert_mp3_to_wav(mp3_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    wav_file = BytesIO()
    audio.export(wav_file, format="wav")
    wav_file.seek(0)
    
    return wav_file

async def speech_to_text_bad_word_detection(file):
    if not file.filename.endswith((".wav",".mp3")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .wav or .mp3 file.")
    
    with open(file_name,"rb") as model_file:
        model = pickle.load(model_file)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        if file.filename.endswith(".mp3"):
            wav_file_path = convert_mp3_to_wav(temp_file_path)
        else:
            wav_file_path = temp_file_path

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_sphinx(audio_data)

        prediction = model.predict([text])

        if prediction[0] == 1:
            return "Audio has bad words!!"
        else:
            return "No bad words detect in Audio!!"