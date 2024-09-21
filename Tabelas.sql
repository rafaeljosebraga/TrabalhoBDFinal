CREATE TABLE Empresa (
    registro VARCHAR2(7) PRIMARY KEY,
    nome VARCHAR2(50) NOT NULL
);

CREATE TABLE JazidaUnobtanium (
    latitude NUMBER(5,2),
    longitude NUMBER(6,2),
    estado CHAR(1),
    reserva NUMBER(5,1),
    base NUMBER(4,1),
    altura NUMBER(4,1),
    nomeVale VARCHAR2(50),
    nomeMontanha VARCHAR2(50),
    movimento CHAR(1),
    nomePlanicie VARCHAR2(50),
    CONSTRAINT PK_jazida_lat_long PRIMARY KEY (latitude, longitude),
  	CONSTRAINT FK_jazida_vale FOREIGN KEY (nomeVale) REFERENCES Vale(nome) ON DELETE CASCADE,
  	CONSTRAINT FK_jazida_montanha FOREIGN KEY (nomeMontanha) REFERENCES Montanha(nome) ON DELETE CASCADE,
  	CONSTRAINT FK_jazida_planicie FOREIGN KEY (nomePlanicie) REFERENCES Planicie(nome) 	ON DELETE CASCADE,
    CONSTRAINT  CHK_estado_exclusive CHECK (estado IN (0, 1)),
    CONSTRAINT CHK_JazidaUnobtanium_exclusive CHECK (
        (nomevale IS NOT NULL AND nomemontanha IS NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NOT NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NULL AND nomeplanicie IS NOT NULL)
    ),
    CONSTRAINT CHK_movimento_montanha CHECK (
        (nomeMontanha IS NOT NULL AND movimento IN ('0', '1')) OR 
        (nomeMontanha IS NULL AND movimento IS NULL)
    )
);

CREATE TABLE Colonia (
    nome VARCHAR2(50) PRIMARY KEY,
    pressurizada CHAR(1),
    apelido VARCHAR2(46),
    registroEmpresa VARCHAR2(7) NOT NULL,
  	latitude NUMBER(5,2) NOT NULL,
    longitude NUMBER(6,2) NOT NULL,
    CONSTRAINT FK_colonia_empresa FOREIGN KEY (registroEmpresa) REFERENCES Empresa(registro) ON DELETE CASCADE,
  	CONSTRAINT FK_colonia_jazida FOREIGN KEY (latitude, longitude) REFERENCES JazidaUnobtanium(latitude, longitude) ON DELETE CASCADE,
    CONSTRAINT  CHK_pressurizada_exclusive CHECK (pressurizada IN (0, 1)) 
);

CREATE TABLE Servivodepandora (
    ID INT PRIMARY KEY,
    descricao VARCHAR2(200)
);

CREATE TABLE Conexao (
    ID_A INT,
    ID_B INT,
    tipoconexao VARCHAR2(15),
    CONSTRAINT PK_conexao PRIMARY KEY (ID_A, ID_B), 
    CONSTRAINT FK_conexao_servivopandoraA FOREIGN KEY (ID_A) REFERENCES Servivodepandora(ID) ON DELETE CASCADE,
    CONSTRAINT FK_conexao_servivopandoraB FOREIGN KEY (ID_B) REFERENCES Servivodepandora(ID) ON DELETE CASCADE
);

CREATE TABLE Regiaocontrole (
    nome VARCHAR2(50) PRIMARY KEY,
    regiao VARCHAR2(8),
    CONSTRAINT CHK_regiaocontrole_exclusive CHECK (regiao IN ('Montanha', 'Planicie', 'Vale')) 
);

CREATE TABLE Montanha (
    nome VARCHAR2(50) PRIMARY KEY,
    altura NUMBER(5,1),
    CONSTRAINT FK_montanha_regiaocontrole FOREIGN KEY (nome) REFERENCES Regiaocontrole(nome) ON DELETE CASCADE
);

CREATE TABLE Planicie (
    nome VARCHAR2(50) PRIMARY KEY,
    CONSTRAINT FK_planicie_regiaocontrole FOREIGN KEY (nome) REFERENCES Regiaocontrole(nome) ON DELETE CASCADE
);

CREATE TABLE Vale (
    nome VARCHAR2(50) PRIMARY KEY,
    agua CHAR(1),
    profundidade NUMBER(5,2),  
    CONSTRAINT FK_vale_regiaocontrole FOREIGN KEY (nome) REFERENCES Regiaocontrole(nome) ON DELETE CASCADE,
    CONSTRAINT  CHK_agua_exclusive CHECK (agua IN (0, 1)) 
);

CREATE TABLE Rios (
    nome VARCHAR2(50) PRIMARY KEY,
    rio VARCHAR(30),
    CONSTRAINT FK_rios_planicie FOREIGN KEY (nome) REFERENCES Planicie(nome) ON DELETE CASCADE
);

CREATE TABLE Lagos (
    nome VARCHAR2(50) PRIMARY KEY,
    lago VARCHAR2(30),
    CONSTRAINT FK_lagos_planicie FOREIGN KEY (nome) REFERENCES Planicie(nome) ON DELETE CASCADE
);

CREATE TABLE Thanator (
    ID INT PRIMARY KEY,
    velocidademaxima NUMBER(4,1),
    forca NUMBER(5,1),
    nomevale VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_thanator_servivopandora FOREIGN KEY (ID) REFERENCES Servivodepandora(ID) ON DELETE CASCADE,
    CONSTRAINT FK_thanator_vale FOREIGN KEY (nomevale) REFERENCES Vale(nome) 
);

CREATE TABLE Leonopteryx (
    ID INT PRIMARY KEY,
    asatamanho NUMBER(5,2),
    cor VARCHAR2(20),
    nomevale VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_leonopteryx_servivopandora FOREIGN KEY (ID) REFERENCES Servivodepandora(ID) ON DELETE CASCADE,
    CONSTRAINT FK_leonopteryx_vale FOREIGN KEY (nomevale) REFERENCES Vale(nome) 
);

CREATE TABLE Direhorses (
    ID INT PRIMARY KEY,
    nomeplanicie VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_direhorses_servivopandora FOREIGN KEY (ID) REFERENCES Servivodepandora(ID) ON DELETE CASCADE,
    CONSTRAINT FK_direhorses_planicie FOREIGN KEY (nomeplanicie) REFERENCES Planicie(nome)
);

--arvore tem check que é uma condiçao especial
CREATE TABLE Arvorecontrole (
    ID INT PRIMARY KEY,
    tipoArvore VARCHAR2(9),
    CONSTRAINT CHK_Arvorecontrole_exclusive CHECK (tipoArvore IN ('Arv_alma', 'Arv_lar', 'Arv_vozes', 'Arv_vida'))
);

CREATE TABLE Arv_alma (
    ID INT PRIMARY KEY,
    nomevale VARCHAR2(50),
    nomemontanha VARCHAR2(50),
    nomeplanicie VARCHAR2(50),
    CONSTRAINT FK_alma_arvorecontrole FOREIGN KEY (ID) REFERENCES Arvorecontrole(ID) ON DELETE CASCADE,
    CONSTRAINT FK_alma_vale FOREIGN KEY (nomevale) REFERENCES Vale(nome) ON DELETE CASCADE,
    CONSTRAINT FK_alma_montanha FOREIGN KEY (nomemontanha) REFERENCES Montanha(nome) ON DELETE CASCADE,
    CONSTRAINT FK_alma_planicie FOREIGN KEY (nomeplanicie) REFERENCES Planicie(nome) ON DELETE CASCADE,
    CONSTRAINT CHK_Arv_alma_exclusive CHECK (
        (nomevale IS NOT NULL AND nomemontanha IS NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NOT NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NULL AND nomeplanicie IS NOT NULL)
    )
);

CREATE TABLE Divindade (
    nome VARCHAR2(30) PRIMARY KEY,
    IDalma INT,
    CONSTRAINT FK_divindade_IDalma FOREIGN KEY (IDalma) REFERENCES Arv_alma(ID) ON DELETE CASCADE
);

CREATE TABLE Habitacao (
    altura NUMBER(4,1) PRIMARY KEY,
    capacidadehabitante INT
);

CREATE TABLE Arv_lar (
    ID INT PRIMARY KEY,
    idade INT,
    altura NUMBER(4,1) NOT NULL,
    nomevale VARCHAR2(50),
    nomemontanha VARCHAR2(50),
    nomeplanicie VARCHAR2(50),
    CONSTRAINT FK_lar_arvorecontrole FOREIGN KEY (ID) REFERENCES Arvorecontrole(ID) ON DELETE CASCADE,
    CONSTRAINT FK_habitacao_arv_lar FOREIGN KEY (altura) REFERENCES Habitacao(altura),
    CONSTRAINT FK_lar_vale FOREIGN KEY (nomevale) REFERENCES Vale(nome) ON DELETE CASCADE,
    CONSTRAINT FK_lar_montanha FOREIGN KEY (nomemontanha) REFERENCES Montanha(nome) ON DELETE CASCADE,
    CONSTRAINT FK_lar_planicie FOREIGN KEY (nomeplanicie) REFERENCES Planicie(nome) ON DELETE CASCADE,
    CONSTRAINT CHK_Arv_lar_exclusive CHECK (
        (nomevale IS NOT NULL AND nomemontanha IS NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NOT NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NULL AND nomeplanicie IS NOT NULL)
    )
);

CREATE TABLE Arv_vozes (
    ID INT PRIMARY KEY,
    nomevale VARCHAR2(50),
    nomemontanha VARCHAR2(50),
    nomeplanicie VARCHAR2(50),
    CONSTRAINT FK_vozes_arvorecontrole FOREIGN KEY (ID) REFERENCES Arvorecontrole(ID) ON DELETE CASCADE,
    CONSTRAINT FK_vozes_vale FOREIGN KEY (nomevale) REFERENCES Vale(nome) ON DELETE CASCADE,
    CONSTRAINT FK_vozes_montanha FOREIGN KEY (nomemontanha) REFERENCES Montanha(nome) ON DELETE CASCADE,
    CONSTRAINT FK_vozes_planicie FOREIGN KEY (nomeplanicie) REFERENCES Planicie(nome) ON DELETE CASCADE,
    CONSTRAINT CHK_Arv_vozes_exclusive CHECK (
        (nomevale IS NOT NULL AND nomemontanha IS NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NOT NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NULL AND nomeplanicie IS NOT NULL)
    )
);

CREATE TABLE Arv_vida (
    ID INT PRIMARY KEY,
    nomevale VARCHAR2(50),
    nomemontanha VARCHAR2(50),
    nomeplanicie VARCHAR2(50),
    CONSTRAINT FK_vida_arvorecontrole FOREIGN KEY (ID) REFERENCES Arvorecontrole(ID) ON DELETE CASCADE,
    CONSTRAINT FK_vida_vale FOREIGN KEY (nomevale) REFERENCES Vale(nome) ON DELETE CASCADE,
    CONSTRAINT FK_vida_montanha FOREIGN KEY (nomemontanha) REFERENCES Montanha(nome) ON DELETE CASCADE,
    CONSTRAINT FK_vida_planicie FOREIGN KEY (nomeplanicie) REFERENCES Planicie(nome) ON DELETE CASCADE,
    CONSTRAINT CHK_Arv_vida_exclusive CHECK (
        (nomevale IS NOT NULL AND nomemontanha IS NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NOT NULL AND nomeplanicie IS NULL) OR
        (nomevale IS NULL AND nomemontanha IS NULL AND nomeplanicie IS NOT NULL)
    )
);

CREATE TABLE Humano (
    ID INT PRIMARY KEY,
    nome VARCHAR2(100),
    nomecolonia VARCHAR2(50) NOT NULL,
    mascara CHAR(1),
    IdAlma INT,
    CONSTRAINT FK_humano_colonia FOREIGN KEY (nomecolonia) REFERENCES Colonia(nome) ON DELETE CASCADE,
    CONSTRAINT FK_humano_alma FOREIGN KEY (IdAlma) REFERENCES Arv_alma(ID),
    CONSTRAINT  CHK_mascara_exclusive CHECK (mascara IN (0, 1))
);

CREATE TABLE Militar (
    ID INT PRIMARY KEY,
    nome VARCHAR2(100),
    especializacao VARCHAR2(46),
    CONSTRAINT FK_militar_humano FOREIGN KEY (ID) REFERENCES Humano(ID) ON DELETE CASCADE
);

CREATE TABLE Minerador (
    ID INT PRIMARY KEY,
    nome VARCHAR2(100),
    funcao VARCHAR2(100),
    CONSTRAINT FK_minerador_humano FOREIGN KEY (ID) REFERENCES Humano(ID) ON DELETE CASCADE
);

CREATE TABLE Cientista (
    ID INT PRIMARY KEY,
    nome VARCHAR2(100),
    especializacao VARCHAR2(46),
    CONSTRAINT FK_cientista_humano FOREIGN KEY (ID) REFERENCES Humano(ID) ON DELETE CASCADE
);

CREATE TABLE Cla (
    nome VARCHAR2(30) PRIMARY KEY,
    IDlar INT NOT NULL,
    CONSTRAINT FK_cla_arv_lar FOREIGN KEY (IDlar) REFERENCES Arv_lar(ID) 
);

CREATE TABLE Navi (
    ID INT PRIMARY KEY,
    nome VARCHAR2(60) UNIQUE,
    altura NUMBER(3,1),
    qtdBiolum INT,
    tomaazul VARCHAR2(15),
    nomeCla VARCHAR2(30) NOT NULL,
    funcaoCla VARCHAR2(46),
    IDvida INT NOT NULL,
    qtdSemente INT,
    IDvoz INT NOT NULL,
    qtdAntepassado INT,
    CONSTRAINT FK_navi_servivopandora FOREIGN KEY (ID) REFERENCES Servivodepandora(ID) ON DELETE CASCADE,
    CONSTRAINT FK_navi_cla FOREIGN KEY (nomecla) REFERENCES Cla(nome),
    CONSTRAINT FK_navi_arv_vida FOREIGN KEY (IDvida) REFERENCES Arv_vida(ID),
    CONSTRAINT FK_navi_arv_vozes FOREIGN KEY (IDvoz) REFERENCES Arv_vozes(ID)
);

CREATE TABLE Caracteristicas (
    IDnavi INT,
    caracteristicas VARCHAR2(100), 
    CONSTRAINT PK_caracteristicas PRIMARY KEY (IDnavi, caracteristicas),
    CONSTRAINT FK_caracteristicas_navi FOREIGN KEY (IDnavi) REFERENCES Navi(ID) ON DELETE CASCADE
);

CREATE TABLE Dinasta (
    nomecla VARCHAR2(30),
    dinastia VARCHAR2(50),
    nomenavi VARCHAR2(60) NOT NULL,
    CONSTRAINT PK_dinasta PRIMARY KEY (nomecla,dinastia),
    CONSTRAINT FK_dinasta_cla FOREIGN KEY (nomecla) REFERENCES Cla(nome) ON DELETE CASCADE,
    CONSTRAINT FK_dinasta_navi FOREIGN KEY (nomenavi) REFERENCES Navi(nome) ON DELETE CASCADE
);

CREATE TABLE Banshee (
    ID INT PRIMARY KEY,
    alturavoo NUMBER(5,1),
    cor VARCHAR2(20),
    IDnavi INT,
    nomemontanha VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_banshee_servivopandora FOREIGN KEY (ID) REFERENCES Servivodepandora(ID) ON DELETE CASCADE,
    CONSTRAINT FK_banshee_navi FOREIGN KEY (IDnavi) REFERENCES Navi(ID),
    CONSTRAINT FK_banshee_montanha FOREIGN KEY (nomemontanha) REFERENCES Montanha(nome)
);

CREATE TABLE Guerreiro (
    ID INT PRIMARY KEY,
    intitulacao VARCHAR2(46),
    IDnavi INT UNIQUE NOT NULL,
    IDbanshee INT UNIQUE NOT NULL,
    CONSTRAINT FK_guerreiro_navi FOREIGN KEY (IDnavi) REFERENCES Navi(ID) ON DELETE CASCADE,
    CONSTRAINT FK_guerreiro_banshee FOREIGN KEY (IDbanshee) REFERENCES Banshee(ID) ON DELETE CASCADE
);   

CREATE TABLE Guerreirocla (
    IDnavi INT PRIMARY KEY,
    nomecla VARCHAR2(30) NOT NULL,
    CONSTRAINT FK_guerreirocla_guerreiro FOREIGN KEY (IDnavi) REFERENCES Guerreiro(IDnavi) ON DELETE CASCADE,
    CONSTRAINT FK_guerreirocla_cla FOREIGN KEY (nomecla) REFERENCES Cla(nome) ON DELETE CASCADE
);   

CREATE TABLE Maquinario (
    nome VARCHAR2(50) PRIMARY KEY,
    tipoMaquina VARCHAR2(30),
    potencia NUMBER(5,1),
    pesoOperacional NUMBER(6,2),
    latitudejazida NUMBER(5,2) NOT NULL,
    longitudejazida NUMBER(6,2) NOT NULL,
    CONSTRAINT FK_maquinario_jazida FOREIGN KEY (latitudejazida,longitudejazida) REFERENCES JazidaUnobtanium(latitude,longitude)
);

CREATE TABLE Escavadeira (
    nome VARCHAR2(50) PRIMARY KEY,
    capacidade_pa NUMBER(4,2),
    CONSTRAINT FK_escavadeira_maquinario FOREIGN KEY (nome) REFERENCES Maquinario(nome) ON DELETE CASCADE
);

CREATE TABLE Caminhao (
    nome VARCHAR2(50) PRIMARY KEY,
    capacidade NUMBER(4,2),
    CONSTRAINT FK_caminhao_maquinario FOREIGN KEY (nome) REFERENCES Maquinario(nome) ON DELETE CASCADE
);

CREATE TABLE ConteinerControle (
    numeroserie INT PRIMARY KEY,
    tipoconteiner VARCHAR2(11),
    CONSTRAINT CHK_ConteinerControle_exclusive CHECK (tipoconteiner IN ('Deposito', 'Residencia', 'Laboratorio'))  
);

CREATE TABLE Deposito (
    numeroserie INT PRIMARY KEY,
    nome VARCHAR2(46),
    sigla VARCHAR2(10),
    tamanho NUMBER(5,2),
    tipo VARCHAR2(46),
    nomecolonia VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_deposito_containercontrole FOREIGN KEY (numeroserie) REFERENCES ConteinerControle(numeroserie) ON DELETE CASCADE,
    CONSTRAINT FK_deposito_colonia FOREIGN KEY (nomecolonia) REFERENCES Colonia(nome) 
);    

CREATE TABLE Residencia (
    numeroserie INT PRIMARY KEY,   
    nome VARCHAR2(46),
    sigla VARCHAR2(10),
    tamanho NUMBER(5,2),
    qtdcama INT,
    qtdbanheiro INT,
    nomecolonia VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_residencia_containercontrole FOREIGN KEY (numeroserie) REFERENCES ConteinerControle(numeroserie) ON DELETE CASCADE,
    CONSTRAINT FK_residencia_colonia FOREIGN KEY (nomecolonia) REFERENCES Colonia(nome) 
);

CREATE TABLE Laboratorio (
    numeroserie INT PRIMARY KEY,
    nome VARCHAR2(46),
    sigla VARCHAR2(10),
    tamanho NUMBER(5,2),
    finalidade VARCHAR2(46),
    nomecolonia VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_laboratorio_containercontrole FOREIGN KEY (numeroserie) REFERENCES ConteinerControle(numeroserie) ON DELETE CASCADE,
    CONSTRAINT FK_laboratorio_colonia FOREIGN KEY (nomecolonia) REFERENCES Colonia(nome) 
);

CREATE TABLE Pesquisa (
    nome VARCHAR2(50) PRIMARY KEY,
    investimento NUMBER(10,2),
    numeroserielab INT UNIQUE NOT NULL,
    IDcientista INT UNIQUE NOT NULL,
    CONSTRAINT FK_pesquisa_equipamento FOREIGN KEY (numeroserielab) REFERENCES Laboratorio(numeroserie),
    CONSTRAINT FK_pesquisa_cientista FOREIGN KEY (IDcientista) REFERENCES Cientista(ID) 
);

CREATE TABLE Avatar (
    IDAvatar INT PRIMARY KEY,
    nomepesquisa VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_avatar_navi FOREIGN KEY (IDAvatar) REFERENCES Navi(ID) ON DELETE CASCADE,
    CONSTRAINT FK_avatar_pesquisa FOREIGN KEY (nomepesquisa) REFERENCES Pesquisa(nome) ON DELETE CASCADE
);

CREATE TABLE Avatarhumano (
    IDhumano INT PRIMARY KEY,
    IDhAvatar INT NOT NULL,
    compatibilidadeGenetica NUMBER(5,2),
    CONSTRAINT FK_avatarhumano_humano FOREIGN KEY (IDhumano) REFERENCES Humano(ID),
    CONSTRAINT FK_avatarhumano_avatar FOREIGN KEY (IDhAvatar) REFERENCES Avatar(IDAvatar) ON DELETE CASCADE
);

CREATE TABLE Equipamento (
    ID INT PRIMARY KEY,
    nome VARCHAR2(50) NOT NULL,
    consumoEnergetico NUMBER(4,2),
    utilidade VARCHAR2(100),
    nomePesquisa VARCHAR2(50),
    CONSTRAINT FK_equipamento_pesquisa FOREIGN KEY (nomePesquisa) REFERENCES Pesquisa(nome)
);
