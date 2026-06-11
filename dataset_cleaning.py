
import pandas as pd


# ==========================================================
# CONFIGURACIÓN DEL PROYECTO
# ==========================================================

INPUT_FILE = "nacidos_vivos.csv"
OUTPUT_FILE = "nacidos_vivos_limpio.csv"


# ==========================================================
# CONFIGURACIÓN DE COLUMNAS
# ==========================================================

REQUIRED_COLUMNS = {
    "Fecha_Nacimiento",
    "Departamento Nacimiento",
    "Municipio",
    "Area",
    "Sexo",
    "Tiempo_Gestación",
    "Tipo_Parto",
    "Multiplicidad_Embarazo",
    "Régimen_Seguridad_Social",
    "EPS",
    "Peso",
    "Periodo",
    "Edad_Madre",
    "Edad Padre",
    "Talla",
    "Hora_Nacimiento",
    "Número_Consultas_Prenatales"
}


TEXT_COLUMNS = {
    "Departamento Nacimiento": "string",
    "Municipio": "string",
    "Area": "string",
    "Sexo": "string",
    "Tipo_Parto": "string",
    "Multiplicidad_Embarazo": "string",
    "Régimen_Seguridad_Social": "string",
    "EPS": "string",
}


PARSE_DATE_COLUMNS = [
    "Fecha_Nacimiento"
]


# ==========================================================
# NORMALIZACIÓN EPS
# ==========================================================

EPS_MAPPING = {
    "A.R.S. CONVIDA": "CONVIDA",
    "ASMET SALUD EPS SAS": "ASMET SALUD",
    "ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD E.S.S": "MUTUAL SER",
    "CAJA DE COMPENSACION FAMILIAR  CAJACOPI ATLANTICO": "CAJACOPI",
    "CAPITAL SALUD E.P.S.": "CAPITAL SALUD",
    "COMFAORIENTE": "COMFAORIENTE",
    "COOSALUD -CM": "COOSALUD",
    "COOSALUD E.S.S.": "COOSALUD",
    "COOSALUD E.S.S. -CM": "COOSALUD",
    "COOSALUD ENTIDAD PROMOTORA DE SALUD S.A.": "COOSALUD",
    "E.P.S. SANITAS": "SANITAS",
    "EPS SANITAS - CM": "SANITAS",
    "EMPRESA PROMOTORA DE SALUD ECOOPSOS EPS S.A.S.": "ECOOPSOS",
    "EPS Y MEDICINA PREPAGADA SURAMERICANA S.A": "SURAMERICANA",
    "FAMISANAR E.P.S. LTDA - CAFAM - COLSUBSIDIO": "COLSUBSIDIO",
    "FAMISANAR E.P.S. LTDA - CAFAM - COLSUBSIDIO -CM": "COLSUBSIDIO",
    "FUERZAS MILITARES": "FUERZAS MILITARES",
    "FUNDACION SALUD MIA EPS": "SALUD MIA",
    "MAGISTERIO": "MAGISTERIO",
    "NO ASEGURADO": "NO ASEGURADO",
    "NUEVA EPS S.A.": "NUEVA EPS",
    "NUEVA EPS S.A. -CM": "NUEVA EPS",
    "POLICIA NACIONAL": "POLICIA NACIONAL",
    "SALUD TOTAL E.P.S. -CM": "SALUD TOTAL",
    "SALUD TOTAL S.A.": "SALUD TOTAL"
}


# ==========================================================
# FUNCIONES DE CARGA Y VALIDACIÓN
# ==========================================================

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Carga el dataset original.
    """

    try:

        dataframe = pd.read_csv(
            file_path,
            parse_dates=PARSE_DATE_COLUMNS,
            dtype=TEXT_COLUMNS
        )

        return dataframe

    except FileNotFoundError:

        raise FileNotFoundError(
            f"No existe el archivo: {file_path}"
        )

    except pd.errors.ParserError:

        raise ValueError(
            "El archivo no tiene un formato CSV válido."
        )


def validate_structure(
    dataframe: pd.DataFrame,
    required_columns: set
) -> None:
    """
    Valida que existan
    todas las columnas requeridas.
    """

    missing_columns = (
        required_columns
        - set(dataframe.columns)
    )

    if missing_columns:

        raise ValueError(
            f"Columnas faltantes: "
            f"{sorted(missing_columns)}"
        )


# ==========================================================
# LIMPIEZA DE DATOS
# ==========================================================

def clean_data(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Limpia y transforma
    el dataset.
    """

    # ------------------------------------------------------
    # Correccion y conversión de tipos
    # ------------------------------------------------------

    dataframe["Peso"] = (
        dataframe["Peso"]
        .astype(str)
        .str.replace(",", ".")
        .astype("float64")
    )

    dataframe["Periodo"] = (
        dataframe["Periodo"]
        .astype(str)
        .str.replace(",", "")
        .astype("int64")
    )

    # ------------------------------------------------------
    # Normalización de EPS
    # ------------------------------------------------------

    dataframe["EPS_NORMALIZADA"] = (
        dataframe["EPS"]
        .replace(EPS_MAPPING)
    )

    # ------------------------------------------------------
    # Rango de edad materna
    # ------------------------------------------------------

    bins_maternal_age = [
        0,
        20,
        35,
        float("inf")
    ]

    labels_maternal_age = [
        "Adolescente",
        "Edad reproductiva óptima",
        "Edad materna avanzada"
    ]

    dataframe[
        "RANGO_EDAD_MATERNA"
    ] = pd.cut(
        dataframe["Edad_Madre"],
        bins=bins_maternal_age,
        labels=labels_maternal_age,
        right=False
    )

    # ------------------------------------------------------
    # Grupo edad gestacional
    # ------------------------------------------------------

    bins_gestation = [
        0,
        28,
        32,
        37,
        42,
        float("inf")
    ]

    labels_gestation = [
        "Prematuro extremo",
        "Muy prematuro",
        "Prematuro moderado a tardío",
        "A término",
        "Postérmino"
    ]

    dataframe[
        "grupo_edad_gestacional"
    ] = pd.cut(
        dataframe["Tiempo_Gestación"],
        bins=bins_gestation,
        labels=labels_gestation,
        right=False
    )

    # ------------------------------------------------------
    # Conversión de talla
    # ------------------------------------------------------

    dataframe["Talla"] = (
        dataframe["Talla"]
        .astype(str)
        .str.replace(",", ".")
    )

    dataframe["Talla"] = pd.to_numeric(
        dataframe["Talla"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # Índice ponderal neonatal
    # ------------------------------------------------------

    dataframe[
        "INDICE_PONDERAL"
    ] = (
        dataframe["Peso"] * 100
    ) / (
        dataframe["Talla"] ** 3
    )

    # ------------------------------------------------------
    # Clasificación del índice ponderal
    # ------------------------------------------------------

    bins_ponderal = [
        0,
        2.2,
        3.0,
        float("inf")
    ]

    labels_ponderal = [
        "Bajo / Asimétrico",
        "Normal / Armónico",
        "Alto / Macrosómico"
    ]

    dataframe[
        "CATEGORIA_INDICE_PONDERAL"
    ] = pd.cut(
        dataframe[
            "INDICE_PONDERAL"
        ],
        bins=bins_ponderal,
        labels=labels_ponderal,
        right=False
    )


    



    # ------------------------------------------------------
    # Fecha estimada de concepción
    # ------------------------------------------------------

    dataframe[
        "FECHA_CONCEPCION_ESTIMADA"
    ] = (
        dataframe["Fecha_Nacimiento"]
        - pd.to_timedelta(
            dataframe["Tiempo_Gestación"] * 7,
            unit="D",
            errors="coerce"
        )
        + pd.Timedelta(days=14)
    )

    dataframe[
        "anio_concepcion"
    ] = (
        dataframe[
            "FECHA_CONCEPCION_ESTIMADA"
        ]
        .dt.isocalendar()
        .year
    )

    dataframe[
        "semana_concepcion"
    ] = (
        dataframe[
            "FECHA_CONCEPCION_ESTIMADA"
        ]
        .dt.isocalendar()
        .week
    )

    return dataframe


# ==========================================================
# EXPORTACIÓN
# ==========================================================

def export_dataset(
    dataframe: pd.DataFrame,
    output_file: str
) -> None:
    """
    Exporta el dataset limpio.
    """

    dataframe.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main() -> None:

    dataframe = load_dataset(
        INPUT_FILE
    )

    validate_structure(
        dataframe,
        REQUIRED_COLUMNS
    )

    dataframe = clean_data(
        dataframe
    )

    export_dataset(
        dataframe,
        OUTPUT_FILE
    )

    print(
        "Dataset limpio generado correctamente."
    )


if __name__ == "__main__":

    main()

