import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# CONSTANTES DEL PROYECTO
# ==========================================================

# Nombre del archivo limpio que será utilizado
# durante todo el proyecto.
BORN_LIVE_FILE = "nacidos_vivos_limpio.csv"


# Conjunto de columnas obligatorias.
# Si alguna de estas columnas no existe,
# el programa debe detenerse porque los
# análisis posteriores dependen de ellas.
REQUIRED_COLUMNS = {
    "Periodo",
    "Departamento Nacimiento",
    "Municipio",
    "Area",
    "Sexo",
    "Peso",
    "Talla",
    "Fecha_Nacimiento",
    "Hora_Nacimiento",
    "Tiempo_Gestación",
    "Número_Consultas_Prenatales",
    "Tipo_Parto",
    "Multiplicidad_Embarazo",
    "Edad_Madre",
    "Régimen_Seguridad_Social",
    "EPS",
    "Edad Padre",
    "EPS_NORMALIZADA",
    "RANGO_EDAD_MATERNA",
    "grupo_edad_gestacional",
    "FECHA_CONCEPCION_ESTIMADA",
    "anio_concepcion",
    "semana_concepcion"
}


# ==========================================================
# FUNCIONES DE CARGA Y VALIDACIÓN
# ==========================================================

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Carga el archivo CSV limpio.

    Parámetros:
        file_path:
            Ruta del archivo CSV.

    Retorna:
        pd.DataFrame con los datos cargados.
    """

    try:

        dataframe = pd.read_csv(
            file_path
        )

        return dataframe

    except FileNotFoundError:

        raise FileNotFoundError(
            f"No existe el archivo: {file_path}"
        )

    except pd.errors.ParserError:

        raise ValueError(
            "El archivo CSV posee errores de formato."
        )


def validate_structure(
    dataframe: pd.DataFrame,
    required_columns: set
) -> None:
    """
    Verifica que todas las columnas necesarias
    existan dentro del DataFrame.

    Parámetros:
        dataframe:
            DataFrame a validar.

        required_columns:
            Conjunto de columnas obligatorias.
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


def load_and_validate_dataset() -> pd.DataFrame:
    """
    Función auxiliar encargada de:

    1. Cargar el dataset.
    2. Validar su estructura.
    3. Retornar el DataFrame listo
       para análisis.

    Retorna:
        pd.DataFrame
    """

    dataframe = load_dataset(
        BORN_LIVE_FILE
    )

    validate_structure(
        dataframe,
        REQUIRED_COLUMNS
    )

    return dataframe

# ==========================================================
# FUNCIONES ESTADÍSTICAS
# ==========================================================

def calculate_average_birth_weight(
    dataframe: pd.DataFrame
) -> float:
    """
    Calcula el peso promedio
    de los recién nacidos.
    """

    return dataframe["Peso"].mean()


def calculate_average_mother_age(
    dataframe: pd.DataFrame
) -> float:
    """
    Calcula la edad promedio
    de las madres.
    """

    return dataframe["Edad_Madre"].mean()


def calculate_average_father_age(
    dataframe: pd.DataFrame
) -> float:
    """
    Calcula la edad promedio
    de los padres.
    """

    return dataframe["Edad Padre"].mean()


def calculate_average_gestation_time(
    dataframe: pd.DataFrame
) -> float:
    """
    Calcula el tiempo promedio
    de gestación.
    """

    return dataframe[
        "Tiempo_Gestación"
    ].mean()


# ==========================================================
# FUNCIONES DE DISTRIBUCIÓN
# ==========================================================

def count_births_by_sex(
    dataframe: pd.DataFrame
) -> pd.Series:
    """
    Cuenta los nacimientos
    según el sexo.
    """

    return dataframe[
        "Sexo"
    ].value_counts()


def count_births_by_area(
    dataframe: pd.DataFrame
) -> pd.Series:
    """
    Cuenta los nacimientos
    según el área.
    """

    return dataframe[
        "Area"
    ].value_counts()


def count_births_by_eps(
    dataframe: pd.DataFrame
) -> pd.Series:
    """
    Cuenta los nacimientos
    por EPS normalizada.
    """

    return dataframe[
        "EPS_NORMALIZADA"
    ].value_counts()


def count_births_by_maternal_age_group(
    dataframe: pd.DataFrame
) -> pd.Series:
    """
    Cuenta los nacimientos
    según rango de edad materna.
    """

    return dataframe[
        "RANGO_EDAD_MATERNA"
    ].value_counts()


def count_births_by_gestational_group(
    dataframe: pd.DataFrame
) -> pd.Series:
    """
    Cuenta los nacimientos
    según grupo de edad gestacional.
    """

    return dataframe[
        "grupo_edad_gestacional"
    ].value_counts()

# ==========================================================
# FUNCIONES DE CONSULTA
# ==========================================================

def find_most_common_eps(
    dataframe: pd.DataFrame
) -> str:
    """
    Obtiene la EPS más frecuente.
    """

    return dataframe[
        "EPS_NORMALIZADA"
    ].mode()[0]


def find_most_common_delivery_type(
    dataframe: pd.DataFrame
) -> str:
    """
    Obtiene el tipo de parto
    más frecuente.
    """

    return dataframe[
        "Tipo_Parto"
    ].mode()[0]


def find_most_common_area(
    dataframe: pd.DataFrame
) -> str:
    """
    Obtiene el área con mayor
    cantidad de nacimientos.
    """

    return dataframe[
        "Area"
    ].mode()[0]


# ==========================================================
# FUNCIONES DE PORCENTAJES
# ==========================================================

def calculate_cesarean_percentage(
    dataframe: pd.DataFrame
) -> float:
    """
    Calcula el porcentaje
    de cesáreas.
    """

    total_births = len(
        dataframe
    )

    cesarean_births = len(
        dataframe[
            dataframe["Tipo_Parto"]
            == "CESAREA"
        ]
    )

    return (
        cesarean_births
        / total_births
    ) * 100


def calculate_multiple_pregnancy_percentage(
    dataframe: pd.DataFrame
) -> float:
    """
    Calcula el porcentaje
    de embarazos dobles.
    """

    total_births = len(
        dataframe
    )

    multiple_births = len(
        dataframe[
            dataframe[
                "Multiplicidad_Embarazo"
            ] == "DOBLE"
        ]
    )

    return (
        multiple_births
        / total_births
    ) * 100


# ==========================================================
# FUNCIONES DE GRÁFICAS
# ==========================================================

def generate_scatter_gestation_weight(
    dataframe: pd.DataFrame
) -> None:
    """
    Genera la gráfica
    Tiempo de Gestación vs Peso.
    """

    figure, axis = plt.subplots()

    axis.scatter(
        dataframe["Tiempo_Gestación"],
        dataframe["Peso"]
    )

    axis.set_xlabel(
        "Tiempo de Gestación"
    )

    axis.set_ylabel(
        "Peso"
    )

    axis.set_title(
        "Tiempo de Gestación vs Peso"
    )

    plt.show()


def generate_conception_pattern_graph(
    dataframe: pd.DataFrame
) -> None:
    """
    Genera la gráfica de
    concepciones estimadas
    por semana del año.
    """

    conception_pattern = (
        dataframe
        .groupby(
            [
                "anio_concepcion",
                "semana_concepcion"
            ]
        )
        .size()
        .reset_index(
            name="cantidad"
        )
    )

    plt.figure(figsize=(16, 7))

    # ==========================
    # Líneas por año
    # ==========================
    for year in sorted(
        conception_pattern[
            "anio_concepcion"
        ].unique()
    ):

        year_data = conception_pattern[
            conception_pattern[
                "anio_concepcion"
            ] == year
        ].sort_values(
            "semana_concepcion"
        )

        plt.plot(
            year_data[
                "semana_concepcion"
            ],
            year_data[
                "cantidad"
            ],
            marker="o",
            label=str(year)
        )

    # ==========================
    # Eventos resaltados
    # ==========================
    highlighted_periods = [
        {
            "start": 51,
            "end": 53,
            "label": "Navidad - Año Nuevo",
            "color": "red"
        },
        {
            "start": 1,
            "end": 2,
            "label": None,
            "color": "red"
        },
        {
            "start": 12,
            "end": 16,
            "label": "Semana Santa",
            "color": "gold"
        },
        {
            "start": 24,
            "end": 29,
            "label": "Vacaciones mitad de año",
            "color": "green"
        },
        {
            "start": 37,
            "end": 38,
            "label": "Amor y Amistad",
            "color": "purple"
        },
        {
            "start": 44,
            "end": 45,
            "label": "Ferias San Gil",
            "color": "orange"
        }
    ]

    for period in highlighted_periods:
        plt.axvspan(
            period["start"],
            period["end"],
            color=period["color"],
            alpha=0.15,
            label=period["label"]
        )

    # ==========================
    # Configuración gráfica
    # ==========================
    plt.title(
        "Concepciones estimadas por semana del año"
    )

    plt.xlabel(
        "Semana"
    )

    plt.ylabel(
        "Cantidad de concepciones"
    )

    plt.xticks(
        range(1, 54, 2)
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend(
        title="Año",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    plt.tight_layout()

    plt.show()