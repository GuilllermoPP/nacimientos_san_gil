# ==========================================================
# USO de la logica de generación de gráficos para visualizar los datos limpios
# ==========================================================

from graphs_generator import *
from dataset_cleaning import *


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


    generate_scatter_plot(
        borns,
        x_column="Tiempo_Gestación",
        y_column="INDICE_PONDERAL",
        title="Tiempo de Gestación vs IP"
    )

    generate_grouped_scatter_plot(
        borns,
        x_column="Tiempo_Gestación",
        y_column="Peso",
        category_column="RANGO_EDAD_MATERNA",
        title="Tiempo de Gestación vs Peso por Rango edad materna"
    )

    generate_grouped_scatter_plot(
        borns,
        x_column="Tiempo_Gestación",
        y_column="INDICE_PONDERAL",
        category_column="RANGO_EDAD_MATERNA",
        title="Tiempo de Gestación vs IP por Rango edad materna"
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
        category_column="EPS_NORMALIZADA",
        title="EPS y controles prenatales",
        ascending=True
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
    
    title="Distribución porcentual del índice ponderal por edad materna",
    normalize=True
    )

    generate_conception_pattern_graph(
        dataframe=borns
        )