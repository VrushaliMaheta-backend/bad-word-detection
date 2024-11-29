import os
import spacy
import pickle
import tempfile
from io import BytesIO
from fuzzywuzzy import fuzz
from pydub import AudioSegment
import speech_recognition as sr
from fastapi import HTTPException
from better_profanity import profanity
from nltk.stem.snowball import SnowballStemmer

file_name = os.getcwd() + "/bad_word_classifier.pkl"

def text_cleaning(text_data):
    word_list = []
    for words in text_data:
        if words.is_stop or words.is_punct:
            pass
        else:
            word_list.append(words.text)
    return word_list

def check_similarity(text_data,badwords,threshold=85):
    with open(os.getcwd() + "/badwords.txt","r") as f:
        badword = [line.strip() for line in f.readlines()]

    badwords += badword
    badword_list = []
    for words in text_data:
        for badword in badwords:
            stem_word = SnowballStemmer(language="english").stem(words)
            similarity = fuzz.ratio(badword,stem_word)
            if similarity >= threshold:
                badword_list.append(words)
                break
    return list(set(badword_list))

def bad_word_prediction(text):
    # get list of badwords from a profanity.CENSOR_WORDSET
    badwords = []
    for words in profanity.CENSOR_WORDSET:
        badwords.append(str(words))

    # read a file
    with open(file_name,"rb") as file:
        model = pickle.load(file)
    
    # load spacy
    nlp = spacy.load("en_core_web_sm")
    data = nlp(text)

    # text cleaning process and check similarity with badwords
    cleaned_res = text_cleaning(data)
    res = check_similarity(cleaned_res,badwords)

    prediction = model.predict([text])

    if prediction[0] == 1:
        return {
            "text":text,
            "it_is_curse_phrase":"YES",
            "bad_words":res
        }
    else:
        return {
            "text":text,
            "it_is_curse_phrase":"NO"
        }

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