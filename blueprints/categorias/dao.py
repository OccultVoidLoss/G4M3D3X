import os
from .models import Categoria
import mysql.connector
from blueprints.base.dao import BaseDAO

class CategoriaDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    
    def carregar_categorias(self):
        sql = "Select id,nome FROM Categorias"
        lista_categorias = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary = True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                categoria = Categoria(linha["nome"],
                            categoria_id = linha["id"])
                lista_categorias.append(categoria)
        finally:
            cursor.close()
            conexao.close()

        return lista_categorias

    def salvar_categoria(self, categoria):
        sql = "Insert into Categorias(Nome) VALUES (%s)"

        conexao = self._get_connection()
        cursor = conexao.cursor()
        valores = categoria.nome,
        try:
            cursor.execute(sql,valores)
            conexao.commit()
            categoria.id = cursor.lastrowid                        
        finally:
            cursor.close()
            conexao.close()
        
        return categoria.id
    

    def buscar_por_id(self, id_categoria):
        sql = "SELECT id, nome FROM Categorias WHERE id=%s"

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, (id_categoria,))
            linha = cursor.fetchone()

            if linha:
                return Categoria(
                    linha["nome"],
                    categoria_id=linha["id"]
                )

            return None

        finally:
            cursor.close()
            conexao.close()

    def remover_categoria(self, id_categoria):
        sql = "DELETE FROM Categorias WHERE id=%s"
        conexao = self._get_connection()
        cursor = conexao.cursor()
        try:
            cursor.execute(sql, (id_categoria,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()
    
    
    def atualizar(self, id_categoria, nome):
        sql = "UPDATE Categorias SET nome=%s WHERE id=%s"

        conexao = self._get_connection()    
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (nome, id_categoria))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()

