# -*- coding: utf-8 -*-
"""Genera index.html + tecnica.html + marca.html + hosteleria.html
desde un solo origen de datos. Ejecutar: python tools/build.py
"""
import os, sys, html, datetime, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from traducciones import TR, MESES as MESES_IDIOMA

LANG = "es"      # idioma de la página que se está generando
BASE = ""        # prefijo de rutas ("" en la raíz, "../" dentro de en/ e it/)
IDIOMAS_SITIO = [("es", "ES", ""), ("en", "EN", "en/"), ("it", "IT", "it/")]

def t(s):
    """Traduce un texto al idioma actual; si no hay traducción, deja el español."""
    return TR.get(LANG, {}).get(s, s)

def A(ruta):
    """Ruta a un recurso compartido (assets, css, js) desde la página actual."""
    return BASE + ruta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = datetime.date.today().strftime("%Y%m%d")

NOMBRE = "Natalia Giordano"
EMAIL = "nataliagiordano9@gmail.com"
WHATSAPP = "34610080434"
WHATSAPP_VISIBLE = "+34 610 080 434"
CIUDAD = "Valencia, España"

# ---------------------------------------------------------------- puertas
PUERTAS = {
    "tecnica": dict(
        archivo="tecnica.html",
        nav="Técnica de proyectos",
        titulo="Cálculo, presupuesto y dibujo.",
        linea="Ingeniera civil como asistente técnica o colaboradora en estudios y empresas: cómputos, presupuestos, dibujo y documentación de proyecto. Me integro rápido a un equipo y trabajo con orden.",
        disponible="Disponibilidad inmediata · presencial en Valencia o en remoto desde cualquier lugar",
        cv="assets/cv/natalia-giordano-cv-tecnica.pdf",
        asunto="Técnica de proyectos",
        pilares=[
            ("Cómputos y presupuestos", "Mediciones, cuantificación y presupuesto de proyecto, con documentación clara y ordenada."),
            ("Dibujo técnico", "Plantas, cortes, alzados y detalles en AutoCAD. Modelado 3D en SketchUp y Revit."),
            ("Documentación de proyecto", "Organización de la información técnica, relevamientos, memorias y material gráfico para presentar."),
        ],
        muestras=[
            ("Plantas, corte y axonometría · de la línea al collage", "rota:tec-plantas-linea-h,tec-plantas-color-h,tec-axonometria-h", "", "fila"),
            ("Vestidor · alzado interior", "tec-vestidor", "", "par"),
            ("Interior · línea", "tec-interior", "", "par"),
        ],
        muestras_titulo="Muestras de trabajo.",
        etiqueta_sector="tecnica",
    ),
    "marca": dict(
        archivo="marca.html",
        nav="Diseño de marca",
        titulo="Pienso la marca y la dibujo.",
        linea="Diseñadora de marca desde 2018. Identidad visual, manuales, aplicaciones y, cuando el proyecto lo pide, escenas del espacio en arte digital y motion.",
        disponible="Disponibilidad inmediata · presencial en Valencia o en remoto desde cualquier lugar",
        cv="assets/cv/natalia-giordano-cv-marca.pdf",
        asunto="Diseño de marca",
        pilares=[
            ("La marca", "Pienso el concepto y dibujo el logotipo, el sistema de color y la tipografía."),
            ("Las aplicaciones", "Manual de marca, envases y etiquetas, piezas para redes, cartelería y material corporativo."),
            ("El espacio", "Visualizaciones de la marca en su lugar: arte digital y motion sobre escenas arquitectónicas."),
        ],
        muestras=[
            ("Textura de la selva · pieza del collage", "marca-selva", ""),
            ("Escena animada · escritorio", "video:escena-escritorio", "marca-escena-cartel"),
            ("Proceso · tableta", "marca-wacom", ""),
            ("Paleta de materiales", "marca-materiales", ""),
            ("Escena del espacio · cocina", "marca-escena-cocina-foto", ""),
            ("Escena animada · cocina", "video:escena-cocina", "marca-escena-cocina"),
            ("Escena del espacio · baño", "marca-escena-bano", ""),
            ("Collage de objetos y materiales", "video:collage-objetos", "marca-collage-cartel"),
        ],
        muestras_titulo="Proyectos.",
        etiqueta_sector="marca",
    ),
    "hosteleria": dict(
        archivo="hosteleria.html",
        nav="Hostelería y ventas",
        titulo="Trabajo donde haga falta.",
        linea="Housekeeper en hoteles, catering assistant en eventos, dishwasher en restaurantes y sales assistant en tienda. Temporadas de verano e invierno en Italia, Australia y España.<br>Espero que mi experiencia sea útil para tu equipo.",
        disponible="Disponibilidad inmediata · España (incluidas las islas), Italia, Suiza, Noruega, Islandia y Países Bajos",
        cv="assets/cv/natalia-giordano-cv-hosteleria.pdf",
        asunto="Hostelería y ventas",
        pilares=[
            ("Housekeeping", "Camarera de pisos en hotel boutique, limpieza residencial y comercial, mantenimiento de áreas comunes."),
            ("Cocina y eventos", "Lavaplatos y auxiliar de cocina en ritmo alto. Preparación y servicio en eventos de catering."),
            ("Sales assistant / retail", "Asesoramiento, reposición, gestión de stock con PDA y visual merchandising en Zara Home."),
        ],
        muestras=None,
        muestras_titulo=None,
        etiqueta_sector="hosteleria",
    ),
}

ORDEN_PUERTAS = ["tecnica", "marca", "hosteleria"]

# --------------------------------------------------------- línea de tiempo
# (inicio, fin, sector, lugar, puesto, empresa, tareas)
TIMELINE = [
    ("2026-04", "2026-05", "hosteleria", "Valencia, España", "Dependienta y asesora de ventas", "Zara Home",
     "Atención al cliente, reposición, gestión de stock con PDA, visual merchandising."),
    ("2025-10", "2026-01", "viaje", "Córdoba, Argentina", "Estancia en Argentina", "Familia y viaje",
     "Entre la temporada de Australia y la de Italia."),
    ("2026-01", "2026-03", "hosteleria", "Passo del Tonale, Italia", "Polivalente de hotel · housekeeping", "La Torretta Wellness",
     "Temporada de invierno: habitaciones y zonas comunes, spa y gimnasio, sala de esquís y lavandería."),
    ("2025-06", "2025-07", "hosteleria", "Magnetic Island, Australia", "Voluntaria", "Proyecto MINCA y casa de familia",
     "Conservación de flora nativa, mantenimiento ambiental y apoyo doméstico."),
    ("2025-06", "2025-06", "hosteleria", "Cape Tribulation, Australia", "Polivalente", "Cape Trib Farm",
     "Limpieza, mantenimiento general y apoyo en visitas guiadas de fruta tropical."),
    ("2025-04", "2025-06", "hosteleria", "Ravenshoe, Australia", "Polivalente de hotel", "Ravenshoe Hotel",
     "Limpieza, ayuda en cocina y tareas generales del hotel. Voluntariado en casa de familia en paralelo."),
    ("2025-03", "2025-04", "hosteleria", "Byron Bay, Australia", "Auxiliar de catering", "Spanish Catering",
     "Montaje de eventos, servicio y atención al público."),
    ("2024-10", "2025-02", "hosteleria", "Sídney, Australia", "Auxiliar de limpieza", "No Sweat Cleaning",
     "Limpieza residencial y comercial, trabajo autónomo con estándares de calidad."),
    ("2024-08", "2024-10", "hosteleria", "Sicilia, Italia", "Lavaplatos y apoyo de sala", "Sabbinirica Bistrot",
     "Apoyo general de restaurante."),
    ("2024-07", "2024-09", "hosteleria", "Sicilia, Italia", "Camarera de pisos", "La Dependance Hotel",
     "Limpieza y preparación de habitaciones y áreas comunes en hotel boutique."),
    ("2024-04", "2024-08", "hosteleria", "Sicilia, Italia", "Lavaplatos y auxiliar de cocina", "Fontana D'Ercole",
     "Cocina en ritmo alto, coordinación con el equipo."),
    ("2023-11", "2024-05", "tecnica", "Italia · remoto", "Técnica de proyectos arquitectónicos", "INGEC Studio",
     "Cómputos, presupuestos y documentación de proyecto. Relevamientos, modelado 3D y material gráfico. Apoyo a la dirección del estudio."),
    ("2021-01", "2022-01", "tecnica", "Córdoba, Argentina", "Diseñadora de proyectos arquitectónicos", "Área Arquitectura + Diseño",
     "Propuestas espaciales y tipológicas, apoyo técnico para la viabilidad, documentación y material gráfico."),
    ("2020-01", "2022-02", "marca", "Colombia · remoto", "Diseñadora gráfica", "Itseil",
     "Contenido para campañas digitales y redes, adaptación de identidades para distintas marcas."),
    ("2018-06", None, "marca", "Remoto", "Diseñadora de marca independiente", "Clientes propios",
     "Identidades visuales, logotipos, manuales de marca, editorial, envases y etiquetas. Gestión completa del proyecto con el cliente."),
    ("2013-03", "2023-09", "formacion", "Córdoba, Argentina", "Ingeniería Civil", "UTN · Facultad Regional Córdoba",
     "Título de Ingeniera Civil."),
    ("2007-03", "2012-12", "formacion", "Argentina", "Bachiller en Economía y Gestión de las Organizaciones", "Instituto Secundario Dr. Raúl Loza",
     ""),
]

MESES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

def fecha(s):
    if s is None:
        return t("hoy")
    a, m = s.split("-")
    return f"{MESES_IDIOMA[LANG][int(m)]} {a}"

SECTOR_NOMBRE = {"tecnica": "Técnica", "marca": "Marca", "hosteleria": "Hostelería", "formacion": "Formación", "viaje": "Viaje"}

HERRAMIENTAS = [
    ("Técnica", ["AutoCAD", "SketchUp", "Revit", "Excel"]),
    ("Diseño", ["Illustrator", "Photoshop", "InDesign", "After Effects", "Lightroom", "Canva"]),
    ("Oficina", ["Microsoft Office", "Google Workspace (Meet, Drive, Docs)"]),
    ("Inteligencia artificial", ["Claude Code", "ChatGPT", "Midjourney"]),
]

IDIOMAS = [("Español", "Nativo"), ("Italiano", "B1"), ("Inglés", "A2")]

FICHA = [
    ("Ciudadanía", "Italiana y argentina. Permiso de trabajo en toda la Unión Europea."),
    ("Carnet de conducir", "No."),
]


PRESENTACION = [
    "Gracias por llegar hasta aquí.",
    "Durante mucho tiempo pensé que tenía que elegir entre el cálculo y el dibujo. Estudié ingeniería, y mientras tanto aprendí diseño por mi cuenta, proyecto a proyecto, desde 2018. Con los años entendí que no eran dos caminos: la ingeniería me enseñó responsabilidad y constancia, a medir antes de opinar y a documentar bien; el diseño, a mirar cómo se siente un lugar y a escuchar lo que alguien necesita antes de dibujarlo. Hoy trabajo con las dos cosas a la vez.",
    "Los últimos años fueron de viaje y de trabajo. Trabajé de manera independiente y en estudios con equipos grandes dentro de mi profesión; también fui ayudante de cocina, hice camas en hoteles, lavé platos en restaurantes y serví eventos grandes en Italia y pequeños en Australia. Eso me enseñó lo que vale llegar a tiempo, hacer bien lo que toca y cuidar a la persona que tienes delante. También a trabajar codo a codo con gente de todas partes, a no perder la calma cuando el ritmo aprieta y, de paso, a cocinar mucho mejor.",
    "Me gusta preguntar mucho antes de empezar y explicar el porqué de cada decisión.",
    "Viajo desde que terminé la carrera y la curiosidad no se me ha pasado: ya son casi veinte países, algunos apenas de paso. Por eso llevo a todas partes una cámara de segunda mano: para retratar lo que no quiero olvidar.",
    "Si estás leyendo esto, seguramente buscas a alguien para tu estudio, tu restaurante, tu local o tu hotel. Me encantaría contarte más en persona. Escríbeme.",
]

def presentacion():
    parrafos = "".join(f"<p>{e(t(x))}</p>" for x in PRESENTACION)
    return f"""<section class="bloque bloque-pres" id="quien">
  <h2 class="bloque-titulo">{e(t("Quién soy."))}</h2>
  <div class="pres">{parrafos}</div>
</section>
"""

# ------------------------------------------------------------------ html
def e(s):
    return html.escape(str(s), quote=True)

def ratio(nombre):
    m = re.search(r'width="(\d+)" height="(\d+)"', tam(nombre))
    return (int(m.group(1)) / int(m.group(2))) if m else 1.0

_TAM = {}
def tam(nombre):
    """width/height reales del webp, para reservar el espacio antes de cargar."""
    if nombre not in _TAM:
        try:
            from PIL import Image
            with Image.open(os.path.join(ROOT, "assets", "img", nombre + ".webp")) as im:
                _TAM[nombre] = f' width="{im.width}" height="{im.height}"'
        except Exception:
            _TAM[nombre] = ""
    return _TAM[nombre]

def head(titulo, descripcion, activa, archivo="index.html"):
    alternos = "".join(f'<link rel="alternate" hreflang="{c}" href="{BASE}{carpeta}{archivo}">' for c, _, carpeta in IDIOMAS_SITIO)
    return f"""<!DOCTYPE html>
<html lang="{LANG}" data-puerta="{activa}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:type" content="profile">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{A("styles.css")}?v={V}">
<link rel="icon" href="{A("assets/favicon.svg")}" type="image/svg+xml">
{alternos}
<script src="{A("lib/tema.js")}?v={V}"></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"{NOMBRE}","jobTitle":"Ingeniera civil · Técnica de proyectos · Diseñadora de marca","email":"mailto:{EMAIL}","address":{{"@type":"PostalAddress","addressLocality":"Valencia","addressCountry":"ES"}}}}
</script>
</head>
<body>
<a class="skip-link" href="#principal">{e(t("Ir al contenido"))}</a>
"""

def selector_idioma(archivo):
    enlaces = []
    for c, rotulo, carpeta in IDIOMAS_SITIO:
        activo = ' aria-current="true"' if c == LANG else ""
        enlaces.append(f'<a href="{BASE}{carpeta}{archivo}" hreflang="{c}" lang="{c}"{activo}>{rotulo}</a>')
    return f'<div class="cab-idiomas" role="group" aria-label="{e(t("Idioma"))}">{"".join(enlaces)}</div>'

def nav(activa, archivo="index.html"):
    items = []
    for k in ORDEN_PUERTAS:
        p = PUERTAS[k]
        cls = ' class="is-activa"' if k == activa else ""
        items.append(f'<li><a href="{p["archivo"]}" data-sector="{k}"{cls}>{e(t(p["nav"]))}</a></li>')
    return f"""<header class="cab">
  <a class="cab-nombre" href="index.html">Natalia Giordano</a>
  <div class="cab-acciones">
    {selector_idioma(archivo)}
    <button class="cab-tema" type="button" data-tema aria-label="{e(t("Cambiar entre modo claro y oscuro"))}" title="{e(t("Modo claro / oscuro"))}"><span class="tema-icono" aria-hidden="true"></span></button>
    <button class="cab-menu" type="button" aria-expanded="false" aria-controls="nav-principal" data-menu>{e(t("Menú"))}</button>
  </div>
  <nav id="nav-principal" class="cab-nav" aria-label="{e(t("Áreas"))}">
    <ul>
      {''.join(items)}
      <li><a href="#contacto" class="cab-contacto">{e(t("Escríbeme"))}</a></li>
    </ul>
  </nav>
</header>
"""

def boton(href, texto, extra="", descarga=False):
    d = " download" if descarga else ""
    return f'<a class="btn {extra}" href="{href}"{d} data-iman>{e(texto)}</a>'

def mailto(asunto):
    return f"mailto:{EMAIL}?subject={html.escape(asunto.replace(' ', '%20'))}"

def hero_puerta(k):
    p = PUERTAS[k]
    return f"""<section class="hero hero-{k}" id="principal">
  <div class="hero-int">
    <p class="hero-rotulo">{e(t(p["nav"]))}</p>
    <h1 class="hero-titulo">{e(t(p["titulo"]))}</h1>
    {"".join(f'<p class="hero-linea">{e(x.strip())}</p>' for x in t(p["linea"]).split("<br>"))}
    <p class="hero-disp mono">{e(t(p["disponible"]))}</p>
  </div>
  <div class="hero-foto"><img src="{A("assets/img/nati-carnet.webp")}" alt="Natalia Giordano" loading="eager"></div>
</section>
"""

def pilares(k):
    p = PUERTAS[k]
    cols = "".join(f"""<div class="pilar">
      <h3 class="pilar-nombre">{e(t(tt))}</h3>
      <p>{e(t(d))}</p>
    </div>""" for tt, d in p["pilares"])
    return f"""<section class="bloque bloque-pilares">
  <h2 class="bloque-titulo">{e(t("Qué hago."))}</h2>
  <div class="pilares">{cols}</div>
</section>
"""

def muestras(k):
    p = PUERTAS[k]
    if not p["muestras"]:
        return ""
    cards = []
    for item in p["muestras"]:
        tt, src, extra = t(item[0]), item[1], item[2]
        tipo = item[3] if len(item) > 3 else ""
        ajuste = " ajuste-contener" if tipo in ("contener", "ancha", "fila", "cuadro", "grande", "par") else ""
        ancha = {"ancha": " muestra-ancha", "fila": " muestra-fila", "cuadro": " muestra-cuadro", "grande": " muestra-grande", "par": " muestra-par"}.get(tipo, "")
        if src == "Espacio reservado":
            cuerpo = f'<div class="muestra-img muestra-hueco"><span>Espacio reservado</span></div>'
        elif src.startswith("rota:"):
            lista = src[5:].split(",")
            imgs = "".join(f'<img src="{A("assets/img/")}{n}.webp"{tam(n)} alt="{e(tt)}, {e(t("vista"))} {i + 1}" loading="lazy" decoding="async"{" class=is-on" if i == 0 else ""}>' for i, n in enumerate(lista))
            cuerpo = f'<div class="muestra-img muestra-rota" data-rota tabindex="0" role="button" aria-label="{e(tt)}: {e(t("alterna sola; tocar para pasar a la siguiente"))}">{imgs}</div>'
        elif src.startswith("swap:"):
            a1 = src[5:]
            cuerpo = (f'<div class="muestra-img muestra-swap" data-swap tabindex="0" role="button" aria-label="{e(tt)}: pasar el ratón o tocar para ver la versión a color">'
                      f'<img src="{A("assets/img/")}{a1}.webp"{tam(a1)} alt="{e(tt)}, versión en línea" loading="lazy" decoding="async">'
                      f'<img class="swap-color" src="{A("assets/img/")}{extra}.webp"{tam(extra)} alt="{e(tt)}, versión a color" loading="lazy" decoding="async"></div>')
        elif src.startswith("video:"):
            v = src[6:]
            cuerpo = (f'<div class="muestra-img muestra-video{ajuste}"><video src="{A("assets/video/")}{v}.mp4" poster="{A("assets/img/")}{extra}.webp" '
                      f'autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback controlslist="nodownload noplaybackrate noremoteplayback" aria-label="{e(tt)}"></video></div>')
        else:
            cuerpo = f'<div class="muestra-img{ajuste}"><img src="{A("assets/img/")}{src}.webp"{tam(src)} alt="{e(tt)}" loading="lazy" decoding="async"></div>'
        cards.append((tipo, src, f'<figure class="muestra{ancha}" data-reveal>{cuerpo}<figcaption>{e(tt)}</figcaption></figure>'))
    # fila justificada: los "par" consecutivos comparten altura; el ancho de cada uno sigue su proporción
    salida, grupo = [], []
    def cerrar():
        if grupo:
            cols = " ".join(f"{ratio(src):.4f}fr" for _, src, _ in grupo)
            salida.append(f'<div class="muestras-par" style="grid-template-columns:{cols}">' + "".join(h for _, _, h in grupo) + "</div>")
            grupo.clear()
    for tipo, src, h in cards:
        if tipo == "par":
            grupo.append((tipo, src, h))
        else:
            cerrar(); salida.append(h)
    cerrar()
    cards = salida
    return f"""<section class="bloque bloque-muestras" id="trabajo">
  <h2 class="bloque-titulo">{e(t(p["muestras_titulo"]))}</h2>
  <div class="muestras">{''.join(cards)}</div>
</section>
"""

ARCHIVO = ["AgroPec","Serendipia","Luna Encantada","HF.org","Victoria","Brûlée","Falafel pa' vo'","Georgiana Lupu","JaaGlobal","Perséfone","Bloom Society","Naturaleza","Joana","LoVintage","Rise","Terraz","Origen","Haya","El Conde de la Corte","Creatio","StratBridge","Gazzi","Casa Apicultora Saladillo","Pia Barriga","Comparo.uy","Opuletta","Honky Tonk"]

def archivo(k):
    if k != "marca":
        return ""
    items = "".join(f'<li><img src="{A("assets/img/")}logo-{i:02d}.webp" alt="{e(t("Logotipo"))} {e(n)}" loading="lazy"></li>' for i, n in enumerate(ARCHIVO, 1))
    return f"""<section class="bloque bloque-archivo" id="archivo">
  <h2 class="bloque-titulo">{e(t("Marcas."))}</h2>
  <ul class="archivo">{items}</ul>
</section>
"""

def timeline(activa):
    filas = []
    for ini, fin, sector, lugar, puesto, empresa, tareas in TIMELINE:
        propio = " is-propio" if sector == activa else ""
        filas.append(f"""<li class="tl-item sector-{sector}{propio}" data-reveal>
      <span class="tl-fecha">{e(fecha(ini))} – {e(fecha(fin))}</span>
      <span class="tl-punto" aria-hidden="true"></span>
      <div class="tl-cuerpo">
        <h3 class="tl-puesto">{e(t(puesto))}</h3>
        <p class="tl-empresa">{e(t(empresa))} · {e(t(lugar))}</p>
        {f'<p class="tl-tareas">{e(t(tareas))}</p>' if tareas else ''}
        <span class="tl-sector">{e(t(SECTOR_NOMBRE[sector]))}</span>
      </div>
    </li>""")
    return f"""<section class="bloque bloque-tl" id="trayectoria">
  <h2 class="bloque-titulo">{e(t("Toda la trayectoria."))}</h2>
  <p class="bloque-linea">{e(t("Desde 2007 hasta la actualidad."))}</p>
  <ol class="tl">{''.join(filas)}</ol>
</section>
"""

MOVILIDAD = {
    "tecnica": "Disponibilidad inmediata. Presencial en Valencia o en remoto desde cualquier lugar.",
    "marca": "Disponibilidad inmediata. Presencial en Valencia o en remoto desde cualquier lugar.",
    "hosteleria": "Disponibilidad inmediata. Puedo mudarme dentro de España (incluidas las islas) y a Italia, Suiza, Noruega, Islandia y Países Bajos.",
    "index": "Presencial en Valencia, en remoto desde cualquier lugar, o con traslado dentro de España y a Italia, Suiza, Noruega, Islandia y Países Bajos.",
}

def ficha(k="index"):
    filas_datos = [FICHA[0], ("Movilidad", MOVILIDAD[k])] + FICHA[1:]
    filas = "".join(f'<div class="ficha-fila"><dt>{e(t(a))}</dt><dd>{e(t(b))}</dd></div>' for a, b in filas_datos)
    cv = f"assets/cv/CV-Natalia-Giordano-{LANG}.pdf"
    return f"""<section class="bloque bloque-ficha" id="ficha">
  <h2 class="bloque-titulo">{e(t("Lo práctico."))}</h2>
  <dl class="ficha">{filas}</dl>
  <p class="ficha-cv"><a class="btn btn-borde" href="{A(cv)}" download>{e(t("Descargar el CV en PDF"))}</a></p>
</section>
"""

def herramientas():
    grupos = "".join(f"""<div class="herr-grupo">
      <h3 class="herr-nombre">{e(t(g))}</h3>
      <ul>{''.join(f'<li>{e(x)}</li>' for x in xs)}</ul>
    </div>""" for g, xs in HERRAMIENTAS)
    idi = "".join(f'<li><strong>{e(t(a))}</strong> {e(t(b))}</li>' for a, b in IDIOMAS)
    return f"""<section class="bloque bloque-herr" id="herramientas">
  <h2 class="bloque-titulo">{e(t("Herramientas e idiomas."))}</h2>
  <div class="herr">{grupos}
    <div class="herr-grupo">
      <h3 class="herr-nombre">{e(t("Idiomas"))}</h3>
      <ul class="idiomas">{idi}</ul>
    </div>
  </div>
</section>
"""

# Series de fotografía: un recuadro por lugar; la primera es la portada, el resto se funden encima.
SERIES = [
    ("Valencia, España · 2026", ["foto-valencia-1", "foto-valencia-2", "foto-valencia-3", "foto-valencia-4", "foto-valencia-5", "foto-valencia-6", "foto-valencia-7", "foto-valencia-12", "foto-valencia-8", "foto-valencia-9", "foto-valencia-10", "foto-valencia-11"]),
    ("Passo del Tonale, Italia · 2026", [
        "foto-tonale-bandera", "foto-tonale-esquis", "foto-tonale-2", "foto-tonale-retrato", "foto-tonale-3",
        "foto-tonale-valle", "foto-tonale-6", "foto-tonale-1", "foto-tonale-pico", "foto-tonale-4",
    ]),
    ("Australia · 2024 – 2025", [
        "foto-australia-1", "foto-au-ballena", "foto-au-medusa", "foto-australia-2", "foto-au-opera-1", "foto-au-delfines",
        "foto-au-surf-2", "foto-au-ola", "foto-australia-4", "foto-au-opera-2", "foto-au-playa-3",
        "foto-australia-5", "foto-au-playa-4", "foto-australia-6", "foto-au-camping", "foto-au-playa-2",
    ]),
]

def fotografia():
    series = ""
    for i, (lugar, fotos) in enumerate(SERIES):
        imgs = "".join(
            f'<img src="{A("assets/img/")}{a}.webp" alt="{e(t(lugar))}" loading="lazy" decoding="async"{" class=is-on" if j == 0 else ""}>'
            for j, a in enumerate(fotos))
        series += f'''<figure class="serie" data-serie data-reveal style="--desfase:{i * 2200}ms">
      <div class="serie-marco">{imgs}</div>
      <figcaption class="mono">{e(t(lugar))} <span class="serie-n">{len(fotos)} {e(t("fotos"))}</span></figcaption>
    </figure>'''
    return f"""<section class="bloque bloque-foto" id="fotografia">
  <h2 class="bloque-titulo">{e(t("Fotografía."))}</h2>
  <p class="bloque-linea">{e(t("Mi afición. Me ayuda a desconectar y a mirar mejor."))}</p>
  <div class="series">{series}</div>
</section>
"""

def whatsapp():
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(t('Hola Natalia, vi tu portafolio y me gustaría hablar contigo.'))}"

def contacto(asunto):
    return f"""<section class="bloque bloque-contacto inv" id="contacto">
  <h2 class="bloque-titulo">{e(t("Hablemos."))}</h2>
  <p class="bloque-linea">{e(t("Un correo o un mensaje. Respondo en el día."))}</p>
  <div class="contacto-botones">
    <a class="btn btn-blanco" href="{mailto(t(asunto))}" data-iman data-correo="{EMAIL}" data-asunto="{e(t(asunto))}" data-l-titulo="{e(t("Escribir a"))}" data-l-copiar="{e(t("Copiar"))}" data-l-copiado="{e(t("Correo copiado"))}" data-l-gmail="{e(t("Abrir en Gmail"))}" data-l-outlook="{e(t("Abrir en Outlook"))}" data-l-app="{e(t("Programa de correo"))}" data-l-cerrar="{e(t("Cerrar"))}">{e(t("Escríbeme"))}</a>
    <a class="btn btn-borde" href="{whatsapp()}" target="_blank" rel="noopener" data-iman>WhatsApp</a>
  </div>
  <p class="contacto-datos"><a href="{mailto(t(asunto))}" data-correo="{EMAIL}" data-asunto="{e(t(asunto))}" data-l-titulo="{e(t("Escribir a"))}" data-l-copiar="{e(t("Copiar"))}" data-l-copiado="{e(t("Correo copiado"))}" data-l-gmail="{e(t("Abrir en Gmail"))}" data-l-outlook="{e(t("Abrir en Outlook"))}" data-l-app="{e(t("Programa de correo"))}" data-l-cerrar="{e(t("Cerrar"))}">{e(EMAIL)}</a> · <a href="{whatsapp()}" target="_blank" rel="noopener">{e(WHATSAPP_VISIBLE)}</a> · {e(t(CIUDAD))}</p>
</section>
"""

def pie():
    return f"""<footer class="pie">
  <span>© {datetime.date.today().year} Natalia Giordano</span>
  <a href="#principal">{e(t("Volver arriba"))}</a>
</footer>
<script defer src="{A("lib/manifest.js")}?v={V}"></script>
<script defer src="{A("main.js")}?v={V}"></script>
</body>
</html>
"""

def pagina_puerta(k):
    p = PUERTAS[k]
    titulo = f"{NOMBRE} — {t(p['nav'])}"
    return (head(titulo, t(p["linea"]).replace("<br>", " "), k, p["archivo"]) + nav(k, p["archivo"]) + '<main>' + hero_puerta(k) + presentacion() + pilares(k) + muestras(k) + archivo(k)
            + timeline(k) + ficha(k) + herramientas() + fotografia() + contacto(p["asunto"]) + '</main>' + pie())

def pagina_index():
    puertas = "".join(f"""<a class="puerta puerta-{k}" href="{PUERTAS[k]['archivo']}" data-iman>
      <span class="puerta-nombre">{e(t(PUERTAS[k]['nav']))}</span>
      <span class="puerta-linea">{e(t(PUERTAS[k]['linea'])).replace("&lt;br&gt;", "<br>")}</span>
      <span class="puerta-disp mono">{e(t(PUERTAS[k]['disponible']))}</span>
      <span class="puerta-ir">{e(t("Entrar"))}</span>
    </a>""" for k in ORDEN_PUERTAS)
    hero = f"""<section class="hero hero-index" id="principal">
  <div class="hero-int">
    <p class="hero-rotulo">{e(t("Ingeniera civil · Técnica de proyectos · Diseñadora gráfica"))}</p>
    <h1 class="hero-titulo">Natalia Giordano.</h1>
    <p class="hero-linea">{e(t("Ingeniera civil y diseñadora gráfica argentina, viviendo actualmente en Valencia, España. Elige el área que te interesa: verás primero lo que buscas y, debajo, toda la trayectoria."))}</p>
  </div>
  <div class="hero-foto"><img src="{A("assets/img/nati-carnet.webp")}" alt="Natalia Giordano" loading="eager"></div>
</section>
<section class="bloque bloque-puertas">
  <div class="puertas">{puertas}</div>
</section>
"""
    desc = t("Ingeniera civil, técnica de proyectos y diseñadora de marca en Valencia. Cómputos y presupuestos, diseño de marca, hostelería y ventas.")
    return (head(f"{NOMBRE} — {t('Ingeniera civil · Diseñadora de marca')}", desc, "index", "index.html") + nav("index", "index.html") + '<main>' + hero + presentacion()
            + timeline("index") + ficha() + herramientas() + fotografia() + contacto("Contacto desde la web") + '</main>' + pie())

def manifest():
    return f"""(function () {{
  "use strict";
  window.__BRAND__ = {{
    name: "{NOMBRE}",
    email: "{EMAIL}",
    whatsapp: "{WHATSAPP}",
    version: "{V}"
  }};
}})();
"""

def escribir(nombre, contenido):
    with open(os.path.join(ROOT, nombre), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)
    print("ok", nombre)

if __name__ == "__main__":
    for codigo, _, carpeta in IDIOMAS_SITIO:
        LANG = codigo
        BASE = "../" if carpeta else ""
        if carpeta:
            os.makedirs(os.path.join(ROOT, carpeta), exist_ok=True)
        escribir(carpeta + "index.html", pagina_index())
        for k in ORDEN_PUERTAS:
            escribir(carpeta + PUERTAS[k]["archivo"], pagina_puerta(k))
    escribir(os.path.join("lib", "manifest.js"), manifest())
