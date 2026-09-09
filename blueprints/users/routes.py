from flask import Flask, render_template, request, redirect, url_for, flash
from . import user_bp
from .controllers import UserController



controller = UserController()



@user_bp.route("/cadastro", methods=["GET"])
def cadastrar_user():

    return controller.preparar_cadastro()


@user_bp.route("/api/auth/registro", methods=["POST"])
def cadastrar_user_api():
    return controller.cadastrar_user()


@user_bp.route("/")
def index():
    return controller.index()


@user_bp.route("/login", methods=["GET"])
def login():

    return controller.preparar_login()

@user_bp.route("/api/auth/login", methods=["POST"])
def login_api():
        return controller.login()



@user_bp.route("/sair", methods=["POST", "GET"])
def sair():
    return controller.encerrar()

@user_bp.route("/erro", methods=["POST", "GET"])
def erro():
    return controller.erro()

@user_bp.route("/admin", methods= ["POST", "GET"])
def admin():
    return controller.admin()



@user_bp.route("/apagar/<int:id>", methods=["POST"])
def excluir_user(id):
    return controller.remover_user(id)

@user_bp.route("/creditos")
def creditos():
    return controller.creditos()

@user_bp.route("/painel", methods=["POST", "GET"])
def painel():
    return controller.painel()

@user_bp.route("/api/painel", methods=["GET"])
def painel_api():

    return controller.painel_api()

@user_bp.route("/painel/remover/<int:id>", methods=["POST", "GET"])
def remover_user(id):
    return controller.remover_user(id)


@user_bp.route("/painel/editar/<int:id>", methods=["GET", "POST"])
def editar_user(id):
    if request.method == "POST":
        return controller.editar_user(id)
    return controller.preparar_edicao(id)

@user_bp.route("/admin/user", methods= ["GET","POST"])
def admin_user():
    return controller.admin_user()

@user_bp.route("/admin/user/promover/<int:id>", methods= ["GET","POST"])
def promover(id):
    return controller.promover(id)

@user_bp.route("/admin/user/rebaixar<int:id>", methods= ["GET","POST"])
def rebaixar(id):
    return controller.rebaixar(id)