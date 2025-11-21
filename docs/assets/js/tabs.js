function openTab(tabName, groupName = 'default') {
  var tab = document.getElementsByClassName("skhep-tab");
  for (const t of tab) {
    if (t.classList.contains(`${groupName}-${tabName}-tab`)) {
      t.style.display = "block";
    } else if (Array.from(t.classList).some(c => c.startsWith(`${groupName}-`) && c.endsWith('-tab'))) {
      t.style.display = "none";
    }
  }
  var btn = document.getElementsByClassName("skhep-bar-item");
  for (const b of btn) {
    if (b.classList.contains(`${groupName}-${tabName}-btn`)) {
      b.classList.add("btn-purple");
    } else if (Array.from(b.classList).some(c => c.startsWith(`${groupName}-`) && c.endsWith('-btn'))) {
      b.classList.remove("btn-purple");
    }
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
