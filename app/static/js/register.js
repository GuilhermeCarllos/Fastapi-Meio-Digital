document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Salva o token no localStorage
            localStorage.setItem("token", data.access_token);
            // Redireciona para a página de login ou dashboard
            window.location.href = "/api/auth/login";
        } else {
            alert(data.detail || "Erro ao cadastrar");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao cadastrar");
    }
});