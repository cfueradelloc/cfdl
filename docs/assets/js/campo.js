/* ============================================================================
   C.F.D.L. — campo.js
   «Ruido de fondo»: un campo de maleza generativo, ligero, sin p5. Partículas
   que siguen un campo de ruido y dejan trazo; el trazo se marchita despacio.
   Semilla distinta en cada visita, y se dice cuál.

   Uso: <canvas data-campo data-campo-tone="papel|zafiro"></canvas>
        <button data-campo-toggle>…</button>   (opcional)
        <span data-campo-seed></span>          (opcional)

   - Se detiene fuera de pantalla y con la pestaña oculta.
   - Con prefers-reduced-motion dibuja una sola imagen quieta y no anima.
   - El botón lo apaga; la preferencia se recuerda (localStorage, si hay).
   ========================================================================== */
(function () {
    "use strict";

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var KEY = "cfdl-campo";
    var store = {
        get: function () { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
        set: function (v) { try { localStorage.setItem(KEY, v); } catch (e) { /* sin almacenamiento */ } }
    };
    var enabled = store.get() !== "off";   // compartido: el botón apaga todos

  /* Un campo por lienzo, cada uno con su semilla. */
  function Campo(canvas) {
    var ctx = canvas.getContext("2d");

    /* ── Azar con semilla ──────────────────────────────────────────────── */
    var seed = Math.floor(Math.random() * 9000) + 1000;
    function mulberry32(a) {
        return function () {
            a |= 0; a = a + 0x6D2B79F5 | 0;
            var t = Math.imul(a ^ a >>> 15, 1 | a);
            t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
            return ((t ^ t >>> 14) >>> 0) / 4294967296;
        };
    }
    var rand = mulberry32(seed);

    /* Ruido de valor 3D (x, y, tiempo), suavizado. Basta y sobra. */
    var P = new Uint8Array(512);
    (function () {
        var p = [];
        for (var i = 0; i < 256; i++) p[i] = i;
        for (i = 255; i > 0; i--) { var j = Math.floor(rand() * (i + 1)); var t = p[i]; p[i] = p[j]; p[j] = t; }
        for (i = 0; i < 512; i++) P[i] = p[i & 255];
    })();
    function fade(t) { return t * t * (3 - 2 * t); }
    function lerp(a, b, t) { return a + (b - a) * t; }
    function h(x, y, z) { return P[P[P[x & 255] + (y & 255)] + (z & 255)] / 255; }
    function noise(x, y, z) {
        var xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z);
        var xf = fade(x - xi), yf = fade(y - yi), zf = fade(z - zi);
        return lerp(
            lerp(lerp(h(xi, yi, zi), h(xi + 1, yi, zi), xf), lerp(h(xi, yi + 1, zi), h(xi + 1, yi + 1, zi), xf), yf),
            lerp(lerp(h(xi, yi, zi + 1), h(xi + 1, yi, zi + 1), xf), lerp(h(xi, yi + 1, zi + 1), h(xi + 1, yi + 1, zi + 1), xf), yf),
            zf);
    }

    /* ── Paleta ────────────────────────────────────────────────────────── */
    var TONES = {
        papel:  { ink: "51,47,138",  inkA: 0.16, hot: "255,185,35", hotA: 0.55 },
        zafiro: { ink: "255,244,214", inkA: 0.10, hot: "255,185,35", hotA: 0.45 }
    };
    var tone = TONES[canvas.getAttribute("data-campo-tone")] || TONES.papel;

    /* ── Estado ────────────────────────────────────────────────────────── */
    var W = 0, H = 0, dpr = 1, parts = [], t = 0;
    var running = false, visible = true, raf = 0;
    var SCALE = 0.0021;   // tamaño de las matas
    var STEP = 1.1;       // velocidad

    function spawn(p) {
        p.x = rand() * W;
        p.y = rand() * H;
        p.life = 60 + rand() * 220;
        p.hot = rand() < 0.07;            // una de cada catorce, ámbar
        return p;
    }

    function size() {
        var r = canvas.getBoundingClientRect();
        dpr = Math.min(window.devicePixelRatio || 1, 1.5);
        W = Math.max(1, Math.round(r.width));
        H = Math.max(1, Math.round(r.height));
        canvas.width = Math.round(W * dpr);
        canvas.height = Math.round(H * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.lineWidth = 1;
        ctx.lineCap = "round";
        var n = Math.min(900, Math.round(W * H / 1800));
        parts = [];
        for (var i = 0; i < n; i++) parts.push(spawn({}));
    }

    function step(withFade) {
        if (withFade) {
            // El trazo se marchita: se borra un poco, nunca se repinta el fondo.
            ctx.globalCompositeOperation = "destination-out";
            ctx.fillStyle = "rgba(0,0,0,0.018)";
            ctx.fillRect(0, 0, W, H);
            ctx.globalCompositeOperation = "source-over";
        }
        t += 0.0016;
        ctx.beginPath();
        ctx.strokeStyle = "rgba(" + tone.ink + "," + tone.inkA + ")";
        var hot = [];
        for (var i = 0; i < parts.length; i++) {
            var p = parts[i];
            var a = noise(p.x * SCALE, p.y * SCALE, t) * Math.PI * 4;
            var nx = p.x + Math.cos(a) * STEP, ny = p.y + Math.sin(a) * STEP;
            if (p.hot) hot.push(p.x, p.y, nx, ny);
            else { ctx.moveTo(p.x, p.y); ctx.lineTo(nx, ny); }
            p.x = nx; p.y = ny;
            if (--p.life < 0 || nx < 0 || ny < 0 || nx > W || ny > H) spawn(p);
        }
        ctx.stroke();
        if (hot.length) {
            ctx.beginPath();
            ctx.strokeStyle = "rgba(" + tone.hot + "," + tone.hotA + ")";
            for (var k = 0; k < hot.length; k += 4) { ctx.moveTo(hot[k], hot[k + 1]); ctx.lineTo(hot[k + 2], hot[k + 3]); }
            ctx.stroke();
        }
    }

    function loop() {
        raf = 0;
        if (!running) return;
        step(true);
        raf = requestAnimationFrame(loop);
    }

    function still() {
        // Una imagen quieta: el mismo campo, sin movimiento.
        ctx.clearRect(0, 0, W, H);
        // Menos pasos que la versión viva: sin marchitarse, el trazo se acumula.
        for (var i = 0; i < 70; i++) step(false);
    }

    function sync() {
        var should = enabled && visible && !document.hidden && !reduce;
        if (should && !running) { running = true; raf = requestAnimationFrame(loop); }
        else if (!should && running) { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }
    }

    function render() {
        canvas.hidden = !enabled;
        if (!enabled) { ctx.clearRect(0, 0, W, H); sync(); return; }
        if (reduce) { still(); return; }
        // Arranca con algo ya crecido, para no abrir sobre el vacío.
        for (var i = 0; i < 90; i++) step(true);
        sync();
    }

    size();
    render();

    if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (e) {
            visible = e[0].isIntersecting;
            sync();
        }).observe(canvas);
    }
    document.addEventListener("visibilitychange", sync);

    var lastW = W, rt;
    window.addEventListener("resize", function () {
        clearTimeout(rt);
        rt = setTimeout(function () {
            var w = Math.round(canvas.getBoundingClientRect().width);
            if (w === lastW) return;   // la barra del móvil cambia la altura: se ignora
            lastW = w;
            size();
            render();
        }, 200);
    });

    return { seed: seed, render: render };
  }

    /* ── Arranque ──────────────────────────────────────────────────────── */
    var canvases = document.querySelectorAll("canvas[data-campo]");
    if (!canvases.length || !canvases[0].getContext) return;
    var campos = Array.prototype.map.call(canvases, function (c) { return Campo(c); });

    Array.prototype.forEach.call(document.querySelectorAll("[data-campo-seed]"), function (el) {
        el.textContent = String(campos[0].seed);
    });

    var toggle = document.querySelector("[data-campo-toggle]");
    if (toggle) {
        toggle.hidden = false;
        var label = function () {
            toggle.setAttribute("aria-pressed", String(enabled));
            toggle.textContent = enabled ? "ruido de fondo — sí" : "ruido de fondo — no";
        };
        label();
        toggle.addEventListener("click", function () {
            enabled = !enabled;
            store.set(enabled ? "on" : "off");
            label();
            campos.forEach(function (c) { c.render(); });
        });
    }
})();
