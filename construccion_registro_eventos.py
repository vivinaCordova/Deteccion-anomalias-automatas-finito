# ==================================================
# BLOQUE 9: CONSTRUCCIÓN DE REGISTROS DE EVENTOS
# ==================================================

import pandas as pd
from datetime import datetime, timedelta

FECHA_INICIAL = datetime(2026, 10, 20, 8, 0, 0)

def construir_bitacora(sesiones, prefijo_actor):
    """Transforma las cadenas en registros de eventos."""

    filas = []
    contador_eventos = 1

    for indice, sesion in enumerate(sesiones):

        id_sesion = sesion["id_sesion"]
        actor = f"{prefijo_actor}-{indice + 1:04d}"

        # Cada sesión inicia en un momento diferente
        inicio = FECHA_INICIAL + timedelta(
            minutes=indice * 5
        )

        for posicion, simbolo in enumerate(sesion["cadena"]):

            fecha_hora = inicio + timedelta(
                seconds=posicion * 3
            )

            filas.append({
                "id_evento": contador_eventos,
                "fecha_hora": fecha_hora.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "id_sesion": id_sesion,
                "actor": actor,
                "evento": EVENTOS[simbolo],
                "simbolo": simbolo,
                "etiqueta": sesion["etiqueta"],
                "tipo_patron": sesion["tipo_patron"]
            })

            contador_eventos += 1

    return pd.DataFrame(filas)


# Construir registros de ambos conjuntos
df_validacion = construir_bitacora(
    datos_validacion, "USR"
)

df_prueba_completa = construir_bitacora(
    datos_prueba, "TST"
)

print("REGISTROS DE BITÁCORAS GENERADOS\n")

print("Validación:")
print("Eventos:", len(df_validacion))
print("Sesiones:", df_validacion["id_sesion"].nunique())

print("\nPrueba:")
print("Eventos:", len(df_prueba_completa))
print("Sesiones:", df_prueba_completa["id_sesion"].nunique())

# Comprobaciones
assert df_validacion["id_sesion"].nunique() == 300
assert df_prueba_completa["id_sesion"].nunique() == 50

assert len(df_validacion) == sum(
    len(s["cadena"]) for s in datos_validacion
)

assert len(df_prueba_completa) == sum(
    len(s["cadena"]) for s in datos_prueba
)

print("\nVERIFICACIÓN: CORRECTA")

# Mostrar únicamente cinco registros
display(df_validacion.head(5))
