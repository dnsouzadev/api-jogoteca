import os

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length
from jogoteca import app
from flask_wtf import FlaskForm


class FormCriarJogo(FlaskForm):
    nome = StringField('Nome do jogo', render_kw={'placeholder': 'Nome do jogo'}, description='Nome do jogo', id='nome', validators=[DataRequired(), length(min=1, max=50)])
    categoria = StringField('Categoria', render_kw={'placeholder': 'Categoria'}, description='Categoria', id='categoria', validators=[DataRequired(), length(min=1, max=40)])
    console = StringField('Console', render_kw={'placeholder': 'Console'}, description='Console', id='console', validators=[DataRequired(), length(min=1, max=20)])
    salvar = SubmitField('Salvar')



def recupera_imagem(id):
    for root, dirs, files in os.walk(app.config['UPLOAD_PATH']):
        for nome_arquivo in files:
            if 'capa' + str(id) in nome_arquivo:
                return os.path.basename(root) + '$' + nome_arquivo
    return 'capa.jpg'

def deleta_imagem(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo.replace('$', '/')))
