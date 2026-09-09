from flask import request
from . import categorias_bp
from .controllers import CategoriaController

controller = CategoriaController()

@categorias_bp.route("/categorias")
def listar_categorias():
    return controller.listar_categorias()

@categorias_bp.route("/categorias/cadastrar", methods=["GET","POST"])
def cadastrar_categoria():
    if request.method == "POST":
        return controller.cadastrar_categoria()
    
    return controller.preparar_cadastro()

@categorias_bp.route("/editar_categoria/<int:id>", methods=["GET", "POST"])
def editar_categoria(id):

    if request.method == "POST":
        return controller.editar_categoria(id)

    return controller.preparar_edicao(id)

@categorias_bp.route("/excluir_categoria/<int:id>", methods=["POST"])
def excluir_categoria(id):
    return controller.remover_categoria(id) 



