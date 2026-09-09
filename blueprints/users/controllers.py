from flask import render_template, request, redirect, url_for, flash, session, jsonify, current_app
from .dao import UserDAO
from .models import User, Comum, Admin
import bcrypt
from datetime import datetime, timedelta, timezone
import jwt

class UserController:

    def __init__(self):
        self.__dao = UserDAO()


    # CADASTRAR
    def cadastrar_user(self):
        dados = request.get_json()
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha = bcrypt.hashpw(bytes, salt)
        tipo = dados.get("tipo")
        usuarios = self.__dao.carregar_user()

        if not email or not senha or not nome:
            return jsonify({"Erro": "Todos os campos são obrigatórios"}), 400
        
        for user in usuarios:
            if user.email == email:
                return jsonify({"Erro": "Email já existente"}), 400

        try:
            if tipo == "comum":
                novo_user = Comum(
                    nome,
                    email,
                    senha
                )
                self.__dao.salvar_user(novo_user,tipo)
            else:
                autorizacao = dados.get("aut")
                if autorizacao == "root":
                    novo_user = Admin(
                        nome,
                        email,
                        senha
                    )
                    self.__dao.salvar_user(novo_user, tipo)
                else:
                    return jsonify({"Erro": "Permissão Negada"}), 400  
            return jsonify({"mensagem": f"o user '{nome}' foi cadastrado"}), 200

        except Exception as e:
            return jsonify({"Erro": "Falha ao cadastrar"}), 400

        
    def preparar_cadastro(self):
        return render_template("users/cadastro.html")


    def index(self):
        return render_template("index.html")
    
    def login(self):
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")
        if not email or not senha:
            return jsonify({"Erro": "Todos os campos são obrigatórios"}), 400
        users = self.__dao.carregar_user()
        for user in users:
            senha_status = bcrypt.checkpw(senha.encode('utf-8'), user.senha.encode('utf-8'),)
            if user.email == email and senha_status == True:
                        payload = {
                            "sub": str(user.id),
                            "exp": datetime.now(timezone.utc) + timedelta(hours = 4),
                        }
                        token = jwt.encode(
                            payload,
                            current_app.config["JWT_SECRET"],
                            algorithm="HS256"
                        )

                        return jsonify({"mensagem": f"Logado como user {email}",
                                        "token": token}), 200
        return jsonify({"Erro": "Falha ao logar"}), 400
        
    def preparar_login(self):
        return render_template("users/login.html")
    
    def encerrar(self):
        session.pop('usuario', None)
        session.pop('admin', None)
        return redirect(url_for("user.index"))


    def erro(self):
        return render_template("erro.html")

    #REMOVER
    def remover_user(self, id):
        self.__dao.remover_user(id)
        flash("Sucesso: User removido com sucesso!", "success")
        if (session.get("admin") and id != session.get("user_id")):
            return redirect(url_for("user.admin_user"))
        else:
            return self.encerrar()
    def admin(self):
        if not session.get("admin"):
            flash("Acesso negado", "danger")
            return redirect(url_for("user.erro"))
        return render_template("admin/admin.html")
    
    def creditos(self):
        return render_template("creditos.html")
    
    def painel(self):
            return render_template("users/painel.html")
    
    def painel_api(self):
        auth = request.headers.get("Authorization")

        if not auth:
            return jsonify({"Erro": "Token inválido"}), 401

        try:
            token = auth.split(" ")[1]


            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )


            user_id = int(payload["sub"])


            user = self.__dao.buscar_user_por_id(user_id)


            if not user:
                return jsonify({"Erro": "Usuário não encontrado"}), 404

            return jsonify(user.to_dict()), 200

        except jwt.InvalidTokenError:
            return jsonify({"Erro": "Token inválido"}), 401

    def preparar_edicao(self,id):
        user = self.__dao.buscar_user_por_id(id)
        return render_template("users/editar.html")

    def editar_user(self, id):
        dados = request.get_json()
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        tipo = session.get("Admin")
        bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha = bcrypt.hashpw(bytes, salt)

        try:
            if tipo == "False":
                user_att = Comum(
                nome,
                email,
                senha,
                id
                )
            else:
                user_att = Admin(
                    nome,
                    email,
                    senha,
                    id
                )
            session["usuario"] = user_att.nome
            self.__dao.editar_user(user_att)
            return render_template("users/painel.html", user = user_att)
        except Exception as e:
            flash(f"Erro ao atualizar user: {str(e)}", "danger")
            return redirect(url_for("user.editar_user", id=id))

    def admin_user(self):
        users = self.__dao.carregar_user()
        return render_template("admin/usuarios.html", users=users)
    
    def promover(self, id):
        self.__dao.promover(id)
        return redirect(url_for("user.admin_user"))
    
    def rebaixar(self,id):
        self.__dao.rebaixar(id)
        return redirect(url_for("user.admin_user"))
