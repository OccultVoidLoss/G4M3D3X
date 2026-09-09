
from abc import ABC, abstractmethod

class Jogo(ABC):

    def __init__(self, nome_jogo, dev_jogo, data_lanc, genero_jogo, sinopse_jogo, plataformas_jogo, imagens_jogo, categoria_jogo, status, autor, jogo_id=None):
        self.__nome = nome_jogo
        self.__dev = dev_jogo
        self.__data = data_lanc
        self.__genero = genero_jogo
        self.__sinopse = sinopse_jogo
        self.__plat = plataformas_jogo
        self.__img = imagens_jogo
        self.__cat = categoria_jogo
        self.__status = status
        self.__autor = autor
        self.__id = jogo_id

    @abstractmethod
    def to_dict(self):
        pass
    
    #nome
    @property
    def nome(self):
        return str.capitalize(self.__nome)
    
    
    @nome.setter
    def nome(self, valor):
        self.__nome = str.capitalize(valor)

    #desenvolvedora
    @property 
    def dev(self):
        return self.__dev
    
    @dev.setter
    def dev(self, valor):
        self.__dev = (valor)

    #data de lançamento
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self,valor):
        self.__data = (valor)

    #genero
    @property
    def genero(self):
        return self.__genero
    
    @genero.setter
    def genero(self, v):
        self.__genero = (v)

    #sinopse
    @property
    def sinopse(self):
        return self.__sinopse
    
    @sinopse.setter
    def sinopse(self, v):
        self.__sinopse = (v)

    #plataforma    
    @property
    def plat(self):
        return self.__plat
    
    @plat.setter
    def plat(self, v):
        self.__plat = (v)
    
    #imagens?
    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, v):
        self.__img = (v)

    #categoria
    @property
    def cat(self):
        return self.__cat
    
    @cat.setter
    def cat(self, v):
        self.__cat = (v)

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, v):
        self.__status = (v)


    @property
    def autor(self):
        return self.__autor
    
    @autor.setter
    def autor(self, v):
        self.__autor = (v)


    #id
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, v):
        self.__id = (v)
    
    @abstractmethod
    def tipo(self):
        pass

class Fisico(Jogo):
    def __init__(self, nome_jogo, dev_jogo, data_lanc, genero_jogo, sinopse_jogo, plataformas_jogo, imagens_jogo,midia, console, categoria_jogo, status, autor, jogo_id=None):
        super().__init__(nome_jogo, dev_jogo, data_lanc, genero_jogo, sinopse_jogo, plataformas_jogo, imagens_jogo, categoria_jogo, status, autor, jogo_id)
        self.__midia = midia
        self.__console = console

    @property
    def midia(self):
            return self.__midia
        
    @property
    def console(self):
            return self.__console
        
    def tipo (self):
        return "fisico"
    
    def to_dict(self):
            return {
            "nome": self.nome,
            "dev": self.dev,
            "data": self.data,
            "genero": self.genero,
            "sinopse": self.sinopse,
            "plat": self.plat,
            "img": self.img,
            "categoria": self.cat,
            "status": self.status,
            "midia": self.__midia,
            "console": self.__console,
            "autor": self.__autor,
            "id":self.id
            }   
    

class Digital(Jogo):
    def __init__(self, nome_jogo, dev_jogo, data_lanc, genero_jogo, sinopse_jogo, plataformas_jogo, imagens_jogo,distribuicao, tamanho, categoria_jogo, status, autor, jogo_id=None):
        super().__init__(nome_jogo, dev_jogo, data_lanc, genero_jogo, sinopse_jogo, plataformas_jogo, imagens_jogo, categoria_jogo, status, autor, jogo_id)
        self.__distribuicao = distribuicao
        self.__tamanho = tamanho

    @property
    def distribuicao(self):
            return self.__distribuicao
        
    @property
    def tamanho(self):
            return self.__tamanho
        
    def tipo (self):
            return "digital"
    def to_dict(self):
            return {
            "nome": self.nome,
            "dev": self.dev,
            "data": self.data,
            "genero": self.genero,
            "sinopse": self.sinopse,
            "plat": self.plat,
            "img": self.img,
            "categoria": self.cat,
            "status": self.status,
            "distribuicao": self.distribuicao,
            "tamanho": self.tamanho,
            "autor": self.autor,
            "id":self.id
            }   