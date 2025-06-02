create database doacaoAlimentos;

CREATE TABLE Endereco (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cep VARCHAR(9),
    logradouro VARCHAR(100),
    bairro VARCHAR(100),
    uf CHAR(2),
    cidade VARCHAR(100)
);

CREATE TABLE Perfil (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE Users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(50) unique not null,
    senha_hash VARCHAR(100) not null,
    telefone VARCHAR(30) not null,
    documento VARCHAR(20) not null,
    perfil_id BIGINT not null,
    endereco_id BIGINT,
    numero VARCHAR(20),
    complemento VARCHAR(100),
	FOREIGN KEY (perfil_id) REFERENCES Perfil(id) ON DELETE RESTRICT,
	FOREIGN KEY (endereco_id) REFERENCES Endereco(id) ON DELETE SET NULL
);

CREATE TABLE Status (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(30)
);

CREATE TABLE Doacao (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doador_id BIGINT not null,
    solicitante_id BIGINT,
    dataDoacao DATETIME not null,
    status_id BIGINT not null,
    data_recebimento DATETIME,
    FOREIGN KEY (doador_id) REFERENCES Users(id),
    FOREIGN KEY (solicitante_id) REFERENCES Users(id),
    FOREIGN KEY (status_id) REFERENCES Status(id)
);

CREATE TABLE Alimento (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) not null,
    marca VARCHAR(50)
);

CREATE TABLE DoacaoItem (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doacao_id BIGINT not null,
    alimento_id BIGINT not null,
    quantidade INT not null,
    data_vencimento DATE,
    FOREIGN KEY (doacao_id) REFERENCES Doacao(id),
    FOREIGN KEY (alimento_id) REFERENCES Alimento(id)
);