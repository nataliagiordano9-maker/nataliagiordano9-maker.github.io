(function () {
  try {
    var t = localStorage.getItem("tema");
    if (!t) { t = matchMedia("(prefers-color-scheme: dark)").matches ? "oscuro" : "claro"; }
    document.documentElement.setAttribute("data-tema", t);
  } catch (e) {}
})();
