from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    jogos = ['Super Mario', 'Zelda', 'Pokemon', 'Donkey Kong', 'Mortal Kombat', 'Street Fighter', 'Final Fantasy', 'Castlevania', 'Metroid', 'Sonic']
    return render_template('lista.html', titulo='Jogos', jogos=jogos)


app.run(debug=True)
