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


class Usuario:
    def __init__(self, nickname, nome, senha):
        self.nickname = nickname
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('admin', 'admin', '1234')

usuarios = { usuario1.nickname: usuario1 }


@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    return render_template('lista.html', titulo='Jogos', jogos=jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
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
    if request.form['usuario'] in usuarios:
        if request.form['senha'] == usuarios[request.form['usuario']].senha:
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
