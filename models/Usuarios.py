from jogoteca import db

class Usuarios(db.Model):
    nome = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(8), primary_key=True, unique=True)
    senha = db.Column(db.String(100), nullable=False)
