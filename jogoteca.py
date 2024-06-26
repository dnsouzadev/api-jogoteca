from flask import Flask, flash, redirect, render_template, request, url_for, session

app = Flask(__name__)

app.secret_key = 'alura'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
jogo4 = Jogo('GTA V', 'Ação', 'PS4')
jogos = [jogo1, jogo2, jogo3, jogo4]


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=jogos)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogos.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html', titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'admin' == request.form['usuario'] and '1234' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash('Login realizado com sucesso!')
        return redirect(url_for('index'))
    flash('Usuário ou senha inválidos!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
