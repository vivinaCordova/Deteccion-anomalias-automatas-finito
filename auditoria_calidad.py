
# ==================================================
# BLOQUE 8: AUDITORÍA DE CALIDAD DE LOS DATOS
# ==================================================

from collections import Counter

registros = datos_validacion + datos_prueba

cadenas = [
    registro["cadena"]
    for registro in registros
]

# --------------------------------------------------
# 1. DIVERSIDAD
# --------------------------------------------------

total_sesiones = len(cadenas)
cadenas_unicas = len(set(cadenas))

diversidad = (
    cadenas_unicas / total_sesiones * 100
)

print("1. DIVERSIDAD")
print(f"Total de sesiones: {total_sesiones}")
print(f"Cadenas únicas: {cadenas_unicas}")
print(f"Diversidad: {diversidad:.2f}%")


# --------------------------------------------------
# 2. LONGITUDES
# --------------------------------------------------

longitudes = [
    len(cadena)
    for cadena in cadenas
]

promedio = sum(longitudes) / len(longitudes)

print("\n2. LONGITUDES")
print(f"Mínima: {min(longitudes)}")
print(f"Máxima: {max(longitudes)}")
print(f"Promedio: {promedio:.2f}")


# --------------------------------------------------
# 3. FRECUENCIA DE EVENTOS
# --------------------------------------------------

frecuencias = Counter(
    simbolo
    for cadena in cadenas
    for simbolo in cadena
)

total_eventos = sum(frecuencias.values())

print("\n3. FRECUENCIA DE EVENTOS")

for simbolo in sorted(ALFABETO):
    print(
        f"{simbolo}: {frecuencias[simbolo]}"
    )

porcentaje_v = (
    frecuencias["V"] / total_eventos * 100
)

sesiones_con_v = sum(
    "V" in cadena
    for cadena in cadenas
)

print(f"Total de eventos: {total_eventos}")
print(f"Porcentaje de V: {porcentaje_v:.2f}%")
print(f"Sesiones con V: {sesiones_con_v}/350")


# --------------------------------------------------
# 4. COBERTURA DE PATRONES
# --------------------------------------------------

print("\n4. COBERTURA DE PATRONES")

cobertura = {}

for patron in ("P1", "P2", "P3", "P4"):

    cantidad = sum(
        detectar_patrones(cadena)[patron]
        for cadena in cadenas
    )

    cobertura[patron] = cantidad

    print(f"{patron}: {cantidad}")


# --------------------------------------------------
# 5. AUDITORÍA OPERATIVA ESTRICTA
# --------------------------------------------------

def revisar_coherencia_estricta(cadena):
    """
    Comprueba correspondencia solicitud-respuesta
    sin permitir excepciones.

    Un evento A o D debe responder a una S previa.
    """

    problemas = []
    autenticado = False
    solicitud_pendiente = False

    for posicion, simbolo in enumerate(cadena):

        if simbolo == "E":
            autenticado = True

        elif simbolo == "C":

            if not autenticado:
                problemas.append(
                    f"C sin sesión activa en {posicion}"
                )

            if solicitud_pendiente:
                problemas.append(
                    f"C con solicitud pendiente en {posicion}"
                )

            autenticado = False

        elif simbolo == "S":

            if solicitud_pendiente:
                problemas.append(
                    f"S con solicitud pendiente en {posicion}"
                )

            solicitud_pendiente = True

        elif simbolo in ("A", "D"):

            if not solicitud_pendiente:
                problemas.append(
                    f"{simbolo} sin solicitud en {posicion}"
                )

            else:
                solicitud_pendiente = False

    if solicitud_pendiente:
        problemas.append(
            "Solicitud sin respuesta al finalizar"
        )

    return problemas


observaciones_estrictas = []
observaciones_modelo = []

for registro in registros:

    cadena = registro["cadena"]
    categoria = registro["categoria"]

    # Evaluación sin excepciones
    problemas_estrictos = (
        revisar_coherencia_estricta(cadena)
    )

    if problemas_estrictos:

        observaciones_estrictas.append({
            "id_sesion": registro["id_sesion"],
            "cadena": cadena,
            "categoria": categoria,
            "problemas": problemas_estrictos
        })

    # Evaluación según las reglas del modelo
    problemas_modelo = comprobar_coherencia(
        cadena,
        categoria
    )

    if problemas_modelo:

        observaciones_modelo.append({
            "id_sesion": registro["id_sesion"],
            "cadena": cadena,
            "categoria": categoria,
            "problemas": problemas_modelo
        })


print("\n5. COHERENCIA OPERATIVA")

print(
    "Sesiones con observaciones estrictas:",
    len(observaciones_estrictas)
)

print(
    "Sesiones con observaciones según el modelo:",
    len(observaciones_modelo)
)


# --------------------------------------------------
# 6. ANÁLISIS DE LA EXCEPCIÓN P3
# --------------------------------------------------

casos_p3 = [
    registro
    for registro in registros
    if registro["categoria"] == "P3"
]

ids_p3 = {
    registro["id_sesion"]
    for registro in casos_p3
}

ids_observados = {
    registro["id_sesion"]
    for registro in observaciones_estrictas
}

observaciones_fuera_p3 = (
    ids_observados - ids_p3
)

print("\n6. ANÁLISIS DE P3")

print(
    f"Sesiones generadas como P3: {len(casos_p3)}"
)

print(
    "Observaciones estrictas fuera de P3:",
    len(observaciones_fuera_p3)
)

print(
    "Observaciones según el modelo:",
    len(observaciones_modelo)
)

# Ejemplos de la anomalía intencional
print("\nEJEMPLOS DE P3")

for registro in casos_p3[:3]:

    print(
        registro["id_sesion"],
        "|",
        registro["cadena"]
    )


# --------------------------------------------------
# 7. INTEGRIDAD DE ETIQUETAS
# --------------------------------------------------

errores_etiquetado = []

for registro in registros:

    etiqueta_calculada, patrones = (
        clasificar_sesion(registro["cadena"])
    )

    patrones_calculados = ",".join(
        patron
        for patron in ("P1", "P2", "P3")
        if patrones[patron]
    ) or "Ninguno"

    if (
        etiqueta_calculada != registro["etiqueta"]
        or patrones_calculados != registro["tipo_patron"]
    ):

        errores_etiquetado.append(
            registro["id_sesion"]
        )

print("\n7. INTEGRIDAD DE ETIQUETAS")

print(
    "Sesiones con errores de etiquetado:",
    len(errores_etiquetado)
)


# --------------------------------------------------
# 8. VERIFICACIÓN FINAL
# --------------------------------------------------

assert total_sesiones == 350
assert cadenas_unicas == 350

assert all(
    3 <= longitud <= 20
    for longitud in longitudes
)

assert cobertura["P1"] > 0
assert cobertura["P2"] > 0
assert cobertura["P3"] > 0
assert cobertura["P4"] > 0

assert len(observaciones_modelo) == 0
assert len(observaciones_fuera_p3) == 0
assert len(errores_etiquetado) == 0

# Comprobar la distribución prevista de anomalías
assert sum(
    registro["etiqueta"] == "anómala"
    for registro in datos_validacion
) == 54

assert sum(
    registro["etiqueta"] == "anómala"
    for registro in datos_prueba
) == 9

print("\n8. VERIFICACIÓN FINAL")

print("Cantidad y unicidad: CORRECTAS")
print("Longitudes: CORRECTAS")
print("Cobertura de patrones: CORRECTA")
print("Etiquetas: CORRECTAS")
print("Coherencia según el modelo: CORRECTA")
print("Excepción P3: IDENTIFICADA")
print("AUDITORÍA COMPLETADA")
