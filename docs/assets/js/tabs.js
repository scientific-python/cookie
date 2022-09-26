function openTab(tabName) {
  var tab = document.getElementsByClassName("skhep-tab");
  for (const t of tab) {
    t.style.display = t.classList.contains(`${tabName}-tab`) ? "block" : "none";
  }
  var btn = document.getElementsByClassName("skhep-bar-item");
  for (const b of btn) {
    if (b.classList.contains(`${tabName}-btn`)) b.classList.add("btn-purple");
    else b.classList.remove("btn-purple");
  }
}
function ready() {
  const urlParams = new URLSearchParams(window.location.search);
  const tabs = urlParams.getAll("tabs");

  for (const tab of tabs) {
    openTab(tab);
  }
}

document.addEventListener("DOMContentLoaded", ready, false);
