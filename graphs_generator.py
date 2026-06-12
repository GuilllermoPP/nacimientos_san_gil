
import os
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

DATASET_FILE = "nacidos_vivos_limpio.csv"
GRAPH_FOLDER = "Graficas"


# ==========================================================
# UTILIDADES
# ==========================================================

def create_graph_folder(
    folder_path: str
) -> None:
    """
    Crea la carpeta donde se
    almacenarán las gráficas.
    """

    os.makedirs(
        folder_path,
        exist_ok=True
    )


def load_dataset(
    file_path: str
) -> pd.DataFrame:
    """
    Carga el dataset limpio.
    """

    return pd.read_csv(
        file_path
    )


def save_figure(
    figure,
    file_name: str
) -> None:
    """
    Guarda la gráfica.
    """

    create_graph_folder(
        GRAPH_FOLDER
    )

    file_path = os.path.join(
        GRAPH_FOLDER,
        file_name
    )

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(
        figure
    )


# ==========================================================
# GRÁFICO DE DISPERSIÓN (2 VARIABLES)
# ==========================================================

def generate_scatter_plot(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = None
) -> None:
    """
    Genera gráfico de dispersión
    entre dos variables.
    """

    figure, axis = plt.subplots()

    axis.scatter(
        dataframe[x_column],
        dataframe[y_column]
    )

    axis.set_xlabel(
        x_column
    )

    axis.set_ylabel(
        y_column
    )

    if title:

        axis.set_title(
            title
        )

    file_name = (
        f"scatter_"
        f"{x_column}_"
        f"{y_column}.png"
    )

    save_figure(
        figure,
        file_name
    )


# ==========================================================
# GRÁFICO DE DISPERSIÓN (3 VARIABLES)
# ==========================================================

def generate_grouped_scatter_plot(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str,
    category_column: str,
    title: str = None
) -> None:
    """
    Gráfico de dispersión
    agrupado por categoría.
    """

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    categories = (
        dataframe[
            category_column
        ]
        .dropna()
        .unique()
    )

    for category in categories:

        subset = dataframe[
            dataframe[
                category_column
            ] == category
        ]

        axis.scatter(
            subset[x_column],
            subset[y_column],
            label=str(category),
            alpha=0.7
        )

    axis.set_xlabel(
        x_column
    )

    axis.set_ylabel(
        y_column
    )

    if title:

        axis.set_title(
            title
        )

    axis.legend(
        title=category_column
    )

    file_name = (
        f"scatter_"
        f"{x_column}_"
        f"{y_column}_"
        f"{category_column}.png"
    )

    save_figure(
        figure,
        file_name
    )


# ==========================================================
# GRÁFICO DE BARRAS
# ==========================================================

def generate_bar_plot(
    dataframe: pd.DataFrame,
    category_column: str,
    value_column: str = None,
    aggregation: str = "count",
    title: str = None
) -> None:
    """
    Genera gráfico de barras.
    """

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    # -----------------------------------------
    # UNA VARIABLE
    # -----------------------------------------

    if value_column is None:

        result = (
            dataframe[
                category_column
            ]
            .value_counts()
        )

    # -----------------------------------------
    # DOS VARIABLES
    # -----------------------------------------

    else:

        grouped = (
            dataframe
            .groupby(
                category_column
            )[value_column]
        )

        if aggregation == "sum":

            result = grouped.sum()

        elif aggregation == "mean":

            result = grouped.mean()

        elif aggregation == "median":

            result = grouped.median()

        elif aggregation == "count":

            result = grouped.count()

        else:

            raise ValueError(
                "Agregación inválida."
            )

    result.plot.bar(
        ax=axis
    )

    axis.set_xlabel(
        category_column
    )

    axis.set_ylabel(
        aggregation
    )

    if title:

        axis.set_title(
            title
        )

    file_name = (
        f"bar_"
        f"{category_column}.png"
    )

    save_figure(
        figure,
        file_name
    )


# ==========================================================
# GRÁFICO DE BARRAS AGRUPADOS
# ==========================================================

def generate_grouped_bar_plot(
    dataframe: pd.DataFrame,
    category_column_1: str,
    category_column_2: str,
    normalize: bool = False,
    title: str = None
) -> None:
    """
    Genera gráfico de barras agrupadas
    entre dos variables categóricas.

    Parámetros:
    ----------
    category_column_1:
        Categoría principal
        (eje X).

    category_column_2:
        Categorías agrupadas
        dentro de cada barra.

    normalize:
        Si True, muestra proporciones
        porcentuales en lugar de
        frecuencias absolutas.
    """

    figure, axis = plt.subplots(
        figsize=(12, 6)
    )

    # -----------------------------------------
    # TABLA DE CONTINGENCIA
    # -----------------------------------------

    result = pd.crosstab(
        dataframe[
            category_column_1
        ],
        dataframe[
            category_column_2
        ],
        normalize="index"
        if normalize
        else False
    )

    # Convertir a porcentaje
    if normalize:

        result *= 100

    # -----------------------------------------
    # GRÁFICA
    # -----------------------------------------

    result.plot.bar(
        ax=axis
    )

    axis.set_xlabel(
        category_column_1
    )

    axis.set_ylabel(
        "Porcentaje"
        if normalize
        else "Frecuencia"
    )

    axis.tick_params(
        axis="x",
        rotation=45
    )

    axis.legend(
        title=category_column_2
    )

    if title:

        axis.set_title(
            title
        )

    file_name = (
        f"grouped_bar_"
        f"{category_column_1}_"
        f"{category_column_2}.png"

    )

    save_figure(
        figure,
        file_name
    )





# ==========================================================
# GRÁFICO DE CAJA Y BIGOTES
# ==========================================================

def generate_boxplot_vertical(
    dataframe: pd.DataFrame,
    numeric_column: str,
    category_column: str = None,
    title: str = None
) -> None:
    """
    Genera gráfico de caja
    y bigotes.
    """

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    # -----------------------------------------
    # UNA VARIABLE
    # -----------------------------------------

    if category_column is None:

        axis.boxplot(
            dataframe[
                numeric_column
            ].dropna()
        )

        axis.set_ylabel(
            numeric_column
        )

    # -----------------------------------------
    # AGRUPADO
    # -----------------------------------------

    else:

        dataframe.boxplot(
            column=numeric_column,
            by=category_column,
            ax=axis
        )

        plt.suptitle("")

    if title:

        axis.set_title(
            title
        )

    file_name = (
        f"boxplot_"
        f"{numeric_column}.png"
    )

    save_figure(
        figure,
        file_name
    )



def generate_boxplot_horizontal(
    dataframe: pd.DataFrame,
    numeric_column: str,
    category_column: str = None,
    title: str = None
) -> None:
    """
    Genera gráfico de caja
    y bigotes horizontal.
    """

    num_categories = (
        dataframe[
            category_column
        ].nunique()
    )

    figure, axis = plt.subplots(
        figsize=(
            10,
            max(
                6,
                num_categories * 0.4
            )
        )
    )

    dataframe.boxplot(
        column=numeric_column,
        by=category_column,
        ax=axis,
        vert=False
    )

    plt.suptitle("")

    axis.set_xlabel(
        numeric_column
    )

    axis.set_ylabel(
        category_column
    )

    if title:

        axis.set_title(
            title
        )

    file_name = (
        f"boxplot_horizontal_"
        f"{numeric_column}_"
        f"{category_column}.png"
    )

    save_figure(
        figure,
        file_name
    )




# ==========================================================
# EJEMPLO DE USO
# ==========================================================

if __name__ == "__main__":

    borns = load_dataset(
        DATASET_FILE
    )

    generate_scatter_plot(
        borns,
        x_column="Tiempo_Gestación",
        y_column="Peso",
        title="Tiempo de Gestación vs Peso"
    )

    generate_grouped_scatter_plot(
        borns,
        x_column="Tiempo_Gestación",
        y_column="Peso",
        category_column="RANGO_EDAD_MATERNA",
        title="Gestación vs Peso por Rango edad materna"
    )

    generate_bar_plot(
        borns,
        category_column="EPS_NORMALIZADA"
    )

    generate_boxplot_vertical(
        borns,
        numeric_column="Peso",
        category_column="RANGO_EDAD_MATERNA"
    )

    generate_boxplot_horizontal(
        borns,
        numeric_column="Número_Consultas_Prenatales",
        category_column="EPS_NORMALIZADA"
    )

    generate_boxplot_vertical(
        borns,
        numeric_column="Número_Consultas_Prenatales",
        category_column="Régimen_Seguridad_Social"
    )

    generate_scatter_plot(
        borns,
        x_column="Edad_Madre",
        y_column="INDICE_PONDERAL",
        
        title="Gestación vs IP por Rango edad materna"
    )

    generate_grouped_bar_plot(
        dataframe=borns,
        category_column_1="RANGO_EDAD_MATERNA",
        category_column_2="CATEGORIA_INDICE_PONDERAL",
        title="Índice ponderal por rango de edad materna"
    )

    generate_grouped_bar_plot(
    dataframe=borns,
    category_column_1="RANGO_EDAD_MATERNA",
    category_column_2="CATEGORIA_INDICE_PONDERAL",
    
    title="Distribución porcentual del índice ponderal por edad materna"
    )