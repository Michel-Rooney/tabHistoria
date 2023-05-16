


// Option to see password
const togglePasswordButton = document.getElementById("toggle-password");
const passwordInput = document.getElementById("password");

togglePasswordButton.addEventListener("click", () => {
const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
passwordInput.setAttribute("type", type);
togglePasswordButton.firstElementChild.classList.toggle("bi-eye");
togglePasswordButton.firstElementChild.classList.toggle("bi-eye-slash");
});
