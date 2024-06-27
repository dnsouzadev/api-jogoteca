from flask import flash, redirect, render_template, request, url_for, session
from models.Usuarios import Usuarios
from jogoteca import app
from models.forms import FormLogin

@app.route('/login')
def login():
    form = FormLogin()
    return render_template('login.html', titulo='Login', form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormLogin(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if not usuario:
        flash('Usuário não encontrado!')
        return redirect(url_for('login'))
    if usuario.senha != form.senha.data:
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
