import json
import os
from .models import Jogo, Fisico, Digital
import mysql.connector
from blueprints.categorias.dao import CategoriaDAO


class JogoDAO:

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


    def carregar_jogos(self):
        sql = "SELECT id, Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse, Imagem, Status, Autor, Midia, Console, Distribuicao, Tipo, Tamanho FROM Jogos"
        lista_jogos = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                if linha["Tipo"] == "fisico":
                    jogo = Fisico(
                        linha["Titulo"],
                        linha["Desenvolvedora"],
                        linha["Data_lanc"],
                        linha["Genero"],
                        linha["Sinopse"],
                        None,                  
                        linha["Imagem"],      
                        linha["Midia"], 
                        linha["Console"],     
                        None,                  
                        linha["Status"],       
                        linha["Autor"],       
                        linha["id"]            
                    )
                    print (linha["Midia"], linha["Console"])
                    lista_jogos.append(jogo)
                else:
                    jogo = Digital(
                        linha["Titulo"],
                        linha["Desenvolvedora"],
                        linha["Data_lanc"],
                        linha["Genero"],
                        linha["Sinopse"],
                         None,                    
                        linha["Imagem"],         
                        linha["Distribuicao"],    
                        linha["Tamanho"],         
                        None,                    
                        linha["Status"],          
                        linha["Autor"],          
                        linha["id"]           
                    )
                    lista_jogos.append(jogo)
        finally:
            cursor.close()
            conexao.close()

        return lista_jogos

    def salvar_jogo(self, novo_jogo, categorias, plataformas, autor):
        if novo_jogo.tipo() == "fisico":
            sql = """
            INSERT INTO Jogos (Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse, Imagem, Tipo, Midia, Console, Status, Autor)
            VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s)
            """
            valores = (
                novo_jogo.nome,
                novo_jogo.dev,
                novo_jogo.data,
                novo_jogo.genero,
                novo_jogo.sinopse,
                novo_jogo.img,
                novo_jogo.tipo(),
                novo_jogo.midia,
                novo_jogo.console,
                novo_jogo.status,
                autor
            )
        else:
            sql = """
            INSERT INTO Jogos (Titulo, Desenvolvedora, Data_lanc, Genero, Sinopse ,Imagem, Tipo, Distribuicao, Tamanho, Status, Autor)
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
            """
            valores = (
                novo_jogo.nome,
                novo_jogo.dev,
                novo_jogo.data,
                novo_jogo.genero,
                novo_jogo.sinopse,
                novo_jogo.img,
                novo_jogo.tipo(),
                novo_jogo.distribuicao,
                novo_jogo.tamanho,
                novo_jogo.status,
                autor
            )

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            print("VALORES:")
            for i, valor in enumerate(valores):
                print(i, valor, type(valor))
            cursor.execute(sql, valores)
            
            jogo_id = cursor.lastrowid
            novo_jogo.id = jogo_id
            


            for id_categoria in categorias:
                cursor.execute(
                    "INSERT INTO Jogo_categoria (id_jogo, id_categoria) VALUES (%s, %s)",
                    (jogo_id, id_categoria)
                )

            for id_plataforma in plataformas:
                cursor.execute(
                    "INSERT INTO Jogo_plataforma (Id_jogo, Id_plataforma) VALUES (%s, %s)",
                    (jogo_id, id_plataforma)
    )
            conexao.commit()
                                                            

        finally:
            cursor.close()
            conexao.close()

        return jogo_id

    def buscar_jogo_por_id(self, id_jogo):
        sql1 = "SELECT * FROM Jogos WHERE id=%s"

        sql2 = '''
        SELECT jc.id_categoria, c.nome 
        FROM Jogo_categoria jc
        JOIN Categorias c ON jc.id_categoria = c.id
        WHERE jc.id_jogo = %s
        '''

        sql3 = '''
        SELECT jp.Id_plataforma, p.nome
        FROM Jogo_plataforma jp
        JOIN Plataformas p ON jp.Id_plataforma = p.id
        WHERE jp.Id_jogo = %s
        '''

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            
            cursor.execute(sql1, (id_jogo,))
            jogo = cursor.fetchone()

            
            cursor.execute(sql2, (id_jogo,))
            categorias = cursor.fetchall()
            lista_categorias = [c["nome"] for c in categorias]

            
            cursor.execute(sql3, (id_jogo,))
            plataformas = cursor.fetchall()
            lista_plataformas = [p["Id_plataforma"] for p in plataformas]
            

            
            if jogo["Tipo"] == "fisico":
                jogo_obj = Fisico(
                    jogo["Titulo"],
                    jogo["Desenvolvedora"],
                    jogo["Data_lanc"],
                    jogo["Genero"],
                    jogo["Sinopse"],
                    lista_plataformas,
                    jogo["Imagem"],
                    jogo["Midia"],
                    jogo["Console"],
                    lista_categorias,
                    jogo["Status"],
                    jogo["Autor"],
                    jogo["id"]
                )
            else:
                jogo_obj = Digital(
                    jogo["Titulo"],
                    jogo["Desenvolvedora"],
                    jogo["Data_lanc"],
                    jogo["Genero"],
                    jogo["Sinopse"],
                    lista_plataformas,
                    jogo["Imagem"],
                    jogo["Distribuicao"],
                    jogo["Tamanho"],
                    lista_categorias,
                    jogo["Status"],
                    jogo["Autor"],
                    jogo["id"]
                )

            return jogo_obj

        finally:
            cursor.close()
            conexao.close()




    def atualizar_jogo(self, jogoatt,id):
        if isinstance(jogoatt,Fisico):
            sql = """
            UPDATE Jogos
            SET Titulo  = %s,
            Desenvolvedora = %s,
            Data_lanc = %s,
            Genero = %s,
            Sinopse = %s,
            Imagem  = %s,
            Tipo  = %s,
            Midia  = %s,
            Console = %s
            WHERE id = %s
            """
            val = (
                jogoatt.nome,
                jogoatt.dev,
                jogoatt.data,
                jogoatt.genero,
                jogoatt.sinopse,
                jogoatt.img,
                jogoatt.tipo(),
                jogoatt.midia,
                jogoatt.console,
                id
            )
        else:
            sql = """
            UPDATE Jogos
            SET Titulo  = %s,
            Desenvolvedora = %s,
            Data_lanc = %s,
            Genero = %s,
            Sinopse = %s,
            Imagem  = %s,
            Tipo  = %s,
            Distribuicao  = %s,
            Tamanho = %s
            WHERE id = %s
            """
            val = (
                jogoatt.nome,
                jogoatt.dev,
                jogoatt.data,
                jogoatt.genero,
                jogoatt.sinopse,
                jogoatt.img,
                jogoatt.tipo(),
                jogoatt.distribuicao,
                jogoatt.tamanho,
                id
            )


        conexao = self.__get_connection()
        cursor = conexao.cursor()
        categorias = jogoatt.cat
        if type(categorias) != list:
            categorias = [categorias]
        plataformas = jogoatt.plat
        if type(plataformas) != list:
            plataformas = [plataformas]

        try:
            cursor.execute(sql, val)
            cursor.execute("DELETE FROM Jogo_categoria where id_jogo = %s", (id,))
            cursor.execute("DELETE FROM Jogo_plataforma where id_jogo = %s", (id,))
            for id_categoria in categorias:
                cursor.execute("INSERT INTO Jogo_categoria (id_jogo, id_categoria) VALUES (%s, %s)", (id, id_categoria))
            for id_plataforma in plataformas:
                cursor.execute("INSERT INTO Jogo_plataforma (id_jogo, id_plataforma) VALUES (%s, %s)", (id, id_plataforma))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_jogo(self, id_jogo):
        sql = "DELETE FROM Jogos WHERE id = %s"
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)


        try:
            cursor.execute("SELECT Imagem FROM Jogos WHERE id = %s", (id_jogo,))
            resultado = cursor.fetchone()
            imagem = resultado["Imagem"]
            cursor.execute("DELETE FROM Comentarios WHERE Id_jogo = %s", (id_jogo,))
            cursor.execute("DELETE FROM Jogo_categoria WHERE id_jogo = %s", (id_jogo,))
            cursor.execute(sql, (id_jogo,))
            if imagem:
                caminho = os.path.join("static/uploads/games",imagem)
                os.remove(caminho)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def enviar_comentario(self, autor, comentario, id_autor, Id_jogo, status):
        sql = """
                INSERT INTO Comentarios (Autor, Comentario, Id_autor, Id_jogo, Status)
                VALUES (%s, %s, %s, %s, %s)
            """
        val = (autor, comentario, id_autor, Id_jogo, status)

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, val)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def selecionar_comentario(self, Id_jogo):
        sql = """
            SELECT c.Id, c.Comentario, u.Email, c.Id_autor, c.Status
            FROM Comentarios c
            JOIN Usuario u ON c.id_autor = u.id
            WHERE c.Id_jogo = %s AND c.Status = 'aprovado' 
            """
        conexao = self.__get_connection()
        cursor = conexao.cursor()
        try: 
            cursor.execute(sql, (Id_jogo,))
            resultado = cursor.fetchall()  
        finally: 
            cursor.close()
            conexao.close()
        return resultado 
    
    def carregar_comentarios_pendentes(self):
        sql = """
            SELECT c.Id as Id, c.Comentario, u.Email, c.Id_jogo
            FROM Comentarios c
            JOIN Usuario u ON c.id_autor = u.id
            WHERE c.Status = 'pendente'
            """
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True) 
        try: 
            cursor.execute(sql)
            resultado = cursor.fetchall()  
        finally: 
            cursor.close()
            conexao.close()
        return resultado
    
    def excluir_comentario(self, id_comentario):
        sql = """
            DELETE FROM Comentarios
            WHERE Id = %s
            """
        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (id_comentario,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def aprovar_comentario(self, id_comentario):
        sql = "UPDATE Comentarios SET Status = 'aprovado' WHERE Id = %s"
        conexao = self.__get_connection()
        cursor = conexao.cursor()
        try:
            cursor.execute(sql, (id_comentario,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()



    def bc(self, id_jogo):
            sql = """
                SELECT c.nome
                FROM Categorias c
                JOIN Jogo_categoria jc ON c.id = jc.id_categoria
                WHERE jc.id_jogo = %s
            """

            conexao = self.__get_connection()
            cursor = conexao.cursor()

            try:
                cursor.execute(sql, (id_jogo,))
                resultado = cursor.fetchall()
                return resultado
            finally:
                cursor.close()
                conexao.close()

    def recentes(self):
        sql = "SELECT * FROM Jogos WHERE YEAR(Data_lanc) >= 2020 ORDER BY Data_lanc DESC"
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)
        lista =[]
        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                jogo = Jogo(
                    linha["Titulo"],
                    linha["Desenvolvedora"],
                    linha["Data_lanc"],
                    linha["Genero"],
                    linha["Sinopse"],
                    linha["Plataformas"],
                    linha["Imagem"],
                    None,
                    linha["id"]
                )
                lista.append(jogo)
            return lista
        finally:
            cursor.close()
            conexao.close()
    
    def buscar_jogo_por_categoria(self, categoria):
        sql = " SELECT j.* FROM Jogos j JOIN Jogo_categoria jc ON j.id = jc.id_jogo JOIN Categorias c ON c.id = jc.id_categoria WHERE c.nome = %s"
        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)
        lista_jogos = []
        try:
            cursor.execute(sql, (categoria,))
            for linha in cursor.fetchall():
                if linha["Tipo"] == "fisico":
                    jogo = Fisico(
                        linha["Titulo"],
                        linha["Desenvolvedora"],
                        linha["Data_lanc"],
                        linha["Genero"],
                        linha["Sinopse"],
                        None,                  
                        linha["Imagem"],      
                        linha["Midia"], 
                        linha["Console"],     
                        None,                  
                        linha["Status"],       
                        linha["Autor"],       
                        linha["id"]            
                    )
                    print (linha["Midia"], linha["Console"])
                    lista_jogos.append(jogo)
                else:
                    jogo = Digital(
                        linha["Titulo"],
                        linha["Desenvolvedora"],
                        linha["Data_lanc"],
                        linha["Genero"],
                        linha["Sinopse"],
                         None,                    
                        linha["Imagem"],         
                        linha["Distribuicao"],    
                        linha["Tamanho"],         
                        None,                    
                        linha["Status"],          
                        linha["Autor"],          
                        linha["id"]           
                    )
                    lista_jogos.append(jogo)
            return lista_jogos
            
        finally:
            cursor.close()
            conexao.close()

    def status(self,id, response):
        sql = '''UPDATE Jogos
        SET Status = %s
        WHERE Id = %s'''
        valores = (response, id)
        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
                cursor.execute(sql, valores)
                conexao.commit()
                return id
        finally:
                cursor.close()
                conexao.close()

    def salvar_autor(self,id_autor, id_jogo):
        sql = '''INSERT INTO Jogo_usuario (Id_autor, Id_jogo)
                VALUES (%s, %s) '''
        conexao = self.__get_connection()
        cursor = conexao.cursor()
        valores = (id_autor, id_jogo)
        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()



    def carregar_plataformas(self):
        sql = "Select id,nome FROM Plataformas"
        lista_plataformas = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary = True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                plataforma = {
                "id": linha["id"],
                "nome": linha["nome"]
            }
                lista_plataformas.append(plataforma)
        finally:
            cursor.close()

            conexao.close()

        return lista_plataformas
    

    def buscar_plataforma_por_id(self, id_plataforma):
        sql = "SELECT id, nome FROM Plataformas WHERE id=%s"

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, (id_plataforma,))
            linha = cursor.fetchone()

            if linha:
                return {
                "id": linha["id"],
                "nome": linha["nome"]
            }

            return None

        finally:
            cursor.close()
            conexao.close()