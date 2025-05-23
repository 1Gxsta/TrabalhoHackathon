-- Criação das tabelas
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    peso REAL NOT NULL,
    raca TEXT,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY(id_usuario) REFERENCES Usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal INTEGER NOT NULL,
    vomito BOOLEAN DEFAULT 0,
    febre BOOLEAN DEFAULT 0,
    perda_apetite BOOLEAN DEFAULT 0,
    diarreia BOOLEAN DEFAULT 0,
    descricao TEXT,
    data_consulta TEXT NOT NULL,
    FOREIGN KEY(id_animal) REFERENCES Animais(id) ON DELETE CASCADE
);