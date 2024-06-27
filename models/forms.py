from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, length
from flask_wtf import FlaskForm


class FormCriarJogo(FlaskForm):
    nome = StringField('Nome do jogo', render_kw={'placeholder': 'Nome do jogo'}, description='Nome do jogo', id='nome', validators=[DataRequired(), length(min=1, max=50)])
    categoria = StringField('Categoria', render_kw={'placeholder': 'Categoria'}, description='Categoria', id='categoria', validators=[DataRequired(), length(min=1, max=40)])
    console = StringField('Console', render_kw={'placeholder': 'Console'}, description='Console', id='console', validators=[DataRequired(), length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormLogin(FlaskForm):
    nickname = StringField('Nickname', render_kw={'placeholder': 'Usuário'}, description='Usuário', id='nickname', validators=[DataRequired(), length(min=1, max=8)])
    senha = PasswordField('Senha', render_kw={'placeholder': 'Senha'}, description='Senha', id='senha', validators=[DataRequired(), length(min=1, max=100)])
    login = SubmitField('Entrar')
