document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("a[href='#aplicaciones']").addEventListener("click", function(event) {
        event.preventDefault(); // Evita el salto instantáneo
        document.querySelector("#aplicaciones").scrollIntoView({ behavior: "smooth" });
    });
});