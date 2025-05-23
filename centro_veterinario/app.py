import os
import sqlite3
from flask import Flask, render_template, request, redirect, g
from datetime import datetime

app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASEDIR, 'centro_veterinario.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exc):
    db = getattr(g, '_database', None)
    if db:
        db.close()

@app.cli.command('init-db')
def init_db():
    """Inicializa o banco de dados executando o schema.sql."""
    conn = sqlite3.connect(DB_PATH)
    with open(os.path.join(BASEDIR, 'schema.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print('Banco de dados inicializado.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO Usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha)
            )
            conn.commit()
            return redirect('/')
        except sqlite3.IntegrityError:
            return render_template('cadastro_usuario.html', error='Email já cadastrado.')
    return render_template('cadastro_usuario.html')

@app.route('/cadastro_pet', methods=['GET', 'POST'])
def cadastro_pet():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        peso = request.form['peso']
        raca = request.form['raca']
        id_usuario = request.form['id_usuario']
        conn = get_db()
        conn.execute(
            "INSERT INTO Animais (nome, idade, peso, raca, id_usuario) VALUES (?, ?, ?, ?, ?)",
            (nome, idade, peso, raca, id_usuario)
        )
        conn.commit()
        return redirect('/')
    # Pegar lista de usuários para selecionar dono
    usuarios = get_db().execute("SELECT id, nome FROM Usuarios").fetchall()
    return render_template('cadastro_pet.html', usuarios=usuarios)

@app.route('/consultas')
def listar_consultas():
    consultas = get_db().execute("""
        SELECT c.*, a.nome AS nome_animal
        FROM Consultas c JOIN Animais a ON c.id_animal = a.id
        ORDER BY c.data_consulta DESC
    """).fetchall()
    return render_template('consultas.html', consultas=consultas)

@app.route('/nova_consulta', methods=['GET', 'POST'])
def nova_consulta():
    conn = get_db()
    if request.method == 'POST':
        id_animal = request.form['id_animal']
        vomito = 1 if 'vomito' in request.form else 0
        febre = 1 if 'febre' in request.form else 0
        perda_apetite = 1 if 'perda_apetite' in request.form else 0
        diarreia = 1 if 'diarreia' in request.form else 0
        descricao = request.form['descricao']
        data_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute("""
            INSERT INTO Consultas
            (id_animal, vomito, febre, perda_apetite, diarreia, descricao, data_consulta)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_animal, vomito, febre, perda_apetite, diarreia, descricao, data_consulta))
        conn.commit()
        return redirect('/consultas')
    animais = conn.execute("SELECT id, nome FROM Animais").fetchall()
    return render_template('nova_consulta.html', animais=animais)

if __name__ == '__main__':
    app.run(debug=True)
