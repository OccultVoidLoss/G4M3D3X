from flask import Flask, render_template, request, redirect, url_for, flash, session
from .dao import CategoriaDAO
from .models import Categoria
from blueprints.users.controllers import login_required, admin_required

class CategoriaController:

    def __init__(self):
        self.__dao = CategoriaDAO()

    def listar_categorias(self):
        lista = self.__dao.carregar_categorias()
        return render_template("categorias/categorias.html",categorias=lista)

    @admin_required
    def preparar_cadastro(self):
            return render_template("categorias/cadastrar.html")

    def cadastrar_categoria(self):
        nome = request.form.get("nome")

        if not nome:
            flash("Erro: O nome da categoria é obrigatório!", "danger")
            return self.preparar_cadastro()

        nova_categoria = Categoria(nome)
        self.__dao.salvar_categoria(nova_categoria)
        flash(f"Sucesso: Categoria '{nome}' cadastrada com sucesso!", "success")
        return redirect(url_for("categorias.listar_categorias"))
    

    def preparar_edicao(self, id):
        categoria = self.__dao.buscar_por_id(id)
        return render_template("categorias/editar_categoria.html", categoria=categoria)


    def editar_categoria(self, id):
        nome = request.form.get("nome")

        self.__dao.atualizar(id, nome)

        flash("Categoria atualizada!", "success")

        return redirect(url_for("categorias.listar_categorias"))
    
    def remover_categoria(self,id):
        self.__dao.remover_categoria(id)
        flash("Sucesso: Categoria removida com sucesso!", "success")
        return redirect(url_for("categorias.listar_categorias"))
    
