# -*- coding: utf-8 -*-
"""Genera el CV de Natalia en PDF, una hoja, en ES / EN / IT.

Los datos salen de build.py y las traducciones de traducciones.py: el CV y la web
se alimentan del mismo origen, así que no se pueden desfasar.

  python tools/cv_pdf.py     ->  assets/cv/CV-Natalia-Giordano-{es,en,it}.pdf
"""
import os, sys, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

import build
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ── tipografías ───────────────────────────────────────────────────────────────
for _p in sorted(glob.glob(os.path.join(AQUI, "fuentes_cv", "*.ttf"))):
    pdfmetrics.registerFont(TTFont(os.path.basename(_p)[:-4], _p))
SERIF, SERIF_M = "Fraunces-Light", "Fraunces-Medium"
SANS, SANS_M = "Inter-Regular", "Inter-Medium"

# ── paleta, la misma de styles.css ────────────────────────────────────────────
FG = (0x1C / 255, 0x1A / 255, 0x17 / 255)
FG2 = (0x5B / 255, 0x56 / 255, 0x50 / 255)
FG3 = (0x8E / 255, 0x88 / 255, 0x7F / 255)
ACENTO = (0xB5 / 255, 0x47 / 255, 0x2C / 255)
LINEA = (0.86, 0.85, 0.84)

MM = 72 / 25.4
ANCHO, ALTO = A4
MARGEN = 16 * MM
GUTTER = 25 * MM          # columna de fechas
FOTO = 25 * MM

# ── textos propios del CV (lo demás sale de traducciones.py) ──────────────────
CV = {
    "es": {
        "rol": "Ingeniera civil · Técnica de proyectos · Diseñadora de marca",
        "resumen": "Ingeniera civil por la UTN. Cómputos, presupuestos, dibujo y documentación de proyecto, y diseño de marca desde 2018. Temporadas de hostelería en Italia, Australia y España.",
        "exp": "EXPERIENCIA", "form": "FORMACIÓN", "herr": "HERRAMIENTAS",
        "idi": "IDIOMAS", "prac": "DATOS PRÁCTICOS", "port": "Portafolio",
        "hoy": "hoy",
        "ciud": "Ciudadanía italiana y argentina · permiso de trabajo en toda la UE",
        "nie": "NIE, Seguridad Social y cuenta bancaria en España",
        "carnet": "Sin carnet de conducir",
        "disp": "Disponibilidad inmediata · dispuesta a trasladarme",
        "au": "Cinco puestos de temporada: limpieza residencial y comercial, auxiliar de "
              "catering, polivalente de hotel y de granja, y voluntariados.",
        "sic": "Tres temporadas seguidas: cocina en ritmo alto, lavaplatos, apoyo de sala "
               "y camarera de pisos en hotel boutique.",
        "au_t": "Temporada en Australia", "sic_t": "Temporada en Sicilia",
        "pausa": "Entre la temporada de Australia y la de Italia, en Argentina.",
        "au_e": "No Sweat Cleaning · Spanish Catering · Ravenshoe Hotel · Cape Trib Farm · MINCA",
        "sic_e": "Fontana D'Ercole · La Dependance Hotel · Sabbinirica Bistrot",
    },
    "en": {
        "rol": "Civil engineer · Project technician · Brand designer",
        "resumen": "Civil engineer (UTN). Quantity take-offs, budgets, drafting and project documentation, and brand design since 2018. Hospitality seasons in Italy, Australia and Spain.",
        "exp": "EXPERIENCE", "form": "EDUCATION", "herr": "TOOLS",
        "idi": "LANGUAGES", "prac": "PRACTICAL DETAILS", "port": "Portfolio",
        "hoy": "today",
        "ciud": "Italian and Argentine citizenship · entitled to work anywhere in the EU",
        "nie": "NIE, social security number and bank account in Spain",
        "carnet": "No driving licence",
        "disp": "Available immediately · willing to relocate",
        "au": "Five seasonal roles: residential and commercial cleaning, catering assistant, "
              "hotel and farm all-rounder, and volunteering.",
        "sic": "Three consecutive seasons: fast-paced kitchen, dishwashing, front-of-house "
               "support and room attendant in a boutique hotel.",
        "au_t": "Season in Australia", "sic_t": "Season in Sicily",
        "pausa": "Between the Australian season and the Italian one, in Argentina.",
        "au_e": "No Sweat Cleaning · Spanish Catering · Ravenshoe Hotel · Cape Trib Farm · MINCA",
        "sic_e": "Fontana D'Ercole · La Dependance Hotel · Sabbinirica Bistrot",
    },
    "it": {
        "rol": "Ingegnera civile · Tecnica progettista · Brand designer",
        "resumen": "Ingegnera civile (UTN). Computi metrici, preventivi, disegno e documentazione di progetto, e brand design dal 2018. Stagioni nell'ospitalità in Italia, Australia e Spagna.",
        "exp": "ESPERIENZA", "form": "FORMAZIONE", "herr": "STRUMENTI",
        "idi": "LINGUE", "prac": "DATI PRATICI", "port": "Portfolio",
        "hoy": "oggi",
        "ciud": "Cittadinanza italiana e argentina · permesso di lavoro in tutta l'UE",
        "nie": "NIE, numero di previdenza sociale e conto bancario in Spagna",
        "carnet": "Senza patente di guida",
        "disp": "Disponibilità immediata · disposta a trasferirmi",
        "au": "Cinque impieghi stagionali: pulizie residenziali e commerciali, catering, "
              "tuttofare in hotel e in fattoria, e volontariato.",
        "sic": "Tre stagioni consecutive: cucina a ritmo alto, lavapiatti, supporto in sala "
               "e cameriera ai piani in un hotel boutique.",
        "au_t": "Stagione in Australia", "sic_t": "Stagione in Sicilia",
        "pausa": "Tra la stagione in Australia e quella in Italia, in Argentina.",
        "au_e": "No Sweat Cleaning · Spanish Catering · Ravenshoe Hotel · Cape Trib Farm · MINCA",
        "sic_e": "Fontana D'Ercole · La Dependance Hotel · Sabbinirica Bistrot",
    },
}

# claves de TIMELINE que se agrupan en un solo bloque para que entre en una hoja
AGRUPADAS = {"No Sweat Cleaning", "Spanish Catering", "Ravenshoe Hotel", "Cape Trib Farm",
             "Proyecto MINCA y casa de familia", "Fontana D'Ercole", "La Dependance Hotel",
             "Sabbinirica Bistrot"}


def entradas(lang):
    """Los bloques de experiencia, ya ordenados y con Australia y Sicilia agrupadas."""
    c = CV[lang]
    t = build.t
    fuera = []
    for desde, hasta, sector, lugar, puesto, empresa, desc in build.TIMELINE:
        if sector == "formacion" or empresa in AGRUPADAS:
            continue
        if sector == "viaje":
            # No fue un empleo: va como línea discreta, solo para que no quede un
            # hueco de seis meses sin explicar entre Australia y La Torretta.
            fuera.append((desde, hasta, c["pausa"], "", "", "", True))
            continue
        fuera.append((desde, hasta, t(puesto), t(empresa), t(lugar), t(desc), False))
    # sin lugar: el título del bloque ya dice dónde fue
    fuera.append(("2024-10", "2025-07", c["au_t"], c["au_e"], "", c["au"], False))
    fuera.append(("2024-04", "2024-10", c["sic_t"], c["sic_e"], "", c["sic"], False))
    fuera.sort(key=lambda e: e[0], reverse=True)
    return fuera


def formacion(lang):
    t = build.t
    return [(d, h, t(p), t(e), t(l), t(x))
            for d, h, s, l, p, e, x in build.TIMELINE if s == "formacion"]


# ── dibujo ────────────────────────────────────────────────────────────────────
def ancho(txt, fuente, tam):
    return pdfmetrics.stringWidth(txt, fuente, tam)


def partir(txt, fuente, tam, maximo):
    lineas, actual = [], ""
    for palabra in txt.split():
        prueba = (actual + " " + palabra).strip()
        if ancho(prueba, fuente, tam) <= maximo:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


class Hoja(object):
    def __init__(self, c):
        self.c = c
        self.y = ALTO - MARGEN

    def texto(self, x, txt, fuente, tam, color, interlinea=None, maximo=None):
        maximo = maximo or (ANCHO - MARGEN - x)
        self.c.setFont(fuente, tam)
        self.c.setFillColorRGB(*color)
        for linea in partir(txt, fuente, tam, maximo):
            self.c.drawString(x, self.y, linea)
            self.y -= (interlinea or tam * 1.32)

    def regla(self, color=LINEA, grosor=0.5, sangria=0):
        self.c.setStrokeColorRGB(*color)
        self.c.setLineWidth(grosor)
        self.c.line(MARGEN + sangria, self.y, ANCHO - MARGEN, self.y)

    def rotulo(self, txt):
        self.y -= 5 * MM
        self.regla()
        self.y -= 3.6 * MM
        self.c.setFont(SANS_M, 7)
        self.c.setFillColorRGB(*FG3)
        self.c.drawString(MARGEN, self.y, " ".join(txt))   # letra espaciada a mano
        self.y -= 4.6 * MM


def fecha(iso, lang, c):
    if iso is None:
        return c["hoy"]
    a, m = iso.split("-")
    return "%s %s" % (build.MESES_IDIOMA[lang][int(m)], a)


def linea_pausa(h, desde, hasta, texto, lang, c):
    """Una pausa entre temporadas: se anota, pero no compite con un empleo."""
    rango = "%s – %s" % (fecha(desde, lang, c), fecha(hasta, lang, c))
    h.c.setFont(SANS, 7)
    h.c.setFillColorRGB(*FG3)
    h.c.drawString(MARGEN, h.y, rango)
    # el rango va en una sola línea y es más ancho que la columna de fechas:
    # se empuja el texto lo necesario para que nunca se toquen
    x = max(MARGEN + GUTTER, MARGEN + ancho(rango, SANS, 7) + 3.5 * MM)
    h.c.setFont(SANS, 7.6)
    h.c.drawString(x, h.y, texto)
    h.y -= 6.4 * MM


def bloque(h, desde, hasta, puesto, empresa, lugar, desc, lang, c):
    x = MARGEN + GUTTER
    max_txt = ANCHO - MARGEN - x
    arriba = h.y
    # columna de fechas
    h.c.setFont(SANS, 7)
    h.c.setFillColorRGB(*FG3)
    h.c.drawString(MARGEN, h.y, fecha(desde, lang, c))
    h.c.drawString(MARGEN, h.y - 3.4 * MM, fecha(hasta, lang, c))
    # contenido
    h.c.setFont(SANS_M, 8.8)
    h.c.setFillColorRGB(*FG)
    h.c.drawString(x, h.y, puesto)
    h.y -= 3.8 * MM
    h.c.setFont(SANS, 8)
    h.c.setFillColorRGB(*FG2)
    linea = "%s · %s" % (empresa, lugar) if lugar else empresa
    for l in partir(linea, SANS, 8, max_txt):
        h.c.drawString(x, h.y, l)
        h.y -= 3.4 * MM
    if desc:
        h.c.setFont(SANS, 7.4)
        h.c.setFillColorRGB(*FG3)
        for l in partir(desc, SANS, 7.4, max_txt):
            h.c.drawString(x, h.y, l)
            h.y -= 3.1 * MM
    h.y = min(h.y, arriba - 7 * MM) - 2.2 * MM


def generar(lang):
    build.LANG = lang
    c = CV[lang]
    t = build.t
    destino = os.path.join(RAIZ, "assets", "cv", "CV-Natalia-Giordano-%s.pdf" % lang)
    os.makedirs(os.path.dirname(destino), exist_ok=True)

    lienzo = canvas.Canvas(destino, pagesize=A4)
    lienzo.setTitle("CV Natalia Giordano")
    lienzo.setAuthor(build.NOMBRE)
    h = Hoja(lienzo)

    # ── cabecera ──────────────────────────────────────────────────────────────
    foto = os.path.join(RAIZ, "assets", "img", "nati-retrato.jpg")
    hay_foto = os.path.exists(foto)
    ancho_txt = (ANCHO - 2 * MARGEN - FOTO - 6 * MM) if hay_foto else (ANCHO - 2 * MARGEN)
    if hay_foto:
        lienzo.drawImage(ImageReader(foto), ANCHO - MARGEN - FOTO, ALTO - MARGEN - FOTO,
                         FOTO, FOTO, mask=None)

    h.y = ALTO - MARGEN - 8 * MM
    lienzo.setFont(SERIF, 25)
    lienzo.setFillColorRGB(*FG)
    lienzo.drawString(MARGEN, h.y, build.NOMBRE)
    h.y -= 6.4 * MM
    lienzo.setFont(SANS, 8.4)
    lienzo.setFillColorRGB(*ACENTO)
    lienzo.drawString(MARGEN, h.y, c["rol"])
    h.y -= 5.2 * MM
    lienzo.setFont(SANS, 8)
    lienzo.setFillColorRGB(*FG2)
    lienzo.drawString(MARGEN, h.y, "%s · %s · %s"
                      % (build.EMAIL, build.WHATSAPP_VISIBLE, t("Valencia, España")))
    h.y -= 4.2 * MM
    enlace = "https://nataliagiordano9-maker.github.io/%s" % ("" if lang == "es" else lang + "/")
    lienzo.setFillColorRGB(*FG3)
    lienzo.drawString(MARGEN, h.y, "%s: %s" % (c["port"], enlace))
    lienzo.linkURL(enlace, (MARGEN, h.y - 1 * MM, MARGEN + ancho_txt, h.y + 3 * MM),
                   relative=0, thickness=0)
    h.y = min(h.y, ALTO - MARGEN - FOTO) - 4.5 * MM
    h.texto(MARGEN, c["resumen"], SANS, 8, FG2, interlinea=3.9 * MM,
            maximo=ANCHO - 2 * MARGEN)

    # ── experiencia ───────────────────────────────────────────────────────────
    h.rotulo(c["exp"])
    for desde, hasta, puesto, empresa, lugar, desc, pausa in entradas(lang):
        if pausa:
            linea_pausa(h, desde, hasta, puesto, lang, c)
        else:
            bloque(h, desde, hasta, puesto, empresa, lugar, desc, lang, c)

    # ── formación ─────────────────────────────────────────────────────────────
    h.rotulo(c["form"])
    for desde, hasta, puesto, empresa, lugar, desc in formacion(lang):
        bloque(h, desde, hasta, puesto, empresa, lugar, "", lang, c)

    # ── pie: herramientas, idiomas, datos prácticos ───────────────────────────
    h.rotulo(c["herr"])
    # la columna se calcula: el rótulo más largo manda, así nada se pisa
    rotulos = [t(g) for g, _ in build.HERRAMIENTAS] + [c["idi"].capitalize()]
    col = MARGEN + max(ancho(r, SANS_M, 7.4) for r in rotulos) + 5 * MM

    filas = [(t(g), " · ".join(l)) for g, l in build.HERRAMIENTAS]
    filas.append((c["idi"].capitalize(),
                  " · ".join("%s %s" % (t(a), t(b)) for a, b in build.IDIOMAS)))
    for i, (rot, valor) in enumerate(filas):
        if i == len(filas) - 1:
            h.y -= 1.4 * MM
        lienzo.setFont(SANS_M, 7.4)
        lienzo.setFillColorRGB(*FG2)
        lienzo.drawString(MARGEN, h.y, rot)
        lienzo.setFont(SANS, 7.4)
        lienzo.setFillColorRGB(*FG3)
        lienzo.drawString(col, h.y, valor)
        h.y -= 3.6 * MM
    h.y -= 1.4 * MM

    h.regla()
    h.y -= 3.6 * MM
    lienzo.setFont(SANS, 7.4)
    lienzo.setFillColorRGB(*FG2)
    for linea in (c["ciud"], c["nie"], "%s · %s" % (c["carnet"], c["disp"])):
        lienzo.drawString(MARGEN, h.y, linea)
        h.y -= 3.6 * MM

    lienzo.showPage()
    lienzo.save()
    sobra = h.y - MARGEN
    print("ok  %-34s  margen inferior: %+.1f mm  %s"
          % (os.path.basename(destino), sobra / MM,
             "" if sobra >= 0 else "  <-- SE PASA DE UNA HOJA"))
    return sobra


if __name__ == "__main__":
    peor = min(generar(c) for c in ("es", "en", "it"))
    sys.exit(0 if peor >= 0 else 1)
