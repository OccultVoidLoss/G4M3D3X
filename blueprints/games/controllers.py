from flask import render_template, request, redirect, url_for, flash, session
import os
from .dao import JogoDAO
from blueprints.categorias.dao import CategoriaDAO
from .models import Jogo, Fisico, Digital
from werkzeug.utils import secure_filename
import traceback


class JogoController:

    def __init__(self):
        self.__dao = JogoDAO()
        self.__categoria_dao = CategoriaDAO()

    # LISTAR
    def carregar_jogos(self):
        jogos = self.__dao.carregar_jogos()
        plataformas = self.__dao.carregar_plataformas()

        return render_template(
            "jogos.html",
            jogos=jogos,
            plataformas=plataformas
        )

    # CADASTRAR
    def cadastrar_jogo(self):
            diretorio = "static/uploads/games"
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
            nome = request.form.get("nome")
            dev = request.form.get("dev")
            data = request.form.get("data")
            genero = request.form.get("genero")
            sinopse = request.form.get("sinopse")
            categoria_id = request.form.getlist("categorias")
            img = request.files.get("img")
            plat_id = request.form.getlist("plataformas")
            tipo = request.form.get("tipo")
            autor = int(session.get("user_id"))
            if session["admin"] == True:
                status = "aprovado"
            else:
                status = "pendente"
            

            if not nome or not dev or not data or not genero or not categoria_id or not img or not plat_id or img.filename == "":
                flash("Erro: Preencha todos os campos obrigatórios!", "danger")
                return self.preparar_cadastro()

            try:
                filename = secure_filename(img.filename)
                caminho = os.path.join(diretorio, filename)
                if tipo == "fisico":
                    midia = request.form.get("midia")
                    console = request.form.get("console")
                    novo_jogo = Fisico(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat_id,
                        filename, 
                        midia,
                        console,
                        categoria_id,
                        status,
                        autor
                    )
                else:
                    distribuicao = request.form.get("distribuicao")
                    tamanho = int(request.form.get("tamanho"))
                    novo_jogo = Digital(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat_id,
                        filename,
                        distribuicao,
                        tamanho,
                        categoria_id,
                        status,
                        autor
                    )                   
                self.__dao.salvar_jogo(novo_jogo,categoria_id, plat_id, autor)
                img.save(caminho)

                flash(f"Sucesso: O jogo '{nome}' foi cadastrado!", "success")
                return redirect(url_for("games.listar_jogos"))
            

            except Exception as e:
                traceback.print_exc()
                flash(f"Erro ao cadastrar jogo: {str(e)}", "danger")
                return self.preparar_cadastro()

    def preparar_cadastro(self):
        if 'usuario' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            categorias = self.__categoria_dao.carregar_categorias()
            plataformas = self.__dao.carregar_plataformas()
            return render_template("cadastrar.html", categorias = categorias, plataformas = plataformas)

    # PREPARAR EDIÇÃO
    def preparar_edicao(self, id):
        if 'usuario' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            jogo = self.__dao.buscar_jogo_por_id(id)
            categorias = self.__categoria_dao.carregar_categorias()
            plataformas = self.__dao.carregar_plataformas()

            if not jogo:
                flash("Erro: Jogo não encontrado!", "danger")
                return redirect(url_for("games.listar_jogos"))

            return render_template("editar.html", jogo=jogo, categorias = categorias, plataformas = plataformas)

    # EDITAR
    def editar_jogo(self, id):
        diretorio = "static/uploads/games"
        nome = request.form.get("nome")
        dev = request.form.get("dev")
        data = request.form.get("data")
        genero = request.form.get("genero")
        sinopse = request.form.get("sinopse")
        categoria_id = request.form.getlist("categorias")
        img = request.files.get("img")
        plat = request.form.getlist("plataformas")
        tipo = request.form.get("tipo")
        autor = int(session.get("user_id"))
        status = "aprovado"
        if not nome or not dev or not data or not genero or not categoria_id or not plat or not tipo or not autor:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("games.editar_jogo", id=id))

        try:
            jogo_antigo = self.__dao.buscar_jogo_por_id(id)

            if img and img.filename != "":
                filename = secure_filename(img.filename)
                caminho = os.path.join(diretorio, filename)
                img.save(caminho)
            else:
                filename = jogo_antigo.img
            if tipo == "fisico":
                    midia = request.form.get("midia")
                    console = request.form.get("console")
                    jogo_atualizado = Fisico(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat,
                        filename,
                        midia,
                        console,
                        categoria_id,
                        status,
                        autor
                    )
            else:
                    distribuicao = request.form.get("distribuicao")
                    tamanho = int(request.form.get("tamanho"))
                    jogo_atualizado = Digital(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat,
                        filename,
                        distribuicao,
                        tamanho,
                        categoria_id,
                        status,
                        autor
                    )                 

            self.__dao.atualizar_jogo(jogo_atualizado,id)
            flash(f"Sucesso: O jogo '{nome}' foi atualizado!", "success")
            return redirect(url_for("games.listar_jogos"))

        except Exception as e:
            flash(f"Erro ao atualizar jogo: {str(e)}", "danger")
            return redirect(url_for("games.editar_jogo", id=id))

    # REMOVER
    def remover_jogo(self, id):
        if 'usuario' not in session:
                flash("Erro: deve estar logado para essa função", "danger")
                return redirect(url_for("user.erro"))
        else:
                self.__dao.remover_jogo(id)
                flash("Sucesso: Jogo removido com sucesso!", "success")
                return redirect(url_for("games.listar_jogos"))
    

    def index(self):
        recentes = self.__dao.buscar_jogo_por_categoria("Recente")
        promocoes = self.__dao.buscar_jogo_por_categoria("Em promoção")
        destaques = self.__dao.buscar_jogo_por_categoria("Destaque")
        return render_template("index.html", recentes=recentes, promocoes=promocoes, destaques=destaques)
    


    
    def busca(self):
        nome = request.form.get("nome")
        jogos = self.__dao.carregar_jogos()
        jogos_certo = []
        for jogo in jogos:
            if nome.lower() in jogo.nome.lower():
                jogos_certo.append(jogo)

        return render_template("jogos.html", jogos=jogos_certo)
    
    def detalhe(self, id):
        jogo = self.__dao.buscar_jogo_por_id(id)
        plataformas = []
        for i in jogo.plat:
            p = self.__dao.buscar_plataforma_por_id(i)
            plataformas.append(p)
        comentarios = self.__dao.selecionar_comentario(id)
        return render_template("detalhe.html", jogo=jogo, comentarios=comentarios, plataformas=plataformas)
    
    def enviar_comentario(self):
        if session.get("usuario"):
            comentario = request.form.get("comentario")
            id_autor = session.get("user_id")
            id_jogo = int(request.form.get("id_jogo"))
            
            if session.get("admin") == True:
                status_comentario = "aprovado"
            else:
                status_comentario = "pendente"

            self.__dao.enviar_comentario(
                session.get("usuario"),
                comentario,
                session.get('user_id'),
                id_jogo,
                status_comentario
            )

            if status_comentario == "pendente":
                flash("Seu comentário foi enviado e aguarda a aprovação de um administrador.", "info")
            else:
                flash("Comentário publicado com sucesso!", "success")

            comentarios = self.__dao.selecionar_comentario(id_jogo)
            jogo = self.__dao.buscar_jogo_por_id(id_jogo)

            return render_template("detalhe.html", jogo=jogo, comentarios=comentarios)
        else:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
    
    def excluir_comentario(self, id):
        if session.get("usuario"):        
            id_jogo = int(request.form.get("id_jogo"))  
            self.__dao.excluir_comentario(id)
            flash("Sucesso: Comentário removido com sucesso!", "success")
            return redirect(url_for("games.detalhe", id=id_jogo))
        else:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        
    def aprovar_comentario_controle(self):
        if not session.get("admin"):
            flash("Acesso Negado", "danger")
            return redirect(url_for("user.index"))
            
        id_comentario = request.form.get("id_comentario")
        self.__dao.aprovar_comentario(id_comentario)
        
        flash("Comentário aprovado com sucesso!", "success")
        return redirect(url_for("games.admin_jogos", tipo="comentarios"))

    def rejeitar_comentario_controle(self):
        if not session.get("admin"):
            flash("Acesso Negado", "danger")
            return redirect(url_for("user.index"))
            
        id_comentario = request.form.get("id_comentario")
        self.__dao.excluir_comentario(id_comentario)
        
        flash("Comentário rejeitado com sucesso!", "warning")
        return redirect(url_for("games.admin_jogos", tipo="comentarios"))
        
    def admin_jogos(self):
    # 1. Validação de segurança
        if not session.get("admin"):
            flash("Acesso Negado", "danger")
            return redirect(url_for("user.index"))
        
        
        tipo = request.args.get("tipo")
        
        
        if tipo == "comentarios":
            
            c_pendentes = self.__dao.carregar_comentarios_pendentes() 
            return render_template("admin/comentarios.html", comentarios=c_pendentes)
        
        lista_jogos = self.__dao.carregar_jogos()
        j_pendentes = []
        for jogo in lista_jogos:
            if jogo.status == "pendente":
                j_pendentes.append(jogo)
                
        return render_template("admin/jogos.html", jogos=j_pendentes)
    

    def status(self,id,response):
        if not session.get("admin"):
            flash("Acesso Negado","danger")
            return redirect(url_for("user.index"))
        self.__dao.status(id,response)
        return redirect(url_for("games.admin_jogos"))
    

    