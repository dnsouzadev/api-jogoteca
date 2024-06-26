from jogoteca import db

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Name {self.nome}>'

class Usuarios(db.Model):
    nome = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(8), primary_key=True, unique=True)
    senha = db.Column(db.String(100), nullable=False)
