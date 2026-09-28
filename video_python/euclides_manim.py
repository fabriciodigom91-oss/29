"""
Video animado (estilo Manim) del máximo común divisor con el algoritmo de Euclides.

Uso:  pip install manim edge-tts mutagen
      manim -qh euclides_manim.py Euclides
"""

import asyncio
import os
import ssl

import edge_tts
import edge_tts.communicate as ec
from manim import *
from mutagen.mp3 import MP3

VOZ = "es-MX-DaliaNeural"
DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(DIR, "build", "euclides")
if os.path.exists("/root/.ccr/ca-bundle.crt"):
    ec._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

NARRACION = [
    # 0
    "Imagina que tienes un terreno de cuarenta y ocho por dieciocho metros, y quieres cubrirlo con baldosas cuadradas, "
    "todas iguales, lo más grandes posible, y sin cortar ninguna. ¿De qué tamaño deben ser?",
    # 1
    "Esa medida tiene nombre: es el máximo común divisor de cuarenta y ocho y dieciocho. "
    "Y hace más de dos mil años, Euclides encontró una forma genial de calcularlo.",
    # 2
    "La idea es esta: corta el cuadrado más grande que quepa. En cuarenta y ocho caben dos cuadrados de dieciocho... "
    "y sobra una tira de doce.",
    # 3
    "Ahora repetimos lo mismo con lo que sobró. En este pedazo cabe un cuadrado de doce, y sobra una tira de seis.",
    # 4
    "Repetimos otra vez. En doce caben exactamente dos cuadrados de seis. Y esta vez... no sobra nada.",
    # 5
    "Así que la baldosa perfecta mide seis por seis. Caben veinticuatro, sin cortar ninguna. "
    "El máximo común divisor de cuarenta y ocho y dieciocho es seis.",
    # 6
    "Ahora fíjate en lo que hicimos: repetimos el mismo paso, una y otra vez, hasta que no sobró nada. "
    "Y en Python, hasta que se escribe con while.",
    # 7
    "El símbolo de porcentaje calcula el residuo de una división, que es justo la tira que sobra. "
    "Cuarenta y ocho entre dieciocho: sobran doce.",
    # 8
    "En cada vuelta, a toma el valor de b, y b toma el residuo. Dieciocho entre doce: sobran seis. "
    "Doce entre seis: sobra cero.",
    # 9
    "Cuando b llega a cero, la condición del while es falsa, el ciclo termina, y Python imprime seis.",
    # 10
    "¿Y por qué while y no for? Porque no sabíamos cuántos cortes íbamos a necesitar. Eso lo descubrió el propio ciclo. "
    "Recuerda: for, cuando sabes cuántas veces. While, cuando repites hasta que algo cambie.",
]

MONO = "DejaVu Sans Mono"
SANS = "DejaVu Sans"
S = 0.22                      # escala: metros → unidades de pantalla
X0, Y0 = -48 * S / 2, -2.6    # esquina inferior izquierda del terreno


def rect(x, y, w, h, color, opacity=0.55):
    r = Rectangle(width=w * S, height=h * S, stroke_color=WHITE, stroke_width=3,
                  fill_color=color, fill_opacity=opacity)
    r.move_to([X0 + (x + w / 2) * S, Y0 + (y + h / 2) * S, 0])
    return r


def etiqueta(r, texto, size=34):
    return Text(texto, font=SANS, font_size=size, weight=BOLD).move_to(r.get_center())


def code_line(texto):
    t2c = {"while": PURPLE_B, "print": BLUE_B, "48": ORANGE, "18": ORANGE, "0": ORANGE, "!=": WHITE, "%": YELLOW}
    return Text(texto, font=MONO, font_size=30, t2c=t2c)


class Euclides(Scene):
    def preparar_audio(self):
        os.makedirs(AUDIO, exist_ok=True)
        self.duraciones = []
        for i, texto in enumerate(NARRACION):
            p = os.path.join(AUDIO, f"n{i:02d}.mp3")
            if not os.path.exists(p) or os.path.getsize(p) == 0:
                asyncio.run(edge_tts.Communicate(texto, VOZ).save(p))
            self.duraciones.append(MP3(p).info.length)

    def narrar(self, i, *pasos):
        """Reproduce la narración i mientras corren las animaciones; espera a que termine la voz."""
        self.add_sound(os.path.join(AUDIO, f"n{i:02d}.mp3"))
        t0 = self.renderer.time
        for paso in pasos:
            if isinstance(paso, (int, float)):
                self.wait(paso)
            else:
                self.play(*paso[0], run_time=paso[1])
        resto = self.duraciones[i] - (self.renderer.time - t0) + 0.5
        if resto > 0:
            self.wait(resto)

    def construct(self):
        self.preparar_audio()
        self.camera.background_color = "#161B22"

        # --- 0. El problema ---
        titulo = Text("¿Qué baldosa cuadrada cubre el terreno?", font=SANS, font_size=40, weight=BOLD).to_edge(UP)
        terreno = rect(0, 0, 48, 18, GREY_D, 0.4)
        ancho = Text("48 m", font=SANS, font_size=30).next_to(terreno, DOWN, buff=0.2)
        alto = Text("18 m", font=SANS, font_size=30).next_to(terreno, LEFT, buff=0.2)
        self.narrar(0, ([Write(titulo)], 1.5), ([Create(terreno)], 1.5), ([FadeIn(ancho), FadeIn(alto)], 0.8))

        # --- 1. Es el MCD ---
        mcd = Text("= máximo común divisor de 48 y 18", font=SANS, font_size=34, color=YELLOW)
        mcd.next_to(titulo, DOWN, buff=0.3)
        self.narrar(1, ([FadeIn(mcd, shift=DOWN * 0.2)], 1))

        # --- 2. Dos cuadrados de 18 ---
        paso = Text("Idea: corta el cuadrado más grande que quepa", font=SANS, font_size=32, color=BLUE_B)
        paso.move_to(mcd)
        q1, q2 = rect(0, 0, 18, 18, BLUE), rect(18, 0, 18, 18, BLUE)
        l1, l2 = etiqueta(q1, "18"), etiqueta(q2, "18")
        sobra1 = rect(36, 0, 12, 18, GREY_B, 0.25)
        l_s1 = etiqueta(sobra1, "sobra 12", 24)
        self.narrar(2, ([ReplacementTransform(mcd, paso)], 0.8), 1.5,
                    ([DrawBorderThenFill(q1), FadeIn(l1)], 1.0), ([DrawBorderThenFill(q2), FadeIn(l2)], 1.0),
                    ([FadeIn(sobra1), Write(l_s1)], 0.8))

        # --- 3. Un cuadrado de 12 ---
        q3 = rect(36, 0, 12, 12, GREEN)
        l3 = etiqueta(q3, "12")
        sobra2 = rect(36, 12, 12, 6, GREY_B, 0.25)
        l_s2 = etiqueta(sobra2, "sobra 6", 22)
        self.narrar(3, ([Indicate(sobra1, color=YELLOW)], 1.2), ([FadeOut(l_s1)], 0.3),
                    ([DrawBorderThenFill(q3), FadeIn(l3)], 1.0), ([FadeIn(sobra2), Write(l_s2)], 0.8))

        # --- 4. Dos cuadrados de 6 ---
        q4, q5 = rect(36, 12, 6, 6, YELLOW), rect(42, 12, 6, 6, YELLOW)
        l4, l5 = etiqueta(q4, "6", 26), etiqueta(q5, "6", 26)
        self.narrar(4, ([Indicate(sobra2, color=YELLOW)], 1.0), ([FadeOut(l_s2)], 0.3),
                    ([DrawBorderThenFill(q4), FadeIn(l4)], 0.8), ([DrawBorderThenFill(q5), FadeIn(l5)], 0.8))

        # --- 5. La baldosa de 6 cubre todo ---
        cortes = VGroup(q1, q2, q3, q4, q5, l1, l2, l3, l4, l5, sobra1, sobra2)
        baldosas = VGroup(*[rect(6 * i, 6 * j, 6, 6, YELLOW, 0.35) for j in range(3) for i in range(8)])
        res = Text("MCD(48, 18) = 6", font=SANS, font_size=44, weight=BOLD, color=YELLOW).move_to(paso)
        self.narrar(5, ([FadeOut(cortes)], 0.6),
                    ([LaggedStart(*[FadeIn(b, scale=0.5) for b in baldosas], lag_ratio=0.08)], 2.5),
                    ([ReplacementTransform(paso, res)], 1))

        # --- 6. Pasamos al código ---
        dibujo = VGroup(terreno, baldosas, ancho, alto)
        lineas = VGroup(
            code_line("a, b = 48, 18"),
            code_line("while b != 0:"),
            code_line("    a, b = b, a % b"),
            code_line("print(a)"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        # Text() quita los espacios iniciales: aplicamos la sangría a mano
        lineas[2].shift(RIGHT * 4 * Text("a", font=MONO, font_size=30).width * 1.25)
        caja = SurroundingRectangle(lineas, color=GREY_B, buff=0.4, corner_radius=0.15,
                                    fill_color="#212832", fill_opacity=1)
        codigo = VGroup(caja, lineas).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        titulo2 = Text("Repetir hasta que no sobre nada  →  while", font=SANS, font_size=38, weight=BOLD)
        titulo2.to_edge(UP)
        self.narrar(6, ([FadeOut(dibujo), FadeOut(res)], 0.8), ([ReplacementTransform(titulo, titulo2)], 1),
                    ([FadeIn(caja), LaggedStart(*[Write(l) for l in lineas], lag_ratio=0.4)], 2.5))

        # Tabla de la derecha
        encabezado = VGroup(*[Text(t, font=MONO, font_size=30, color=BLUE_B) for t in ("a", "b", "a % b")])
        filas_datos = [("48", "18", "12"), ("18", "12", "6"), ("12", "6", "0")]
        col_x = [2.2, 3.7, 5.4]
        y_tabla = 1.4
        for t, x in zip(encabezado, col_x):
            t.move_to([x, y_tabla, 0])
        linea_tabla = Line([1.5, y_tabla - 0.35, 0], [6.4, y_tabla - 0.35, 0], color=GREY_B)
        filas = []
        for k, fila in enumerate(filas_datos):
            g = VGroup(*[Text(v, font=MONO, font_size=32, color=ORANGE if c < 2 else YELLOW) for c, v in enumerate(fila)])
            for t, x in zip(g, col_x):
                t.move_to([x, y_tabla - 0.9 - 0.75 * k, 0])
            filas.append(g)

        def resaltar(n):
            return SurroundingRectangle(lineas[n], color=YELLOW, buff=0.12, stroke_width=3)

        # --- 7. El residuo ---
        marca = resaltar(2)
        self.narrar(7, ([Create(marca), FadeIn(encabezado), Create(linea_tabla)], 1.2), 1.0,
                    ([FadeIn(filas[0], shift=LEFT * 0.3)], 1.0), ([Indicate(filas[0][2], scale_factor=1.4)], 1.2))

        # --- 8. Vueltas siguientes ---
        self.narrar(8, 1.8, ([FadeIn(filas[1], shift=LEFT * 0.3)], 1.0), 1.6,
                    ([FadeIn(filas[2], shift=LEFT * 0.3)], 1.0), ([Indicate(filas[2][2], color=RED, scale_factor=1.5)], 1.0))

        # --- 9. Termina ---
        falso = Text("b != 0  →  False", font=MONO, font_size=30, color=RED).next_to(caja, DOWN, buff=0.4)
        salida = Text("Salida:  6", font=MONO, font_size=36, color=GREEN, weight=BOLD).move_to([3.8, -2.6, 0])
        self.narrar(9, ([Transform(marca, resaltar(1))], 0.8), ([Write(falso)], 0.8), 0.8,
                    ([Transform(marca, resaltar(3))], 0.8), ([Write(salida)], 0.8))

        # --- 10. Moraleja ---
        fin = VGroup(
            Text("for   →  sabes cuántas veces", font=SANS, font_size=42, t2c={"for": PURPLE_B}),
            Text("while →  hasta que algo cambie", font=SANS, font_size=42, t2c={"while": PURPLE_B}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        todo = VGroup(codigo, encabezado, linea_tabla, *filas, falso, salida, marca)
        self.narrar(10, 4.0, ([FadeOut(todo), FadeOut(titulo2)], 0.8), ([Write(fin[0])], 1.2), 1.5, ([Write(fin[1])], 1.2))
        self.wait(1)
