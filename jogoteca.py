from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'seguro'

# CONFIG BANCO
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://root:root@localhost/jogoteca'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELS
class Jogos(db.Model):
    __tablename__ = 'jogos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Jogo {self.nome}>'


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    nickname = db.Column(db.String(8), primary_key=True, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# ROTAS
@app.route("/")
def index():
    lista = Jogos.query.order_by(Jogos.id).all()
    return render_template("lista.html", titulo="Jogos", jogos=lista)


@app.route("/novo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template("novo.html", titulo="Novo Jogo")


@app.route("/criar", methods=["POST"])
def criar():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(jogo)
    db.session.commit()

    flash('Jogo cadastrado com sucesso!')
    return redirect(url_for('index'))


@app.route("/login")
def login():
    proxima = request.args.get('proxima') or url_for('index')
    return render_template("login.html", proxima=proxima)



@app.route("/autenticar", methods=["POST"])
def autenticar():
    usuario = Usuarios.query.filter_by(
        nickname=request.form['usuario']
    ).first()

    if usuario and request.form['senha'] == usuario.senha:
        session['usuario_logado'] = usuario.nickname
        flash(f'{usuario.nickname} logado com sucesso!')

        proxima_pagina = request.form.get('proxima')

        if not proxima_pagina or proxima_pagina == 'None':
            proxima_pagina = url_for('index')

        return redirect(proxima_pagina)
    else:
        flash('Erro no login!')
        return redirect(url_for('login'))



@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash("Usuário foi deslogado!")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
