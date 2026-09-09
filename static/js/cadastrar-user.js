
document.getElementById("form").addEventListener("submit", async (e) =>{
    e.preventDefault()
    let div_mensagem = document.getElementById("mensagem")
    let nome = document.getElementById("nome").value
    let tipo = document.getElementById("tipo").value
    let senha = document.getElementById("senha").value
    let email = document.getElementById("email").value
    let aut = document.getElementById("aut").value
    if (tipo == "admin" && aut != "root"){
        div_mensagem.classList.remove("alert", "alert-success")
        div_mensagem.classList.add("alert", "alert-danger")
        div_mensagem.textContent = "Permissão negada!"
        return
    }
    const corpo = {
                nome : nome,
                email : email,
                senha : senha,
                tipo : tipo,
                aut : aut
            }
    let res_cadastrar = await fetch("/api/auth/registro", {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify(corpo)
    })
    if (!res_cadastrar.ok){
        div_mensagem.classList.remove("alert", "alert-success")
        div_mensagem.classList.add("alert", "alert-danger")
    }
    else{
        div_mensagem.classList.remove("alert", "alert-danger")
        div_mensagem.classList.add("alert", "alert-success")
    }
        let data_cadastrar = await res_cadastrar.json()
        div_mensagem.textContent = data_cadastrar.mensagem
})