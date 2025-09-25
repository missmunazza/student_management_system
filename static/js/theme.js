document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const btn = document.getElementById("theme-toggle-btn"); // matches base.html
  const icon = document.getElementById("theme-icon");

  // Apply saved theme on page load
  if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark");
    if (icon) {
      icon.classList.remove("bi-moon-stars-fill");
      icon.classList.add("bi-sun-fill");
    }
  }

  // Toggle theme on button click
  if (btn) {
    btn.addEventListener("click", () => {
      body.classList.toggle("dark");

      if (body.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        if (icon) {
          icon.classList.remove("bi-moon-stars-fill");
          icon.classList.add("bi-sun-fill");
        }
      } else {
        localStorage.setItem("theme", "light");
        if (icon) {
          icon.classList.remove("bi-sun-fill");
          icon.classList.add("bi-moon-stars-fill");
        }
      }
    });
  }
});
