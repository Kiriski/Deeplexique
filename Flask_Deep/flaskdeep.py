from flask import Flask, render_template, url_for
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

@app.route('/stt')
def azure_ecriture():
    return render_template('azure_sample.html', title='Ecriture Assistée')


if __name__=="__main__":
    app.run(debug=True)