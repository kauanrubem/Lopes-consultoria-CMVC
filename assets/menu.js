document.addEventListener("click", function (event) {
  const sideMenu = document.getElementById("side-menu");
  const btnToggle = document.getElementById("btn-toggle-menu");

  if (!sideMenu || !btnToggle) return;

  const isClickInsideMenu = sideMenu.contains(event.target);
  const isClickOnButton = btnToggle.contains(event.target);

  if (!isClickInsideMenu && !isClickOnButton) {
    sideMenu.style.display = "none";
  }
});
