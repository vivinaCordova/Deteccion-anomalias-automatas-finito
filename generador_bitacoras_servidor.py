"""9.2. Verificación de integridad de los registros.

Se comprueba que las 350 sesiones conserven sus cadenas originales después
de transformarlas en registros de eventos.

La verificación compara el orden de los símbolos, las etiquetas, los patrones
y la correspondencia entre eventos, garantizando que los datos no se alteren
antes de exportarlos a CSV.
"""


# ==================================================
# BLOQUE 9.2: VERIFICACIÓN DE INTEGRIDAD DEL CSV
# ==================================================

def verificar_integridad(df, sesiones, nombre):

    print(f"\nVERIFICACIÓN: {nombre.upper()}")

    errores = []

    for sesion in sesiones:

        id_sesion = sesion["id_sesion"]

        filas = df[
            df["id_sesion"] == id_sesion
        ].sort_values(["fecha_hora", "id_evento"])

        # Reconstruir la cadena original
        reconstruida = "".join(filas["simbolo"])

        if reconstruida != sesion["cadena"]:
            errores.append(id_sesion)

        # Comprobar etiqueta y patrón
        if not (filas["etiqueta"] == sesion["etiqueta"]).all():
            errores.append(id_sesion)

        if not (filas["tipo_patron"] == sesion["tipo_patron"]).all():
            errores.append(id_sesion)

        # Comprobar correspondencia símbolo-evento
        for _, fila in filas.iterrows():
            if EVENTOS[fila["simbolo"]] != fila["evento"]:
                errores.append(id_sesion)

    print("Sesiones verificadas:", len(sesiones))
    print("Sesiones con errores:", len(set(errores)))

    assert not errores

    print("Reconstrucción de cadenas: CORRECTA")
    print("Etiquetas y patrones: CORRECTOS")
    print("Correspondencia de eventos: CORRECTA")


verificar_integridad(
    df_validacion,
    datos_validacion,
    "Validación"
)

verificar_integridad(
    df_prueba_completa,
    datos_prueba,
    "Prueba"
)




""" 9.3. Exportación de los archivos CSV

Se exportan los conjuntos de validación y prueba, manteniendo las etiquetas del conjunto de prueba en un archivo independiente.
Esta separación permite evaluar el monitor sin proporcionarle previamente las respuestas correctas."""

# ==================================================
# BLOQUE 9.3: EXPORTACIÓN DE ARCHIVOS CSV
# ==================================================

from pathlib import Path
from google.colab import files

# Carpeta de salida
CARPETA = Path("/content/datos")
CARPETA.mkdir(parents=True, exist_ok=True)

# 1. Validación: contiene etiquetas
validacion_csv = df_validacion.copy()

# 2. Prueba: eliminar etiquetas y patrones
prueba_csv = df_prueba_completa.drop(
    columns=["etiqueta", "tipo_patron"]
).copy()

# 3. Clave: una respuesta por sesión
clave_prueba_csv = (
    df_prueba_completa[
        ["id_sesion", "etiqueta", "tipo_patron"]
    ]
    .drop_duplicates(subset=["id_sesion"])
    .reset_index(drop=True)
)

# Guardar los archivos
validacion_csv.to_csv(
    CARPETA / "validacion.csv",
    index=False,
    encoding="utf-8-sig"
)

prueba_csv.to_csv(
    CARPETA / "prueba.csv",
    index=False,
    encoding="utf-8-sig"
)

clave_prueba_csv.to_csv(
    CARPETA / "clave_prueba.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==================================================
# COMPROBACIONES DE EXPORTACIÓN
# ==================================================

assert validacion_csv["id_sesion"].nunique() == 300
assert prueba_csv["id_sesion"].nunique() == 50
assert len(clave_prueba_csv) == 50

assert "etiqueta" not in prueba_csv.columns
assert "tipo_patron" not in prueba_csv.columns

assert set(prueba_csv["id_sesion"]) == set(
    clave_prueba_csv["id_sesion"]
)

print("EXPORTACIÓN COMPLETADA\n")

for nombre in [
    "validacion.csv",
    "prueba.csv",
    "clave_prueba.csv"
]:
    ruta = CARPETA / nombre

    assert ruta.exists()

    print(f"{nombre}: GUARDADO")

print("\nVERIFICACIÓN FINAL: CORRECTA")

# Descargar los tres archivos
for nombre in [
    "validacion.csv",
    "prueba.csv",
    "clave_prueba.csv"
]:
    files.download(str(CARPETA / nombre))
