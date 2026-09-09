from flask import Flask, render_template, request, redirect, url_for, flash
from . import games_bp
from .controllers import JogoController



controller = JogoController()


# --- ROTAS (Páginas da Web) ---
@games_bp.route("/")
def index():
    return controller.index()

@games_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_jogo():
    if request.method == "POST":
        return controller.cadastrar_jogo()

    return controller.preparar_cadastro()


@games_bp.route("/jogos")
def listar_jogos():
    return controller.carregar_jogos()


@games_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_jogo(id):
    if request.method == "POST":
        return controller.editar_jogo(id)
    return controller.preparar_edicao(id)


@games_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir_jogo(id):
    return controller.remover_jogo(id)


@games_bp.route("/detalhe/<int:id>", methods= ["POST", "GET"])
def detalhe(id):
    return controller.detalhe(id)

@games_bp.route("/busca", methods= ["POST", "GET"])
def busca():
    return controller.busca()

@games_bp.route("/comentar", methods=["POST"])
def comentar():
    return controller.enviar_comentario()

@games_bp.route("/excluir_comentario/<int:id>", methods=["POST"])
def excluir_comentario(id):
    return controller.excluir_comentario(id)

@games_bp.route("/admin/jogos", methods=["POST", "GET"])
def admin_jogos():
    return controller.admin_jogos()

@games_bp.route("/admin/status/<response>/<int:id>", methods=["POST", "GET"])
def status(id,response):
    return controller.status(id,response)

@games_bp.route("/admin/comentarios/aprovar", methods=["POST"])
def aprovar_comentario_controle():
    return controller.aprovar_comentario_controle()

@games_bp.route("/admin/comentarios/rejeitar", methods=["POST"])
def rejeitar_comentario_controle():
    return controller.rejeitar_comentario_controle()