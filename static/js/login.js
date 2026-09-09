
document.getElementById("form").addEventListener("submit", async (e) =>{
    e.preventDefault()
    let div_mensagem = document.getElementById("mensagem")
    let senha = document.getElementById("senha").value
    let email = document.getElementById("email").value
    const corpo = {
                email : email,
                senha : senha
            }
    let res_login = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify(corpo)
    })
    if (!res_login.ok){
        div_mensagem.classList.remove("alert", "alert-success")
        div_mensagem.classList.add("alert", "alert-danger")
    }
    else{
        div_mensagem.classList.remove("alert", "alert-danger")
        div_mensagem.classList.add("alert", "alert-success")
    }
        let data_login = await res_login.json()
        div_mensagem.textContent = data_login.mensagem
        localStorage.setItem("token", data_login.token)

        window.location.href = "/"
})