/* ============================================================================
   C.F.D.L. — site.js
   Shared behaviour for the top-level pages. Plain JS, no build, loaded with
   `defer`. Every page must remain fully usable without it.
   ========================================================================== */
(function () {
    "use strict";

    var root = document.documentElement;
    root.classList.add("js");

    // Hoy, en hora local, como AAAA-MM-DD (comparable con data-date).
    function today() {
        var d = new Date();
        return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") +
            "-" + String(d.getDate()).padStart(2, "0");
    }

    /* ── Menú a pantalla completa ───────────────────────────────────────── */
    /* Se construye a partir de .nav-links, así el marcado de las cinco
       páginas no se duplica. */
    function buildMenu() {
        var nav = document.querySelector(".site-nav");
        var links = nav && nav.querySelector(".nav-links");
        if (!links || typeof HTMLDialogElement === "undefined") {
            root.classList.remove("js");   // sin <dialog>: la barra envuelve
            return;
        }

        var toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "nav-toggle";
        toggle.textContent = "Menú";
        toggle.setAttribute("aria-haspopup", "dialog");
        toggle.setAttribute("aria-expanded", "false");
        nav.appendChild(toggle);

        var menu = document.createElement("dialog");
        menu.className = "menu";
        menu.setAttribute("aria-label", "Menú");

        var head = document.createElement("div");
        head.className = "menu-head";
        var brand = nav.querySelector(".nav-brand").cloneNode(true);
        var close = document.createElement("button");
        close.type = "button";
        close.className = "menu-close";
        close.textContent = "Cerrar";
        close.autofocus = true;
        head.appendChild(brand);
        head.appendChild(close);

        var list = document.createElement("ul");
        list.className = "menu-links";
        var foot = document.createElement("div");
        foot.className = "menu-foot";
        var sign = document.createElement("span");
        sign.textContent = "Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc";
        foot.appendChild(sign);

        Array.prototype.forEach.call(links.querySelectorAll("a"), function (a) {
            var c = a.cloneNode(true);
            c.removeAttribute("class");
            if (/^https?:/.test(a.getAttribute("href"))) {
                foot.appendChild(c);            // Instagram → al pie
            } else {
                var li = document.createElement("li");
                li.appendChild(c);
                list.appendChild(li);
            }
        });

        menu.appendChild(head);
        menu.appendChild(list);
        menu.appendChild(foot);
        document.body.appendChild(menu);

        function open() {
            menu.showModal();
            toggle.setAttribute("aria-expanded", "true");
            root.style.overflow = "hidden";
        }
        function shut() { menu.close(); }

        toggle.addEventListener("click", open);
        close.addEventListener("click", shut);
        menu.addEventListener("close", function () {
            toggle.setAttribute("aria-expanded", "false");
            root.style.overflow = "";
            toggle.focus();
        });
        // Al volver a escritorio con el menú abierto, se cierra solo.
        var wide = window.matchMedia("(min-width: 761px)");
        var onWide = function () { if (wide.matches && menu.open) shut(); };
        if (wide.addEventListener) wide.addEventListener("change", onWide);
    }

    /* ── Eventos: próximos / pasados según la fecha de hoy ──────────────── */
    /* Cada <li class="event-item"> lleva data-date="AAAA-MM-DD" (orden) y,
       si dura varios días, data-end (el último, que decide si ya pasó). El reparto escrito a mano en el HTML es el respaldo
       sin JS; aquí se rehace con la fecha real, para que no envejezca. */
    function splitEvents() {
        var upcoming = document.querySelector("[data-events='upcoming']");
        var past = document.querySelector("[data-events='past']");
        if (!upcoming || !past) return;

        var now = today();

        var items = Array.prototype.slice.call(
            document.querySelectorAll(".event-item[data-date]"));
        var up = [], down = [];
        items.forEach(function (li) {
            ((li.dataset.end || li.dataset.date) >= now ? up : down).push(li);
        });
        up.sort(function (a, b) { return a.dataset.date < b.dataset.date ? -1 : 1; });
        down.sort(function (a, b) { return a.dataset.date > b.dataset.date ? -1 : 1; });

        up.forEach(function (li) { li.classList.remove("past"); upcoming.appendChild(li); });
        down.forEach(function (li) { li.classList.add("past"); past.appendChild(li); });

        var empty = document.querySelector(".event-empty");
        if (empty) empty.hidden = up.length > 0;
    }

    /* ── Portada: el próximo encuentro (o el último) ────────────────────── */
    /* Lee eventos.html —la página que ya es la representación del calendario—
       y rellena [data-proximo]. El marcado estático trae el último conocido. */
    function fillProximo() {
        var box = document.querySelector("[data-proximo]");
        if (!box || !window.fetch || !window.DOMParser) return;
        fetch("eventos.html").then(function (r) { return r.ok ? r.text() : null; }).then(function (html) {
            if (!html) return;
            var doc = new DOMParser().parseFromString(html, "text/html");
            var items = Array.prototype.slice.call(doc.querySelectorAll(".event-item[data-date]"));
            if (!items.length) return;
            var now = today();
            var up = items.filter(function (li) { return (li.dataset.end || li.dataset.date) >= now; })
                .sort(function (a, b) { return a.dataset.date < b.dataset.date ? -1 : 1; });
            var past = items.filter(function (li) { return (li.dataset.end || li.dataset.date) < now; })
                .sort(function (a, b) { return a.dataset.date > b.dataset.date ? -1 : 1; });
            var li = up[0] || past[0];
            var txt = function (sel) { var n = li.querySelector(sel); return n ? n.textContent.trim() : ""; };
            var set = function (sel, v) { var n = box.querySelector(sel); if (n) n.textContent = v; };
            set("[data-p-label]", up.length ? "Próximo" : "Último encuentro");
            set("[data-p-day]", txt(".event-month"));
            set("[data-p-month]", txt(".event-year"));
            set("[data-p-title]", txt(".event-title"));
            set("[data-p-meta]", txt(".event-meta"));
            box.classList.toggle("is-next", up.length > 0);
        }).catch(function () { /* sin red o desde file://: queda lo estático */ });
    }

    buildMenu();
    splitEvents();
    fillProximo();
})();
