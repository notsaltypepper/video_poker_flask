from flask import Flask, render_template, url_for, request, session, redirect
from label import *
from module_tirage import *
from module_gain import *

deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']

app = Flask(__name__)
app.secret_key = "key"

@app.route('/')
def homepage():
    return render_template('start.html')

@app.route('/', methods=['POST'])
def check_age():
    user_age = int(request.form['age'])
    session['error-form'] = False
    if user_age < 18:
        session['error-form'] = str_TOO_YOUNGER
        return render_template('start.html')
    else:
        session['wallet'] = int(request.form['wallet'])
        return redirect(url_for('board'))

@app.route('/board')
def board():
    return render_template('board.html')


@app.route('/board', methods=[('POST')])
def board_t1():
    session['bet'] = int(request.form['bet'])
    session['error-form-bet'] = False
    if session['bet'] > session['wallet']:
        session['error-form-bet'] = str_BET_HIGHER
        return render_template('board.html')
    else:
        session['tirage1'], session['deck1'] = premier_tirage(deck)
        session['wallet'] -= session['bet']
        return redirect(url_for('round1'))

@app.route('/round1')
def round1():
    return render_template('tirage1.html')

def choix_cartes(tirage):
    jeu = session['tirage1']
    for i in reversed(tirage):
        print(str(tirage.index(i)))
        if str(tirage.index(i)) in request.form:
            jeu.remove(i)
    return jeu

@app.route('/round1', methods=[('POST')])
def tirage2():
    jeu = choix_cartes(session['tirage1'])
    session['tirage2'] = deuxieme_tirage(jeu, session['deck1'])
    return redirect(url_for('round2'))

@app.route('/round2')
def round2():
    session['gain'], session['resultat'] = gain(session['tirage2'],session['bet'])
    session['wallet'] += session['gain']
    return render_template('tirage2.html')


if __name__ == '__main__':
    app.run(debug=True)