document.addEventListener("DOMContentLoaded", async (e) => {
    const email = document.getElementById("email")
    const nome = document.getElementById("nome")
    const token = localStorage.getItem("token")
    console.log("TOKEN:", token);

    const resposta = await fetch("/api/painel", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
    const dados = await resposta.json()
    nome.textContent = dados.nome
    email.textContent = dados.email

    console.log("DADOS:", dados);
    
    document.getElementById("sair").addEventListener("click", async (e) => {
        localStorage.removeItem("token")
        window.location.href = "/login"
    })
});