from flask import flash, redirect, render_template, request, send_from_directory, url_for, session
from models.models import Jogos, Usuarios
from jogoteca import app, db
import os

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    jogos = Jogos.query.order_by(Jogos.categoria).all()
    return render_template('lista.html', titulo='Jogos', jogos=jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

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

    os.makedirs(f'uploads/{nome}', exist_ok=True)

    arquivo = request.files['arquivo']
    upload_path = os.path.join(app.config['UPLOAD_PATH'], nome, f'{str(novo_jogo.id)}.jpg')
    arquivo.save(upload_path)

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

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).first()

    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    id = request.form['id']
    jogo = Jogos.query.filter_by(id=id).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    db.session.commit()
    flash(f'O jogo {jogo.nome} foi atualizado com sucesso!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).first()
    db.session.delete(jogo)
    db.session.commit()
    flash(f'O jogo {jogo.nome} foi deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
