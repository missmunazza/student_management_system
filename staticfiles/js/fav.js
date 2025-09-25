document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".fav-toggle").forEach(btn => {
      btn.addEventListener("click", () => {
        fetch(btn.dataset.url, {method: "POST", headers: {"X-CSRFToken": btn.dataset.csrf}})
          .then(res => res.json())
          .then(data => {
            if (data.status === "added") {
              btn.classList.add("btn-success");
              btn.classList.remove("btn-outline-success");
            } else {
              btn.classList.remove("btn-success");
              btn.classList.add("btn-outline-success");
            }
          });
      });
    });
  });
  