import os
from jogoteca import app

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
