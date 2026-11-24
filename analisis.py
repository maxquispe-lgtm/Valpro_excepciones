# =========================================================
# TEAM06 - VALPRO
# FUNCIONES DE ANÁLISIS DE DATOS
#
# Yhandel Espinoza:
# - calcular_monto_total()
# - agrupar_por_categoria()
#
# Max Quispe:
# - contar_por_estado()
# - agrupar_por_area()
#
# Nicole Sánchez:
# - calcular_monto_promedio()
# - calcular_monto_por_categoria()
#
# Las demás funciones se utilizan como apoyo o complemento.
# =========================================================


# ---------------------------------------------------------
# IMPORTACIÓN DE FUNCIONES
# ---------------------------------------------------------

# Importamos obtener_datos() desde conexion_sheets.py
# para recuperar las solicitudes registradas en Google Sheets.
from conexion_sheets import obtener_datos


# ---------------------------------------------------------
# NICOLE SÁNCHEZ - FUNCIÓN COMPLEMENTARIA
# NORMALIZAR MONTOS
# ---------------------------------------------------------

def normalizar_monto(valor):
    """
    Convierte los montos provenientes de Google Sheets
    a números decimales para poder realizar cálculos.

    Ejemplos aceptados:
    200
    200.0
    "S/ 200,00"
    "S/ 1.200,50"
    """

    # isinstance() permite comprobar el tipo de dato.
    # Si el valor ya es entero o decimal, solo lo convertimos a float.
    if isinstance(valor, (int, float)):
        return float(valor)

    # str() convierte cualquier valor a texto.
    # strip() elimina espacios al inicio y al final.
    texto = str(valor).strip()

    # replace() elimina o reemplaza caracteres que no permiten
    # convertir directamente el monto a número.
    texto = texto.replace("S/", "")
    texto = texto.replace(" ", "")

    # Eliminamos el punto que se utiliza como separador de miles.
    texto = texto.replace(".", "")

    # Cambiamos la coma decimal por punto porque float()
    # utiliza el punto para reconocer números decimales.
    texto = texto.replace(",", ".")

    # Si después de limpiar el valor no queda ningún dato,
    # devolvemos cero.
    if texto == "":
        return 0.0

    try:
        # float() intenta convertir el texto limpio a número decimal.
        return float(texto)

    # Si Python no puede convertir el valor porque contiene
    # un formato incorrecto, devolvemos cero para evitar errores.
    except ValueError:
        return 0.0


# ---------------------------------------------------------
# YHANDEL ESPINOZA - FUNCIÓN COMPLEMENTARIA
# CONTAR SOLICITUDES
# ---------------------------------------------------------

def contar_solicitudes(registros):
    """
    Devuelve la cantidad total de solicitudes.
    """

    # len() cuenta cuántos registros existen dentro de la lista.
    return len(registros)


# ---------------------------------------------------------
# MAX QUISPE - FUNCIÓN PRINCIPAL 1
# AGRUPAR SOLICITUDES POR ESTADO
# ---------------------------------------------------------

# MAX - FUNCIÓN MEJORADA 2
def contar_por_estado(registros):
    if registros is None:
        raise ValueError("No se recibieron datos de Google Sheets.")
    if len(registros) == 0:
        return {}

    resumen = {}
    estados_validos = {"PENDIENTE FIRMA", "PENDIENTE JEFE", "PENDIENTE ADMIN.", "APROBADO", "RECHAZADO", "OBSERVADO", "CERRADO", "PENDIENTE", "SIN ESTADO"}

    for numero, registro in enumerate(registros, start=1):
        try:
            if not isinstance(registro, dict):
                raise TypeError("El registro no es un diccionario.")
            if "Estado" not in registro:
                raise KeyError("Falta el campo 'Estado'.")

            estado = str(registro.get("Estado", "")).strip().upper()
            if estado == "":
                estado = "SIN ESTADO"
            if estado not in estados_validos:
                raise ValueError(f"Estado inválido: {estado}")

            resumen[estado] = resumen.get(estado, 0) + 1

        except (KeyError, ValueError, TypeError) as e:
            print(f"Fila {numero} ignorada en contar_por_estado: {e}")
            continue
    return resumen


# ---------------------------------------------------------
# MAX QUISPE - FUNCIÓN COMPLEMENTARIA
# CONTAR UN ESTADO ESPECÍFICO
# ---------------------------------------------------------

def contar_estado(registros, estado_buscado):
    """
    Cuenta cuántas solicitudes tienen un estado específico.

    Por ejemplo:
    PENDIENTE FIRMA
    PENDIENTE JEFE
    APROBADO
    RECHAZADO
    """

    # Empezamos el contador en cero.
    total = 0

    # Recorremos todas las solicitudes.
    for registro in registros:

        # Obtenemos el estado de la solicitud.
        # upper() convierte el texto a mayúsculas para evitar
        # diferencias entre "Aprobado", "APROBADO" o "aprobado".
        estado = str(
            registro.get("Estado", "")
        ).strip().upper()

        # También convertimos el estado buscado a mayúsculas
        # para realizar una comparación uniforme.
        if estado == estado_buscado.upper():

            # Cada coincidencia aumenta el contador.
            total += 1

    return total


# ---------------------------------------------------------
# YHANDEL ESPINOZA - FUNCIÓN PRINCIPAL 1
# CALCULAR MONTO TOTAL
# ---------------------------------------------------------

# YHANDEL - FUNCIÓN MEJORADA 1
def calcular_monto_total(registros):
    if registros is None:
        raise ValueError("No se recibieron datos de Google Sheets.")
    if len(registros) == 0:
        return 0.0

    total = 0.0
    for numero, registro in enumerate(registros, start=1):
        try:
            if not isinstance(registro, dict):
                raise TypeError("El registro no es un diccionario.")
            if "Monto" not in registro:
                raise KeyError("Falta el campo 'Monto'.")

            monto = normalizar_monto(registro.get("Monto"))

            # Regla de Valpro: monto > 0 y hasta 200
            if monto <= 0 or monto > 200:
                raise ValueError(f"Monto inválido: {monto}. Debe ser mayor que 0 y hasta 200.")

            total += monto

        except (KeyError, ValueError, TypeError) as e:
            print(f"Fila {numero} ignorada en calcular_monto_total: {e}")
            continue
    return total


# ---------------------------------------------------------
# NICOLE SÁNCHEZ - FUNCIÓN PRINCIPAL 1
# CALCULAR MONTO PROMEDIO
# ---------------------------------------------------------

# NICOLE - FUNCIÓN MEJORADA 3
def calcular_monto_promedio(registros):
    if registros is None:
        raise ValueError("No se recibieron datos de Google Sheets.")
    if len(registros) == 0:
        return 0.0

    try:
        return calcular_monto_total(registros) / len(registros)
    except ZeroDivisionError:
        return 0.0


# ---------------------------------------------------------
# MAX QUISPE - FUNCIÓN PRINCIPAL 2
# AGRUPAR SOLICITUDES POR ÁREA
# ---------------------------------------------------------

def agrupar_por_area(registros):
    """
    Cuenta cuántas solicitudes existen en cada área.
    """

    resumen = {}

    # Recorremos cada solicitud.
    for registro in registros:

        # Obtenemos el área registrada en Google Sheets.
        area = str(
            registro.get("Área", "")
        ).strip()

        # Si el área está vacía, utilizamos un nombre genérico
        # para no perder ese registro durante el análisis.
        if area == "":
            area = "SIN ÁREA"

        # Creamos el área en el diccionario si todavía no existe.
        if area not in resumen:
            resumen[area] = 0

        # Sumamos una solicitud al área correspondiente.
        resumen[area] += 1

    return resumen


# ---------------------------------------------------------
# YHANDEL ESPINOZA - FUNCIÓN PRINCIPAL 2
# AGRUPAR SOLICITUDES POR CATEGORÍA
# ---------------------------------------------------------

def agrupar_por_categoria(registros):
    """
    Cuenta cuántas solicitudes existen en cada categoría.
    """

    resumen = {}

    for registro in registros:

        # Recuperamos la categoría de la solicitud.
        categoria = str(
            registro.get("Categoría", "")
        ).strip()

        # Si no existe categoría, la agrupamos como SIN CATEGORÍA.
        if categoria == "":
            categoria = "SIN CATEGORÍA"

        # Creamos la categoría si todavía no está en el diccionario.
        if categoria not in resumen:
            resumen[categoria] = 0

        # Incrementamos su contador.
        resumen[categoria] += 1

    return resumen


# ---------------------------------------------------------
# NICOLE SÁNCHEZ - FUNCIÓN PRINCIPAL 2
# CALCULAR MONTO POR CATEGORÍA
# ---------------------------------------------------------

def calcular_monto_por_categoria(registros):
    """
    Suma cuánto dinero se ha solicitado
    dentro de cada categoría.
    """

    resumen = {}

    for registro in registros:

        # Obtenemos la categoría correspondiente a la solicitud.
        categoria = str(
            registro.get("Categoría", "")
        ).strip()

        if categoria == "":
            categoria = "SIN CATEGORÍA"

        # Convertimos el monto a número mediante normalizar_monto().
        monto = normalizar_monto(
            registro.get("Monto", 0)
        )

        # Si la categoría todavía no existe en el diccionario,
        # la iniciamos con un monto de cero.
        if categoria not in resumen:
            resumen[categoria] = 0.0

        # Sumamos el monto de la solicitud
        # al total correspondiente a su categoría.
        resumen[categoria] += monto

    return resumen


# ---------------------------------------------------------
# MAX QUISPE - FUNCIÓN COMPLEMENTARIA
# OBTENER ESTADO PREDOMINANTE
# ---------------------------------------------------------

def obtener_estado_predominante(registros):
    """
    Devuelve el estado que aparece más veces
    junto con la cantidad de solicitudes.
    """

    # Reutilizamos contar_por_estado() para obtener
    # el resumen de solicitudes agrupadas por estado.
    resumen = contar_por_estado(registros)

    # Si no existen estados, devolvemos valores por defecto.
    if len(resumen) == 0:
        return "-", 0

    # max() busca el elemento con el valor más alto.
    #
    # key=resumen.get indica que la comparación se realiza
    # utilizando las cantidades almacenadas en el diccionario.
    estado = max(
        resumen,
        key=resumen.get
    )

    # Devolvemos dos resultados:
    # el nombre del estado y su cantidad.
    return estado, resumen[estado]


# ---------------------------------------------------------
# NICOLE SÁNCHEZ - FUNCIÓN COMPLEMENTARIA
# OBTENER ÁREA CON MÁS SOLICITUDES
# ---------------------------------------------------------

def obtener_area_mas_solicitudes(registros):
    """
    Devuelve el área que tiene más solicitudes
    junto con la cantidad correspondiente.
    """

    # Primero agrupamos las solicitudes por área.
    resumen = agrupar_por_area(registros)

    if len(resumen) == 0:
        return "-", 0

    # max() encuentra el área cuyo contador es mayor.
    area = max(
        resumen,
        key=resumen.get
    )

    return area, resumen[area]


# ---------------------------------------------------------
# YHANDEL ESPINOZA - FUNCIÓN COMPLEMENTARIA
# OBTENER CATEGORÍA MÁS UTILIZADA
# ---------------------------------------------------------

def obtener_categoria_mas_usada(registros):
    """
    Devuelve la categoría que aparece más veces
    junto con la cantidad correspondiente.
    """

    # Reutilizamos agrupar_por_categoria()
    # para obtener el conteo de cada categoría.
    resumen = agrupar_por_categoria(registros)

    if len(resumen) == 0:
        return "-", 0

    # max() encuentra la categoría con el valor más alto.
    categoria = max(
        resumen,
        key=resumen.get
    )

    return categoria, resumen[categoria]