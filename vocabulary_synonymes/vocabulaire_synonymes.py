#Imports

import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer

#Stops words
with open('stopwords-fr.json') as f:
    text_file = f.read()
    StopWord = json.loads(text_file)

#synonymes dictionary
with open("./thesaurus-v2.3/dic_synonymes.json") as f:
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

#web API
from flask import Flask, escape, request, jsonify

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def rootvue():
    response = app.send_static_file('index_vue.html')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/syno', methods=['POST'])
def hello():
    text = request.get_json()
    mot_vers_synonymes = get_vocabulary_synonymes(text)
    return jsonify(mot_vers_synonymes)

if __name__ == '__main__':
    app.run(debug=False)