
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
    title: str = None,
    show_labels: bool = True
) -> None:
    """
    Genera gráfico de barras
    con etiquetas de datos.
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

    # Crear gráfico
    result.plot.bar(
        ax=axis
    )

    # -----------------------------------------
    # ETIQUETAS DE DATOS
    # -----------------------------------------

    if show_labels:

        for container in axis.containers:

            # Formato automático
            if aggregation in [
                "mean",
                "median"
            ]:
                labels = [
                    f"{v:.2f}"
                    for v in result.values
                ]

            else:
                labels = [
                    f"{int(v):,}"
                    for v in result.values
                ]

            axis.bar_label(
                container,
                labels=labels,
                padding=3
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

    figure.tight_layout()

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
    title: str = None,
    show_labels: bool = True
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

    show_labels:
        Si True, agrega etiquetas
        sobre cada barra.
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

    # -----------------------------------------
    # ETIQUETAS DE DATOS
    # -----------------------------------------

    if show_labels:

        for container in axis.containers:

            labels = []

            for bar in container:

                value = bar.get_height()

                # Ocultar ceros
                if value == 0:
                    labels.append("")

                # Porcentaje
                elif normalize:
                    labels.append(
                        f"{value:.1f}%"
                    )

                # Frecuencia
                else:
                    labels.append(
                        f"{int(value):,}"
                    )

            axis.bar_label(
                container,
                labels=labels,
                padding=3,
                fontsize=8
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

    figure.tight_layout()

    file_name = (
        f"grouped_bar_"
        f"{category_column_1}_"
        f"{category_column_2}_"
        f"normalize_{normalize}.png"
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
    title: str = None,
    ascending: bool = True
) -> None:
    """
    Genera gráfico de caja y bigotes horizontal,
    ordenado por el promedio de la variable numérica.
    
    Parameters
    ----------
    ascending : bool
        True = menor a mayor promedio
        False = mayor a menor promedio
    """

    df = dataframe.copy()

    # Ordenar categorías por promedio
    category_order = (
        df.groupby(category_column)[numeric_column]
        .mean()
        .sort_values(ascending=ascending)
        .index
    )

    # Convertir a categoría ordenada
    df[category_column] = pd.Categorical(
        df[category_column],
        categories=category_order,
        ordered=True
    )

    num_categories = (
        df[category_column]
        .nunique()
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

    df.boxplot(
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
# GRÁFICO DE CONCEPCIONES POR SEMANA DEL AÑO
# ==========================================================


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

    figure, axis = plt.subplots(
        figsize=(16, 7)
    )

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

        axis.plot(
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

        axis.axvspan(
            period["start"],
            period["end"],
            color=period["color"],
            alpha=0.15,
            label=period["label"]
        )

    # ==========================
    # Configuración gráfica
    # ==========================

    axis.set_title(
        "Concepciones estimadas "
        "por semana del año"
    )

    axis.set_xlabel(
        "Semana"
    )

    axis.set_ylabel(
        "Cantidad de concepciones"
    )

    axis.set_xticks(
        range(1, 54, 2)
    )

    axis.grid(
        True,
        alpha=0.3
    )

    axis.legend(
        title="Año",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    figure.tight_layout()

    save_figure(
        figure,
        "concepciones_por_semana.png"
    )




