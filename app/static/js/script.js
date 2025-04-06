// Adicione esta função para verificar autenticação
async function checkAuth() {
    const protectedRoutes = ["/curso", "/estudante", "/professor", "/enrollments", "/report"];
    const currentPath = window.location.pathname;
    
    if (protectedRoutes.includes(currentPath)) {
        try {
            const response = await fetch("/api/auth/verify", {
                credentials: 'include'
            });
            
            if (!response.ok) {
                window.location.href = "/api/auth/login";
            }
        } catch (error) {
            window.location.href = "/api/auth/login";
        }
    }
}

// Adiciona token a todas as requisições
const originalFetch = window.fetch;
window.fetch = async function(url, options = {}) {
    const token = document.cookie.split('; ')
        .find(row => row.startsWith('access_token='))
        ?.split('=')[1];
    
    if (token) {
        options.headers = options.headers || {};
        options.headers["Authorization"] = `Bearer ${token}`;
    }
    return originalFetch(url, options);
};

// Verifica autenticação ao carregar a página
document.addEventListener("DOMContentLoaded", checkAuth);