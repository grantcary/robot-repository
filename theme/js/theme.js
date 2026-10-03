/* Dark mode toggle. The site works without this file: the CSS follows the
   OS light/dark setting on its own. This only adds the sidebar button and
   remembers the visitor's choice across pages. Loaded in <head> so the saved
   theme is applied before the page paints. */
(function () {
  var root = document.documentElement;
  var dark = window.matchMedia("(prefers-color-scheme: dark)");

  function saved() {
    try { return localStorage.getItem("theme"); } catch (e) { return null; }
  }

  function current() {
    return root.getAttribute("data-theme") || (dark.matches ? "dark" : "light");
  }

  var theme = saved();
  if (theme === "dark" || theme === "light") root.setAttribute("data-theme", theme);

  document.addEventListener("DOMContentLoaded", function () {
    // one toggle in the sidebar nav, one in the small-screen menu
    var buttons = document.querySelectorAll(".theme-toggle");

    function label() {
      var text = current() === "dark" ? "Light mode" : "Dark mode";
      buttons.forEach(function (b) { b.textContent = text; });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var next = current() === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        try { localStorage.setItem("theme", next); } catch (e) {}
        label();
      });
      button.hidden = false;
    });
    dark.addEventListener("change", label);
    label();
  });
})();
