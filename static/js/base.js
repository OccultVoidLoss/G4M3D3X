document.addEventListener("DOMContentLoaded", async (e) => {
    const token = localStorage.getItem("token")
    const painel = document.getElementById("painel")
    const login = document.getElementById("login")
    const cadastro = document.getElementById("cadastro")
    const admin = document.getElementById("admin")
    
    if (!token){
        painel.style.display = "none"
        cadastro.style.display = "block"
        login.style.display = "block"

        return
    }
    else{
        painel.style.display = "block"
        cadastro.style.display = "none"
        login.style.display = "none"
    }
    const resposta = await fetch("/api/painel", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
    const dados = await resposta.json()

    if (resposta.ok){

        if (dados.tipo == "admin"){
            admin.style.display = "block"
        }
        else{
            admin.style.display = "none"
        }
    }
    else{
        localStorage.removeItem("token")
        window.location.href = "/login"
    }

});