-- Tabela de usuários
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL UNIQUE,
    senha VARCHAR(45) NOT NULL
);

-- Tabela de animais
CREATE TABLE IF NOT EXISTS Animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(45) NOT NULL,
    idade INTEGER CHECK(idade >= 0),
    peso REAL CHECK(peso > 0),
    raca VARCHAR(45),
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- Tabela de consultas
CREATE TABLE IF NOT EXISTS Consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal INTEGER NOT NULL,
    
    vomito BOOLEAN DEFAULT 0,
    febre BOOLEAN DEFAULT 0,
    perda_apetite BOOLEAN DEFAULT 0,
    diarreia BOOLEAN DEFAULT 0,

    descricao VARCHAR(150),
    data_consulta TEXT NOT NULL,

    FOREIGN KEY (id_animal) REFERENCES Animais(id) ON DELETE CASCADE
);
