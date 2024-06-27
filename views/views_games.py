from flask import flash, redirect, render_template, request, send_from_directory, url_for, session
from models.Jogos import Jogos
from jogoteca import app, db
import os
from helpers import recupera_imagem, deleta_imagem
from models.forms import FormCriarJogo
import time

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

    form = FormCriarJogo()

    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormCriarJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash(f'O jogo {jogo.nome} já está cadastrado!')
        return redirect(url_for('novo'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    os.makedirs(f'uploads/{nome}', exist_ok=True)
    arquivo = request.files['arquivo']
    timestamp = time.time()
    upload_path = os.path.join(app.config['UPLOAD_PATH'], novo_jogo.nome, f'capa{str(novo_jogo.id)}--{timestamp}.jpg')
    arquivo.save(upload_path)

    flash(f'O jogo {novo_jogo.nome} foi cadastrado com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).first()

    form = FormCriarJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(jogo.id)
    print(capa_jogo)

    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormCriarJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.commit()

        os.makedirs(f'uploads/{jogo.nome}', exist_ok=True)

        arquivo = request.files['arquivo']
        timestamp = time.time()
        deleta_imagem(jogo.id)
        upload_path = os.path.join(app.config['UPLOAD_PATH'], jogo.nome, f'capa{str(jogo.id)}--{timestamp}.jpg')
        arquivo.save(upload_path)

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
    u = nome_arquivo.split('$')
    if 'capa.jpg' not in nome_arquivo:
        diretorio = os.path.join(app.config['UPLOAD_PATH'], os.path.dirname(u[0]))
        diretorio = diretorio + '/' + u[0]
        arquivo = os.path.basename(u[1])

        if not os.path.exists(os.path.join(diretorio, arquivo)):
            return send_from_directory('uploads', 'capa.jpg')

        return send_from_directory(diretorio, arquivo)
    return send_from_directory('uploads', 'capa.jpg')

