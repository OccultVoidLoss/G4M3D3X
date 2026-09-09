DROP DATABASE IF EXISTS games_db;
CREATE DATABASE IF NOT EXISTS games_db;
USE games_db;


CREATE TABLE IF NOT EXISTS Jogos(
	id INT auto_increment PRIMARY KEY,
    Titulo VARCHAR(50),
    Desenvolvedora VARCHAR (50),
    Data_lanc DATE,
    Genero VARCHAR(50),
    Sinopse VARCHAR (1000),
    Imagem VARCHAR(1000) ,
    Midia VARCHAR(1000),
    Console VARCHAR(1000), 
    Distribuicao VARCHAR(1000),
    Tipo VARCHAR(1000),
    Tamanho INT,
    Status VARCHAR(50),
    Autor Int
);

CREATE TABLE IF NOT EXISTS Usuario(
		id INT auto_increment PRIMARY KEY,
        Nome VARCHAR(50),
		Email VARCHAR(50),
        Senha VARCHAR(1000),
        Tipo VARCHAR(50)
);




CREATE TABLE IF NOT EXISTS Comentarios(
		Id INT auto_increment PRIMARY KEY,
		Autor VARCHAR(50),
        Comentario VARCHAR(1000),
        Id_autor INT,
        Id_jogo INT,
        Status VARCHAR(50) DEFAULT 'pendente'
        
);




CREATE TABLE IF NOT EXISTS Categorias(
		Id INT auto_increment PRIMARY KEY,
        Nome VARCHAR(50)
);



CREATE TABLE IF NOT EXISTS Jogo_categoria(
		Id_jogo INT NOT NULL,
		Id_categoria INT NOT NULL,
        PRIMARY KEY (Id_jogo, Id_categoria)

	
);


CREATE TABLE IF NOT EXISTS Plataformas(
		Id INT auto_increment PRIMARY KEY,
        Nome VARCHAR(50)
);



CREATE TABLE IF NOT EXISTS Jogo_plataforma(
		Id_jogo INT NOT NULL,
		Id_plataforma INT NOT NULL,
        PRIMARY KEY (Id_jogo, Id_plataforma)
);

ALTER TABLE Jogo_plataforma
ADD CONSTRAINT fk_jogoss FOREIGN KEY (Id_jogo) REFERENCES Jogos(id) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_plataformas FOREIGN KEY (Id_plataforma) REFERENCES Plataformas(Id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Jogo_categoria
ADD CONSTRAINT fk_jogos FOREIGN KEY (Id_jogo) REFERENCES Jogos(id) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_categorias FOREIGN KEY (Id_categoria) REFERENCES Categorias(Id) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE Comentarios
ADD CONSTRAINT fk_autor FOREIGN KEY (Id_autor) REFERENCES Usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_jogo FOREIGN KEY (Id_jogo) REFERENCES Jogos(id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Jogos
ADD CONSTRAINT fk_games FOREIGN KEY (Autor) REFERENCES Usuario(Id) ON DELETE CASCADE ON UPDATE CASCADE;

INSERT INTO Categorias(nome)
VALUES
("Destaque"),
("Recente"),
("Em promoção");

select * from Jogos;


INSERT INTO Plataformas(nome)
VALUES
("PlayStation 5"),
("PlayStation 4"),
("PlayStation 3"),
("PlayStation 2"),
("PlayStation 1"),
("Xbox"),
("Xbox 360"),
("Xbox One"),
("Xbox One S"),
("Xbox One X"),
("Xbox Series S"),
("Xbox Series X"),
("Microsoft Windows"),
("macOS"),
("Linux"),
("Android"),
("iOS");