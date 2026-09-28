"""
Guion del video "Aprende Python desde cero".

Cada escena es un diccionario:
  - tipo "slide": title, bullets (las que empiezan con "$ " se dibujan como código)
  - tipo "code":  title, code, line (línea resaltada o None), vars, out, dim, caption
  - "say": lo que narra la voz
"""

INTRO = [
    dict(type="title", title="Aprende Python desde cero",
         subtitle="La lógica detrás de if, elif, else, for y while",
         say="Hola, soy Dalia. En este video vas a entender la lógica detrás de Python: "
             "qué hace la computadora cuando lee tu código, y cómo saber cuándo usar if, elif, else, for y while. "
             "Te recomiendo tener abierto tu notebook de Jupyter, para practicar después de cada parte."),
    dict(type="slide", section="1. Cómo piensa una computadora", title="Un programa es una receta",
         bullets=["La computadora lee tu código línea por línea, de arriba hacia abajo",
                  "Hace exactamente lo que escribiste, no lo que quisiste decir",
                  "Todo programa, por grande que sea, usa solo 3 ingredientes"],
         say="Un programa es como una receta. La computadora la sigue línea por línea, de arriba hacia abajo, "
             "y hace exactamente lo que escribiste, no lo que quisiste decir. "
             "Y lo mejor: todo programa, por grande que sea, está hecho con solo tres ingredientes."),
    dict(type="slide", section="1. Cómo piensa una computadora", title="Los 3 ingredientes",
         bullets=["Secuencia: una cosa, luego la siguiente, luego la siguiente",
                  "Decisión: \"si pasa esto, haz aquello\"  →  if, elif, else",
                  "Repetición: \"haz esto varias veces\"  →  for, while",
                  "for = \"por cada...\"  (sabes cuántas veces)",
                  "while = \"mientras...\"  (repites hasta que algo cambie)"],
         say="Primero, la secuencia: hacer una cosa después de otra. Segundo, la decisión: si pasa esto, haz aquello. "
             "Para eso usamos if, elif y else. Tercero, la repetición: hacer algo varias veces, con for o con while. "
             "Guarda esta idea, porque es la clave de todo el video: for significa por cada, y lo usas cuando sabes cuántas veces repetir. "
             "While significa mientras, y lo usas cuando repites hasta que algo cambie."),
]

VARIABLES_CODE = """puntos = 10
puntos = puntos + 5
print(puntos)"""

VARIABLES = [
    dict(type="code", section="2. Variables", title="Variables: cajas con nombre", code=VARIABLES_CODE,
         line=None, vars={}, out=[], caption="=  no significa \"es igual\": significa \"guarda en\"",
         say="Empecemos por lo más básico: las variables. Una variable es una caja con nombre donde guardas un dato. "
             "Ojo: en Python, el signo igual no significa es igual. Significa: guarda en."),
    dict(type="code", section="2. Variables", title="Variables: cajas con nombre", code=VARIABLES_CODE,
         line=0, vars={"puntos": "10"}, out=[], caption="Guarda 10 en la caja llamada puntos",
         say="Primera línea: guarda diez en la caja llamada puntos."),
    dict(type="code", section="2. Variables", title="Variables: cajas con nombre", code=VARIABLES_CODE,
         line=1, vars={"puntos": "15"}, out=[], caption="Primero la derecha: 10 + 5 = 15.  Luego se guarda en puntos",
         say="Segunda línea. Primero se calcula lo de la derecha: puntos vale diez, más cinco, da quince. "
             "Después ese quince se guarda otra vez en puntos, y el diez anterior se reemplaza."),
    dict(type="code", section="2. Variables", title="Variables: cajas con nombre", code=VARIABLES_CODE,
         line=2, vars={"puntos": "15"}, out=["15"], caption="print muestra el valor actual",
         say="Tercera línea: print muestra en pantalla el valor actual de puntos: quince."),
    dict(type="slide", section="3. Preguntas", title="Guardar  vs.  preguntar",
         bullets=["$ edad = 25      # guarda 25 en edad",
                  "$ edad == 25     # pregunta: ¿edad es igual a 25?",
                  "Las preguntas responden True (verdadero) o False (falso)",
                  "$ >   <   >=   <=   !=  (distinto)",
                  "Se combinan con and (las dos), or (al menos una) y not (lo contrario)"],
         say="Un solo igual guarda un valor. Dos iguales hacen una pregunta: ¿edad es igual a veinticinco? "
             "Las preguntas siempre responden verdadero o falso, en inglés True o False. "
             "También puedes preguntar mayor, menor, mayor o igual, menor o igual, o distinto. "
             "Y puedes combinarlas: and exige que se cumplan las dos, or que se cumpla al menos una, y not invierte la respuesta. "
             "Estas preguntas son las que usan if y while para decidir."),
]

IF_CODE = """nota = 85

if nota >= 90:
    print("Excelente")
elif nota >= 80:
    print("Muy bien")
elif nota >= 70:
    print("Bien")
else:
    print("Reprobado")"""

S_IF = "4. Decisiones: if, elif, else"
IF = [
    dict(type="code", section=S_IF, title="if, elif, else", code=IF_CODE, line=None, vars={}, out=[],
         caption="if = \"si...\"   Lo indentado (movido a la derecha) está DENTRO del if",
         say="Ahora las decisiones. If significa si. Revisa una condición, y solo si es verdadera, ejecuta las líneas de adentro: "
             "las que están indentadas, es decir, movidas hacia la derecha. Esa sangría no es decoración: le dice a Python qué está dentro del if. "
             "Y no olvides los dos puntos al final de la condición."),
    dict(type="code", section=S_IF, title="if, elif, else", code=IF_CODE, line=0, vars={"nota": "85"}, out=[],
         caption="Guardamos 85 en nota",
         say="Vamos paso a paso. Primero guardamos ochenta y cinco en nota."),
    dict(type="code", section=S_IF, title="if, elif, else", code=IF_CODE, line=2, vars={"nota": "85"}, out=[],
         caption="¿85 >= 90?   →   False", bad=True,
         say="Python pregunta: ¿ochenta y cinco es mayor o igual que noventa? No, es falso. "
             "Así que se salta el print de adentro y baja al siguiente elif."),
    dict(type="code", section=S_IF, title="if, elif, else", code=IF_CODE, line=4, vars={"nota": "85"}, out=[], dim=[3],
         caption="¿85 >= 80?   →   True", good=True,
         say="Elif significa: si no, entonces si. Solo se revisa porque lo anterior fue falso. "
             "¿Ochenta y cinco es mayor o igual que ochenta? Sí, es verdadero."),
    dict(type="code", section=S_IF, title="if, elif, else", code=IF_CODE, line=5, vars={"nota": "85"}, out=["Muy bien"], dim=[3],
         caption="Se ejecuta lo de adentro",
         say="Entonces ejecuta lo que tiene adentro, y muestra: muy bien."),
    dict(type="code", section=S_IF, title="if, elif, else", code=IF_CODE, line=None, vars={"nota": "85"}, out=["Muy bien"],
         dim=[2, 3, 6, 7, 8, 9], caption="Solo se ejecuta UNA rama: la primera que sea True",
         say="Y aquí viene lo más importante. En cuanto una condición es verdadera, Python ejecuta esa rama y se salta todas las demás, "
             "aunque ochenta y cinco también sea mayor que setenta. De toda la cadena if, elif, else, solo se ejecuta una rama. "
             "El else del final es el plan B: se ejecuta solo si ninguna condición fue verdadera."),
    dict(type="slide", section=S_IF, title="Reglas de oro de if / elif / else",
         bullets=["Python revisa de arriba hacia abajo y se detiene en la primera condición verdadera",
                  "Por eso el orden importa: pon primero la más exigente (>= 90 antes que >= 60)",
                  "if solo → 1 camino (\"haz esto solo si...\")",
                  "if / else → 2 caminos (\"esto o aquello\")",
                  "if / elif / else → 3 o más caminos, y solo ocurre uno",
                  "Varios if separados → preguntas independientes: pueden cumplirse varias"],
         say="Resumamos las reglas de oro. Python revisa de arriba hacia abajo y se detiene en la primera condición verdadera. "
             "Por eso el orden importa: si pusieras primero nota mayor o igual que sesenta, un noventa y cinco caería ahí, y nunca diría excelente. "
             "Un if solo es para un caso especial. If con else, para dos caminos. If, elif, else, para tres o más caminos donde solo ocurre uno. "
             "Y si las preguntas son independientes, y pueden cumplirse varias a la vez, usa varios if separados, no elif."),
]

FOR_CODE = """total = 0
for n in range(1, 6):
    total = total + n
print(total)"""

S_FOR = "5. Repetir con for"
FOR = [
    dict(type="slide", section=S_FOR, title="for = \"por cada...\"",
         bullets=["Úsalo cuando sabes cuántas veces repetir, o tienes una lista que recorrer",
                  "$ for variable in coleccion:",
                  "En cada vuelta, la variable toma el siguiente valor",
                  "$ range(5)          →  0 1 2 3 4",
                  "$ range(1, 6)       →  1 2 3 4 5",
                  "$ range(0, 11, 2)   →  0 2 4 6 8 10",
                  "El número final de range nunca se incluye"],
         say="Pasemos a la repetición. For significa por cada. Lo usas cuando sabes cuántas veces repetir, o cuando tienes una lista de cosas que recorrer. "
             "En cada vuelta, la variable toma el siguiente valor de la colección. "
             "Para generar números usamos range. Range de cinco da del cero al cuatro. Range de uno a seis da del uno al cinco. "
             "Y con un tercer número puedes avanzar de dos en dos. Recuerda: el número final nunca se incluye."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=0, vars={"total": "0"}, out=[],
         caption="Antes del ciclo: el acumulador empieza en 0",
         say="Veamos el patrón más útil de la programación: el acumulador. Queremos sumar los números del uno al cinco. "
             "Antes del ciclo, creamos total y lo ponemos en cero."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=1, vars={"total": "0", "n": "1"}, out=[],
         caption="Vuelta 1: n toma el primer valor → 1",
         say="Primera vuelta: n toma el primer valor del range, uno."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=2, vars={"total": "1", "n": "1"}, out=[],
         caption="total = 0 + 1 = 1",
         say="Total es cero más uno: uno."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=1, vars={"total": "1", "n": "2"}, out=[],
         caption="Vuelta 2: n → 2",
         say="Python vuelve a la línea del for. Segunda vuelta: n vale dos."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=2, vars={"total": "3", "n": "2"}, out=[],
         caption="total = 1 + 2 = 3",
         say="Uno más dos: tres."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=2, vars={"total": "6", "n": "3"}, out=[],
         caption="Vuelta 3:  total = 3 + 3 = 6",
         say="Tercera vuelta: n vale tres, y total pasa a seis."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=2, vars={"total": "10", "n": "4"}, out=[],
         caption="Vuelta 4:  total = 6 + 4 = 10",
         say="Cuarta vuelta: seis más cuatro, diez."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=2, vars={"total": "15", "n": "5"}, out=[],
         caption="Vuelta 5:  total = 10 + 5 = 15",
         say="Quinta vuelta: diez más cinco, quince."),
    dict(type="code", section=S_FOR, title="El acumulador: sumar del 1 al 5", code=FOR_CODE, line=3, vars={"total": "15", "n": "5"}, out=["15"],
         caption="Se acabaron los números → el ciclo termina",
         say="Ya no quedan números en el range, así que el ciclo termina, y Python sigue con la línea de abajo, que ya no está indentada. "
             "Imprime quince. Fíjate que el print está fuera del for: por eso se ejecuta una sola vez, al final."),
    dict(type="slide", section=S_FOR, title="Patrón acumulador (úsalo siempre)",
         bullets=["1. Crea la variable ANTES del ciclo:  total = 0  (o 1 si vas a multiplicar)",
                  "2. Actualízala DENTRO del ciclo",
                  "3. Usa el resultado DESPUÉS del ciclo (sin indentar)",
                  "Con for + if puedes contar: \"¿cuántos números son pares?\"",
                  "Truco: haz a mano una tabla con los valores de cada vuelta"],
         say="Este patrón lo vas a usar siempre. Uno: crea la variable antes del ciclo. Si vas a multiplicar, como en un factorial, empieza en uno, no en cero. "
             "Dos: actualízala dentro del ciclo. Tres: usa el resultado después del ciclo. "
             "Y si metes un if dentro del for, puedes contar cosas, como cuántos números de una lista son pares. "
             "Un truco que funciona muy bien: haz a mano una tabla con los valores de cada vuelta, como acabamos de hacer."),
]

WHILE_CODE = """meta = 500
ahorro = 0
meses = 0

while ahorro < meta:
    ahorro = ahorro + 200
    meses = meses + 1

print(meses)"""

S_WHILE = "6. Repetir con while"
WHILE = [
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=None, vars={}, out=[],
         caption="¿Cuántos meses para ahorrar 500, guardando 200 al mes?",
         say="Ahora while, que significa mientras. Repite mientras una condición sea verdadera. "
             "Lo usas cuando no sabes cuántas veces vas a repetir, porque depende de algo que va cambiando. "
             "Ejemplo: quiero ahorrar quinientos, guardando doscientos cada mes. ¿Cuántos meses necesito?"),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=2,
         vars={"meta": "500", "ahorro": "0", "meses": "0"}, out=[], caption="Preparamos las variables",
         say="Preparamos las variables: la meta es quinientos, y el ahorro y los meses empiezan en cero."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=4,
         vars={"meta": "500", "ahorro": "0", "meses": "0"}, out=[], caption="¿0 < 500?   →   True: entra", good=True,
         say="Python revisa la condición: ¿cero es menor que quinientos? Sí. Entra al ciclo."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=6,
         vars={"meta": "500", "ahorro": "200", "meses": "1"}, out=[], caption="ahorro = 200, meses = 1  → vuelve arriba",
         say="Suma doscientos al ahorro y un mes al contador. Y ahora, en lugar de seguir hacia abajo, vuelve arriba a revisar la condición."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=4,
         vars={"meta": "500", "ahorro": "200", "meses": "1"}, out=[], caption="¿200 < 500?   →   True", good=True,
         say="¿Doscientos es menor que quinientos? Sí. Otra vuelta."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=6,
         vars={"meta": "500", "ahorro": "400", "meses": "2"}, out=[], caption="ahorro = 400, meses = 2",
         say="Ahorro: cuatrocientos. Meses: dos. Vuelve a preguntar."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=4,
         vars={"meta": "500", "ahorro": "400", "meses": "2"}, out=[], caption="¿400 < 500?   →   True", good=True,
         say="¿Cuatrocientos es menor que quinientos? Sí, todavía falta."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=6,
         vars={"meta": "500", "ahorro": "600", "meses": "3"}, out=[], caption="ahorro = 600, meses = 3",
         say="Ahorro: seiscientos. Meses: tres."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=4,
         vars={"meta": "500", "ahorro": "600", "meses": "3"}, out=[], caption="¿600 < 500?   →   False: sale del ciclo", bad=True,
         say="¿Seiscientos es menor que quinientos? No. Ahora la condición es falsa, y el ciclo termina."),
    dict(type="code", section=S_WHILE, title="while = \"mientras...\"", code=WHILE_CODE, line=8,
         vars={"meta": "500", "ahorro": "600", "meses": "3"}, out=["3"], caption="Nunca le dijimos cuántas veces: lo descubrió el ciclo",
         say="Python salta a la primera línea fuera del while, e imprime tres. "
             "Fíjate: nunca le dijimos cuántas veces repetir. El propio ciclo lo descubrió. Esa es la diferencia con for."),
    dict(type="slide", section=S_WHILE, title="Cuidado: el ciclo infinito",
         bullets=["Si nada dentro del while cambia la condición, nunca termina:",
                  "$ x = 1",
                  "$ while x > 0:",
                  "$     print(x)     # x nunca cambia",
                  "En Jupyter se detiene con  Kernel → Interrupt",
                  "Revisa: ¿valor inicial? ¿algo cambia adentro? ¿se acerca a False?"],
         say="Un cuidado importante. Si nada dentro del while cambia la condición, el ciclo nunca termina. "
             "En este ejemplo, x siempre vale uno, así que x mayor que cero es verdadero para siempre. "
             "Si te pasa en Jupyter, ve al menú Kernel y elige Interrupt. "
             "Para evitarlo, revisa tres cosas: que la variable tenga un valor antes del ciclo, que algo la cambie adentro, "
             "y que ese cambio la acerque a que la condición sea falsa."),
]

S_GUIA = "7. ¿Cuál uso?"
GUIA = [
    dict(type="slide", section=S_GUIA, title="La guía para decidir",
         bullets=["$ ¿Tengo que REPETIR algo?",
                  "$ ├─ NO → ¿depende de una condición?",
                  "$ │       ├─ 1 camino          → if",
                  "$ │       ├─ 2 caminos         → if / else",
                  "$ │       └─ 3 o más caminos   → if / elif / else",
                  "$ └─ SÍ → ¿sé cuántas veces o tengo una lista?",
                  "$         ├─ SÍ               → for",
                  "$         └─ NO, hasta que... → while"],
         say="Ahora la parte más importante: cómo decidir qué usar. Hazte esta pregunta primero: ¿tengo que repetir algo? "
             "Si no, pregúntate si depende de una condición, y cuenta los caminos: uno es if, dos es if con else, y tres o más es if, elif, else. "
             "Si sí tienes que repetir, pregúntate: ¿sé cuántas veces, o tengo una lista que recorrer? Si la respuesta es sí, usa for. "
             "Si no lo sabes, y repites hasta que pase algo, usa while."),
    dict(type="slide", section=S_GUIA, title="Palabras clave en el enunciado",
         bullets=["\"si...\", \"solo cuando...\"  →  if",
                  "\"si no...\", \"de lo contrario...\"  →  else",
                  "\"si es A..., si es B..., si es C...\"  →  if / elif / else",
                  "\"por cada...\", \"del 1 al N\", \"N veces\", \"cada elemento\"  →  for",
                  "\"mientras...\", \"hasta que...\", \"¿cuántos intentos / meses?\"  →  while",
                  "\"el primero que cumpla...\"  →  for + break"],
         say="Otro truco: fíjate en las palabras del problema. Si dice si, o solo cuando, es un if. Si dice de lo contrario, es un else. "
             "Si habla de varias categorías, es if, elif, else. Si dice por cada, del uno al ene, o ene veces, es un for. "
             "Si dice mientras, hasta que, o pregunta cuántos intentos o cuántos meses hacen falta, es un while. "
             "Y si pide el primero que cumpla algo, es un for con break, que veremos en un momento."),
]

QUIZ = []
for pregunta, respuesta, razon, say_q, say_a in [
    ("Imprimir la tabla del 7, del 1 al 10", "for", "Sabes que son 10 veces",
     "Practiquemos. Imprimir la tabla del siete, del uno al diez. ¿Qué usarías?",
     "For, porque sabes exactamente cuántas veces: diez."),
    ("Decir si un número es positivo, negativo o cero", "if / elif / else", "3 caminos y solo ocurre uno",
     "Siguiente. Decir si un número es positivo, negativo o cero.",
     "If, elif, else. Hay tres caminos, y solo puede ocurrir uno."),
    ("¿En cuántos años se duplica una inversión al 7% anual?", "while", "Repites hasta que se duplique: no sabes cuántos años",
     "¿En cuántos años se duplica una inversión al siete por ciento anual?",
     "While. Repites año tras año hasta que el dinero se duplique, y no sabes de antemano cuántos años serán."),
    ("Contar cuántas vocales tiene una palabra", "for + if", "Recorres cada letra y preguntas si es vocal",
     "Última. Contar cuántas vocales tiene una palabra.",
     "For con un if adentro. Recorres cada letra con el for, y con el if preguntas si es vocal."),
]:
    QUIZ.append(dict(type="quiz", section="8. Practiquemos", question=pregunta, answer=None,
                     say=say_q + " Pausa el video si quieres pensarlo. Tres, dos, uno."))
    QUIZ.append(dict(type="quiz", section="8. Practiquemos", question=pregunta, answer=respuesta, reason=razon, say=say_a))

PRIMO_CODE = """n = 15
es_primo = True

for d in range(2, n):
    if n % d == 0:
        es_primo = False
        break

print(es_primo)"""

S_MATE = "9. Matemáticas con Python"
MATE = [
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=None, vars={}, out=[],
         caption="%  da el residuo:  15 % 3 = 0  → la división es exacta",
         say="Pasemos a las matemáticas. Un número primo solo se divide exactamente entre uno y él mismo. "
             "La idea es probar a dividir entre dos, tres, cuatro, y así. Si alguno divide exacto, no es primo. "
             "Para eso usamos el símbolo de porcentaje, que en Python da el residuo de una división. Si el residuo es cero, la división es exacta."),
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=1,
         vars={"n": "15", "es_primo": "True"}, out=[], caption="Suponemos que sí es primo... hasta demostrar lo contrario",
         say="Probemos con quince. Empezamos suponiendo que sí es primo, hasta demostrar lo contrario."),
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=4,
         vars={"n": "15", "es_primo": "True", "d": "2"}, out=[], caption="d = 2:   15 % 2 = 1   → no es exacta", bad=True,
         say="Primera vuelta: d vale dos. ¿El residuo de quince entre dos es cero? No, es uno. No hacemos nada, y seguimos."),
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=4,
         vars={"n": "15", "es_primo": "True", "d": "3"}, out=[], caption="d = 3:   15 % 3 = 0   → ¡divide exacto!", good=True,
         say="Segunda vuelta: d vale tres. Quince entre tres da residuo cero. ¡Encontramos un divisor!"),
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=5,
         vars={"n": "15", "es_primo": "False", "d": "3"}, out=[], caption="Ya sabemos que no es primo",
         say="Entonces la variable es primo pasa a falso."),
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=6,
         vars={"n": "15", "es_primo": "False", "d": "3"}, out=[], caption="break: sale del ciclo YA (no prueba 4, 5, 6...)",
         say="Y break rompe el ciclo. Ya sabemos la respuesta, así que no tiene sentido probar cuatro, cinco, seis, y los demás. "
             "Esta combinación, for con break, sirve para buscar hasta encontrar."),
    dict(type="code", section=S_MATE, title="¿Es primo? (for + if + break)", code=PRIMO_CODE, line=8,
         vars={"n": "15", "es_primo": "False", "d": "3"}, out=["False"], caption="15 no es primo",
         say="Al final imprime False: quince no es primo. Cambia n por veintinueve en tu notebook y verás que sí lo es."),
]

EUCLIDES_CODE = """a = 48
b = 18

while b != 0:
    a, b = b, a % b

print(a)"""

MATE += [
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=None, vars={}, out=[],
         caption="MCD(a, b) = MCD(b, a % b)  ...hasta que el residuo sea 0",
         say="Ahora el máximo común divisor, con el algoritmo de Euclides, que tiene más de dos mil años. "
             "La idea: el máximo común divisor de a y b es el mismo que el de b y el residuo de a entre b. "
             "Se repite hasta que el residuo sea cero. Hasta que: eso nos dice que es un while."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=1,
         vars={"a": "48", "b": "18"}, out=[], caption="a = 48,  b = 18",
         say="Empezamos con a igual a cuarenta y ocho, y b igual a dieciocho."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=3,
         vars={"a": "48", "b": "18"}, out=[], caption="¿18 != 0?   →   True", good=True,
         say="¿b es distinto de cero? Sí. Entramos al ciclo."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=4,
         vars={"a": "18", "b": "12"}, out=[], caption="a, b = 18,  48 % 18 = 12",
         say="Ahora a toma el valor de b, dieciocho, y b toma el residuo de cuarenta y ocho entre dieciocho, que es doce."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=4,
         vars={"a": "12", "b": "6"}, out=[], caption="a, b = 12,  18 % 12 = 6",
         say="b sigue sin ser cero. Otra vuelta: a pasa a doce, y b al residuo de dieciocho entre doce, que es seis."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=4,
         vars={"a": "6", "b": "0"}, out=[], caption="a, b = 6,  12 % 6 = 0",
         say="Otra vuelta: a pasa a seis, y el residuo de doce entre seis es cero."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=3,
         vars={"a": "6", "b": "0"}, out=[], caption="¿0 != 0?   →   False: termina", bad=True,
         say="Ahora b es cero. La condición es falsa, y el ciclo termina."),
    dict(type="code", section=S_MATE, title="Máximo común divisor (Euclides)", code=EUCLIDES_CODE, line=6,
         vars={"a": "6", "b": "0"}, out=["6"], caption="MCD(48, 18) = 6",
         say="Imprime seis. El máximo común divisor de cuarenta y ocho y dieciocho es seis. Sin saber de antemano cuántas vueltas haría falta."),
    dict(type="slide", section=S_MATE, title="Fibonacci: mismo problema, distinto ciclo",
         bullets=["0, 1, 1, 2, 3, 5, 8, 13...  (cada uno es la suma de los dos anteriores)",
                  "\"Los primeros 15 términos\" → sabes cuántos → for",
                  "$ for i in range(15):",
                  "\"Los términos menores que 1000\" → no sabes cuántos → while",
                  "$ while a < 1000:",
                  "La pregunta del problema decide el ciclo, no el tema"],
         say="Un último ejemplo que lo resume todo: la sucesión de Fibonacci, donde cada número es la suma de los dos anteriores. "
             "Si te piden los primeros quince términos, sabes cuántos son, así que usas for. "
             "Si te piden todos los términos menores que mil, no sabes cuántos serán, así que usas while. "
             "Mismo tema, distinta pregunta, distinto ciclo. Lo que decide es la pregunta."),
]

CIERRE = [
    dict(type="slide", section="Resumen", title="Resumen",
         bullets=["if → algo pasa solo en cierto caso",
                  "if / else → 2 caminos",
                  "if / elif / else → 3 o más caminos, solo ocurre uno",
                  "for → sabes cuántas veces, o recorres una lista o un range",
                  "while → repites hasta que algo cambie",
                  "break → salir del ciclo ya"],
         say="Resumamos. If, para algo que pasa solo en cierto caso. If con else, para dos caminos. "
             "If, elif, else, para tres o más caminos donde solo ocurre uno. "
             "For, cuando sabes cuántas veces, o recorres una lista. While, cuando repites hasta que algo cambie. "
             "Y break, para salir de un ciclo en cuanto tienes la respuesta."),
    dict(type="title", title="¡Ahora a practicar!",
         subtitle="Abre Aprende_Python_desde_cero.ipynb en Jupyter, cambia los ejemplos y resuelve los ejercicios",
         say="Ahora te toca a ti. Abre tu notebook, Aprende Python desde cero, en Jupyter. "
             "Ejecuta cada ejemplo, cambia los números, rómpelo a propósito y arréglalo. "
             "Ahí encontrarás más ejercicios de matemáticas resueltos, y ejercicios para ti con sus soluciones. "
             "Programar se aprende programando. ¡Mucho éxito!"),
]

ESCENAS = INTRO + VARIABLES + IF + FOR + WHILE + GUIA + QUIZ + MATE + CIERRE
