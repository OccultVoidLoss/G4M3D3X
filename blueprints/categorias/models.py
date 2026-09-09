class Categoria:

    def __init__(self, nome_categoria, categoria_id = None):
        self.__nome = nome_categoria
        self.__id = categoria_id
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    def to_dict(self):
        return {
            'id' : self.__id,
            'nome': self.__nome
        }
    

