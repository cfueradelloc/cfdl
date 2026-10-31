/* ============================================================================
   C.F.D.L. — viewer.js
   El visor común de las piezas de output/. Se carga en el <head>, sin defer,
   para marcar <html class="visor"> antes de que p5 mida la ventana.

   - Pieza con lienzo (#canvas-container): el lienzo ocupa toda la pantalla;
     los controles pasan a un cajón (lateral en escritorio, hoja inferior en
     el móvil) que se abre con «Controles».
   - Pieza documento (paleta): sólo la barra superior.
   - La barra: volver al archivo, el título, «03 / 07», anterior y siguiente.
     Las flechas ← → del teclado también pasan de pieza (fuera de un control).
   Sin JS, cada pieza conserva su maquetación de siempre.
   ========================================================================== */
(function () {
    "use strict";

    var PIEZAS = [
        { href: "manifiesto-animado.html", t: "Manifiesto animado" },
        { href: "maleza.html",             t: "Maleza" },
        { href: "brujula.html",            t: "Brújula sin su imán" },
        { href: "moho.html",               t: "La llegada del moho" },
        { href: "disgregacion.html",       t: "Ante la síntesis, la disgregación" },
        { href: "garganta.html",           t: "Garganta sin fondo" },
        { href: "paleta.html",             t: "Paleta cromática" }
    ];

    var root = document.documentElement;
    root.classList.add("visor");

    function here() {
        var f = location.pathname.split("/").pop() || "";
        for (var i = 0; i < PIEZAS.length; i++) if (PIEZAS[i].href === f) return i;
        return -1;
    }

    function pad(n) { return (n < 10 ? "0" : "") + n; }

    function build() {
        var i = here();
        var hasCanvas = !!document.getElementById("canvas-container");
        root.classList.add(hasCanvas ? "visor-lienzo" : "visor-doc");

        var prev = PIEZAS[(i - 1 + PIEZAS.length) % PIEZAS.length];
        var next = PIEZAS[(i + 1) % PIEZAS.length];
        var title = i >= 0 ? PIEZAS[i].t : (document.querySelector(".sidebar h1") || {}).textContent || "";

        var bar = document.createElement("header");
        bar.className = "visor-bar";
        bar.innerHTML =
            '<a class="visor-back" href="../proyectos.html"><span aria-hidden="true">←</span> Archivo generativo</a>' +
            '<p class="visor-title"></p>' +
            '<nav class="visor-nav" aria-label="Piezas">' +
                (i >= 0 ? '<span class="visor-count">' + pad(i + 1) + ' / ' + pad(PIEZAS.length) + '</span>' : '') +
                '<a class="visor-step" rel="prev" href="' + prev.href + '" aria-label="Anterior: ' + prev.t + '">←</a>' +
                '<a class="visor-step" rel="next" href="' + next.href + '" aria-label="Siguiente: ' + next.t + '">→</a>' +
            '</nav>';
        bar.querySelector(".visor-title").textContent = title;
        document.body.insertBefore(bar, document.body.firstChild);

        if (hasCanvas) {
            var side = document.querySelector(".sidebar");
            if (side) {
                side.id = side.id || "visor-controles";
                var btn = document.createElement("button");
                btn.type = "button";
                btn.className = "visor-toggle";
                btn.textContent = "Controles";
                btn.setAttribute("aria-controls", side.id);
                btn.setAttribute("aria-expanded", "false");
                bar.querySelector(".visor-nav").appendChild(btn);

                var set = function (open) {
                    root.classList.toggle("visor-open", open);
                    btn.setAttribute("aria-expanded", String(open));
                    btn.textContent = open ? "Cerrar" : "Controles";
                };
                btn.addEventListener("click", function () {
                    set(!root.classList.contains("visor-open"));
                });
                document.addEventListener("keydown", function (e) {
                    if (e.key === "Escape" && root.classList.contains("visor-open")) { set(false); btn.focus(); }
                });
            }
        }

        // ← → pasan de pieza, salvo dentro de un control.
        document.addEventListener("keydown", function (e) {
            var t = e.target;
            if (e.altKey || e.ctrlKey || e.metaKey) return;
            if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT" || t.isContentEditable)) return;
            if (e.key === "ArrowLeft") location.href = prev.href;
            if (e.key === "ArrowRight") location.href = next.href;
        });
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
    else build();
})();
