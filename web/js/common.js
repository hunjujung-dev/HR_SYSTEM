function getToken() {
    return localStorage.getItem("token") || "";
}

window.getToken = getToken;
