(function () {
  "use strict";

  const $ = (sel, scope) => (scope || document).querySelector(sel);
  const $$ = (sel, scope) => Array.from((scope || document).querySelectorAll(sel));
  const fineHover = matchMedia("(hover: hover) and (pointer: fine)").matches;

  function safe(fn, name) {
    try { fn(); } catch (e) { console.warn("[" + name + "]", e); }
  }

  // Menú móvil
  function initMenu() {
    const btn = $("[data-menu]");
    const nav = $("#nav-principal");
    if (!btn || !nav) return;
    btn.addEventListener("click", () => {
      const abierta = nav.classList.toggle("is-abierta");
      btn.setAttribute("aria-expanded", abierta ? "true" : "false");
    });
    nav.addEventListener("click", (e) => {
      if (e.target.closest("a")) {
        nav.classList.remove("is-abierta");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Desplazamiento suave a anclas, con margen para la cabecera fija
  function initAnclas() {
    document.addEventListener("click", (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute("href");
      if (!id || id === "#") return;
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      const top = el.getBoundingClientRect().top + scrollY - 72;
      window.scrollTo({
        top,
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
      });
    });
  }

  // Efecto imán: el botón sigue al ratón y vuelve solo
  function initIman() {
    if (!fineHover) return;
    $$("[data-iman]").forEach((el) => {
      if (el.dataset.imanListo) return;
      el.dataset.imanListo = "1";
      const fuerza = el.classList.contains("puerta") ? 0.08 : 0.28;
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const dx = e.clientX - (r.left + r.width / 2);
        const dy = e.clientY - (r.top + r.height / 2);
        el.style.transform = "translate(" + dx * fuerza + "px," + dy * fuerza + "px)";
      });
      el.addEventListener("mouseout", (e) => {
        if (el.contains(e.relatedTarget)) return;
        el.style.transform = "";
      });
    });
  }

  // Inclinación leve en las muestras
  function initTilt() {
    if (!fineHover) return;
    $$("[data-tilt] .muestra-img").forEach((el) => {
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(800px) rotateX(" + (-y * 6) + "deg) rotateY(" + (x * 6) + "deg)";
      });
      el.addEventListener("mouseout", (e) => {
        if (el.contains(e.relatedTarget)) return;
        el.style.transform = "";
      });
    });
  }

  // Revelado al entrar en pantalla, con red de seguridad
  function initReveal() {
    const items = $$("[data-reveal]");
    if (!items.length) return;
    if (!("IntersectionObserver" in window)) {
      items.forEach((el) => el.classList.add("is-visible"));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("is-visible");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.01, rootMargin: "0px 0px -2% 0px" });
    items.forEach((el) => io.observe(el));
    setTimeout(() => items.forEach((el) => el.classList.add("is-visible")), 6000);
  }

  // Modo claro / oscuro
  function initTema() {
    const btn = $("button[data-tema]");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const actual = document.documentElement.getAttribute("data-tema") === "oscuro" ? "oscuro" : "claro";
      const nuevo = actual === "oscuro" ? "claro" : "oscuro";
      document.documentElement.setAttribute("data-tema", nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) {}
    });
  }

  // Fotografía: fundido lento entre fotos de una misma serie
  function initSeries() {
    const series = $$("[data-serie]");
    if (!series.length) return;
    const lento = matchMedia("(prefers-reduced-motion: reduce)").matches;
    series.forEach((s) => {
      const imgs = $$(".serie-marco img", s);
      if (imgs.length < 2) return;
      let i = 0, timer = null;
      const paso = () => {
        imgs[i].classList.remove("is-on");
        i = (i + 1) % imgs.length;
        imgs[i].classList.add("is-on");
      };
      const iniciar = () => { if (!timer) timer = setInterval(paso, lento ? 7000 : 4200); };
      const parar = () => { clearInterval(timer); timer = null; };
      const desfase = parseInt(getComputedStyle(s).getPropertyValue("--desfase")) || 0;
      if ("IntersectionObserver" in window) {
        new IntersectionObserver((en) => en.forEach((x) => x.isIntersecting ? setTimeout(iniciar, desfase) : parar()), { threshold: 0.2 }).observe(s);
      } else {
        setTimeout(iniciar, desfase);
      }
      s.addEventListener("mouseover", (e) => { if (!s.contains(e.relatedTarget)) parar(); });
      s.addEventListener("mouseout", (e) => { if (!s.contains(e.relatedTarget)) iniciar(); });
    });
  }

  // Videos silenciosos: se reproducen al entrar en pantalla y se pausan al salir
  function initVideos() {
    const vids = $$("video[autoplay]");
    if (!vids.length || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        const v = en.target;
        if (en.isIntersecting) { const p = v.play(); if (p && p.catch) p.catch(() => {}); }
        else v.pause();
      });
    }, { threshold: 0.25 });
    vids.forEach((v) => io.observe(v));
  }

  // Plano en línea / a color: alterna solo cuando está en pantalla; el ratón o un toque lo detienen en la versión que se ve
  function initSwap() {
    const lento = matchMedia("(prefers-reduced-motion: reduce)").matches;
    $$("[data-swap]").forEach((el) => {
      let timer = null, fijo = false;
      const alternar = () => { if (!fijo) el.classList.toggle("is-color"); };
      const iniciar = () => { if (!timer) timer = setInterval(alternar, lento ? 6000 : 3200); };
      const parar = () => { clearInterval(timer); timer = null; };
      const enPantalla = () => {
        const r = el.getBoundingClientRect();
        const vis = Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0));
        return vis / Math.max(1, r.height) > 0.3;
      };
      const revisar = () => { enPantalla() ? iniciar() : parar(); };
      let esperando = false;
      window.addEventListener("scroll", () => { if (!esperando) { esperando = true; setTimeout(() => { esperando = false; revisar(); }, 120); } }, { passive: true });
      window.addEventListener("resize", revisar);
      setInterval(revisar, 1000);
      revisar();
      el.addEventListener("mouseover", (e) => { if (!el.contains(e.relatedTarget)) { fijo = true; el.classList.add("is-color"); } });
      el.addEventListener("mouseout", (e) => { if (!el.contains(e.relatedTarget)) { fijo = false; } });
      el.addEventListener("click", () => { fijo = !fijo; el.classList.toggle("is-color"); });
      el.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fijo = !fijo; el.classList.toggle("is-color"); } });
    });
  }

  // Rotación de láminas: alterna sola cuando está en pantalla; el ratón la detiene; un toque pasa a la siguiente
  function initRota() {
    const lento = matchMedia("(prefers-reduced-motion: reduce)").matches;
    $$("[data-rota]").forEach((el) => {
      const imgs = $$("img", el);
      if (imgs.length < 2) return;
      let i = 0, timer = null, quieto = false;
      const mostrar = (n) => { imgs[i].classList.remove("is-on"); i = (n + imgs.length) % imgs.length; imgs[i].classList.add("is-on"); };
      const paso = () => { if (!quieto) mostrar(i + 1); };
      const iniciar = () => { if (!timer) timer = setInterval(paso, lento ? 4000 : 1800); };
      const parar = () => { clearInterval(timer); timer = null; };
      const enPantalla = () => { const r = el.getBoundingClientRect(); const v = Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0)); return v / Math.max(1, r.height) > 0.3; };
      const revisar = () => { enPantalla() ? iniciar() : parar(); };
      let esperando = false;
      window.addEventListener("scroll", () => { if (!esperando) { esperando = true; setTimeout(() => { esperando = false; revisar(); }, 120); } }, { passive: true });
      window.addEventListener("resize", revisar);
      setInterval(revisar, 1000);
      revisar();
      el.addEventListener("mouseover", (e) => { if (!el.contains(e.relatedTarget)) quieto = true; });
      el.addEventListener("mouseout", (e) => { if (!el.contains(e.relatedTarget)) quieto = false; });
      el.addEventListener("click", () => mostrar(i + 1));
      el.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); mostrar(i + 1); } });
    });
  }

  // Correo: en vez de depender del programa de correo (que muchos no tienen),
  // abre un cuadro con la dirección copiada y tres formas de escribir
  function initCorreo() {
    const els = $$("[data-correo]");
    if (!els.length) return;
    let caja = null;
    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
    const cerrar = () => { if (caja) { caja.classList.remove("is-on"); document.documentElement.classList.remove("con-caja"); } };
    const abrir = (el) => {
      const d = el.dataset, correo = d.correo, asunto = d.asunto || "";
      const q = encodeURIComponent;
      const gmail = "https://mail.google.com/mail/?view=cm&fs=1&to=" + q(correo) + "&su=" + q(asunto);
      const outlook = "https://outlook.office.com/mail/deeplink/compose?to=" + q(correo) + "&subject=" + q(asunto);
      const mailto = "mailto:" + correo + "?subject=" + q(asunto);
      if (!caja) {
        caja = document.createElement("div");
        caja.className = "correo-caja";
        caja.setAttribute("role", "dialog");
        caja.setAttribute("aria-modal", "true");
        document.body.appendChild(caja);
        caja.addEventListener("click", (e) => { if (e.target === caja || e.target.closest("[data-cerrar]")) cerrar(); });
        document.addEventListener("keydown", (e) => { if (e.key === "Escape") cerrar(); });
      }
      caja.innerHTML =
        '<div class="correo-panel">' +
        '<p class="mono correo-titulo">' + esc(d.lTitulo) + '</p>' +
        '<button type="button" class="correo-dir" data-copiar>' + esc(correo) + '</button>' +
        '<p class="mono correo-estado" aria-live="polite"></p>' +
        '<div class="correo-opciones">' +
        '<a class="btn btn-borde" href="' + gmail + '" target="_blank" rel="noopener">' + esc(d.lGmail) + '</a>' +
        '<a class="btn btn-borde" href="' + outlook + '" target="_blank" rel="noopener">' + esc(d.lOutlook) + '</a>' +
        '<a class="btn btn-borde" href="' + mailto + '">' + esc(d.lApp) + '</a>' +
        '</div>' +
        '<button type="button" class="correo-cerrar mono" data-cerrar>' + esc(d.lCerrar) + '</button>' +
        '</div>';
      const estado = $(".correo-estado", caja);
      const copiar = () => {
        const done = () => { estado.textContent = d.lCopiado; };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(correo).then(done).catch(() => { estado.textContent = d.lCopiar + ": " + correo; });
        else { estado.textContent = correo; }
      };
      $(".correo-dir", caja).addEventListener("click", copiar);
      copiar();
      caja.classList.add("is-on");
      document.documentElement.classList.add("con-caja");
      $(".correo-dir", caja).focus();
    };
    els.forEach((el) => el.addEventListener("click", (e) => { e.preventDefault(); abrir(el); }));
  }

  function boot() {
    safe(initCorreo, "initCorreo");
    safe(initRota, "initRota");
    safe(initSwap, "initSwap");
    safe(initVideos, "initVideos");
    safe(initSeries, "initSeries");
    safe(initTema, "initTema");
    document.documentElement.classList.add("js");
    safe(initMenu, "initMenu");
    safe(initAnclas, "initAnclas");
    safe(initIman, "initIman");
    safe(initTilt, "initTilt");
    safe(initReveal, "initReveal");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
