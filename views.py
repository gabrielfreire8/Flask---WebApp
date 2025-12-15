from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos, Usuarios



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

@app.route("/editar/<int:id>")
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(
            url_for('login', proxima=url_for('editar', id=id))
        )

    jogo = Jogos.query.get_or_404(id)
    return render_template("editar.html", titulo="Editando Jogo", jogo=jogo)


@app.route("/atualizar", methods=["POST"])
def atualizar():
    pass


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