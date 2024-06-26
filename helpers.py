import os
from jogoteca import app

def recupera_imagem(id):
    for root, dirs, files in os.walk(app.config['UPLOAD_PATH']):
        for nome_arquivo in files:
            if 'capa' + str(id) + '.jpg' == nome_arquivo:
                return os.path.basename(root) + ':' + nome_arquivo
    return 'capa.jpg'
