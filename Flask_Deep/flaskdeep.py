## import for vocabulary
import pandas as pd
import numpy as np
import json
from TextToSpeech import TextToSpeech
from sklearn.feature_extraction.text import CountVectorizer
## end import

from flask import Flask, render_template, url_for, escape, request, jsonify, Response
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/dyslexie')
def dyslexie():
    return render_template('dyslexie.html', title='Dyslexie')

@app.route('/vocabulary')
def vocabulary():
    return render_template('vocabulary.html', title='Vocabulary')

@app.route('/write_assist')
def write_assist():
    return render_template('write_assist.html', title='Ecriture Assistée')

@app.route('/read_assist')
def read_assist():
    return render_template('read_assist.html', title='Lecture Assistée')

@app.route('/stt')
def synth():
    return render_template('synth.html', title='Synthétiseur')

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    print("here")
    data = request.get_json()
    text_input = data['text']
    tts = TextToSpeech(text_input)
    tts.get_token()
    audio_response = tts.save_audio()
    return audio_response

    


## API vocabulaire

#Stops words
with open('./data/stopwords-fr.json', encoding="utf-8") as f:
    text_file = f.read()
    StopWord = json.loads(text_file)

#synonymes dictionary
with open("./data/dic_synonymes.json", encoding="utf-8") as f:
    data = f.read()
    dic_synonymes = json.loads(data)

#get vocabulary and synonymes
def get_vocabulary_synonymes(text):
    #si le texte est vide, renvoie un dic vide
    if text == "":
        return {}
    #spliter le texte en phrases
    text = text.replace("\n", "").split(".")
    
    #compter les mots par occurence et enlever les stopwords
    vectorizer = CountVectorizer(stop_words=StopWord)
    X = vectorizer.fit_transform(text)

    frequence_mots = X.toarray()
    
    compte = np.sum(frequence_mots, axis=0)
    
    compte = list(compte)
    mots = vectorizer.get_feature_names()

    mots_occurence = pd.DataFrame(data={'compte' : compte, 'mots': mots})
    mots_occurence = mots_occurence.sort_values(by = 'compte', ascending=False)
    mots_occurence.iloc[:30]
    
    return {mot:dic_synonymes[mot] for mot in mots if mot in dic_synonymes}


@app.route('/api/syno', methods=['POST'])
def hello():
    text = request.get_json()
    mot_vers_synonymes = get_vocabulary_synonymes(text)
    return jsonify(mot_vers_synonymes)


if __name__=="__main__":
    app.run(debug=True)