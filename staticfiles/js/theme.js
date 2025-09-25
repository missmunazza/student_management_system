document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const btn = document.getElementById("theme-toggle");
  
    if (localStorage.getItem("theme") === "dark") {
      body.classList.add("dark");
    }
  
    btn.addEventListener("click", () => {
      body.classList.toggle("dark");
      localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
    });
  });
  