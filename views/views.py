from flask import flash, redirect, render_template, request, url_for, session
from models.models import Jogos, Usuarios
from jogoteca import app, db

@app.route('/')
def index():
    jogos = Jogos.query.order_by(Jogos.categoria).all()
    return render_template('lista.html', titulo='Jogos', jogos=jogos)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash(f'O jogo {jogo.nome} já está cadastrado!')
        return redirect(url_for('novo'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()
    flash(f'O jogo {novo_jogo.nome} foi cadastrado com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html', titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('login'))
    if usuario.senha != request.form['senha']:
        flash('Senha incorreta!')
        return redirect(url_for('login'))
    session['usuario_logado'] = usuario.nickname
    flash(f'{usuario.nome} logou com sucesso!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))
