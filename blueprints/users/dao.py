import json
import os
from .models import User, Comum, Admin
import mysql.connector


class UserDAO:

    def __init__(self):
        self.__db_config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'port': os.getenv("MYSQL_PORT")
        }

    def __get_connection(self):
        return mysql.connector.connect(**self.__db_config)

    @property
    def arquivo_caminho(self):
        return self.__arquivo_caminho

    @arquivo_caminho.setter
    def arquivo_caminho(self, v):
        self.__arquivo_caminho = v


    def carregar_user(self):
        sql = "SELECT id, Nome, Email, Senha, Tipo FROM Usuario"
        lista_user = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                if linha["Tipo"] == "comum":  
                    user = Comum(
                        linha["Nome"],
                        linha["Email"],
                        linha["Senha"],
                        linha["id"]
                    )
                    lista_user.append(user)
                else:
                    user = Admin(
                        linha["Nome"],
                        linha["Email"],
                        linha["Senha"],
                        linha["id"]
                    )
                    lista_user.append(user)
        finally:
            cursor.close()
            conexao.close()

        return lista_user

    def salvar_user(self, novo_user, tipo):
        sql = """
        INSERT INTO Usuario (Nome, Email, Senha, Tipo)
        VALUES (%s,%s, %s, %s)
        """
        valores = (
            novo_user.nome,
            novo_user.email,
            novo_user.senha,
            tipo
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            novo_user.id = cursor.lastrowid
        finally:
            cursor.close()
            conexao.close()

        return novo_user.id

    def buscar_user_por_id(self, user_id):
        user = self.carregar_user()
        for usuario in user:
            if usuario.id == user_id:
                return usuario
        return None


    def atualizar_user(self, useratt):
        sql = """
        UPDATE Usuario
        SET Email = %s,
            Senha = %s
        WHERE id = %s
        """

        val = (
            useratt.email,
            useratt.senha,
            useratt.id
        )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, val)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_user(self, id_user):
        sql = "DELETE FROM Usuario WHERE id = %s"

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute("DELETE FROM Comentarios WHERE id_autor = %s", (id_user,))
            cursor.execute(sql, (id_user,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()


    def editar_user(self, user_att):
        sql =  '''UPDATE Usuario
        SET Nome = %s, 
            Email = %s,
            Senha = %s
        WHERE ID = %s'''
        conexao = self.__get_connection()
        cursor = conexao.cursor()
        valores = (user_att.nome, user_att.email, user_att.senha, user_att.id)
        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()
 
    def promover(self, id):
        sql =         '''UPDATE Usuario
        SET Tipo = 'admin'
        WHERE id = %s '''
        conexao = self.__get_connection()    
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (id,))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()

    def rebaixar(self, id):
        sql =         '''UPDATE Usuario
        SET Tipo = 'comum'
        WHERE id = %s '''
        conexao = self.__get_connection()    
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (id,))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()


    