import pandas as pd
import os
import matplotlib.pyplot as plt

#solana

BORN_LIVE_FILE = "nacidos_vivos.csv"

# Gestion de errores realizada con apoyo de chatGPT

def load_dataset(file_path):
    try:
        return pd.read_csv(
            file_path,
            parse_dates=PARSE_DATE_COLUMNS,
            dtype=TEXT_COLUMNS
        )
# luisvilla

    except FileNotFoundError:
        raise FileNotFoundError(
            f"No existe el archivo: {file_path}"
        )

    except pd.errors.ParserError:
        raise ValueError(
            "El archivo no tiene un formato CSV válido"
        )


def validate_structure(df, required_columns):
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Columnas faltantes: {sorted(missing)}"
        )
    
    #Edward Perea
    

# Definimos las columnas de texto para que pandas las lea como string, ya que por defecto las lee como object, lo que puede generar problemas al momento de hacer
# análisis de datos.
EPS_MAPPING = {
    'A.R.S. CONVIDA': 'CONVIDA',
    
    'ASMET SALUD EPS SAS': 'ASMET SALUD',
    
    'ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD E.S.S': 'MUTUAL SER',
    
    'CAJA DE COMPENSACION FAMILIAR  CAJACOPI ATLANTICO': 'CAJACOPI',
    
    'CAPITAL SALUD E.P.S.': 'CAPITAL SALUD',
    
    'COMFAORIENTE': 'COMFAORIENTE',
    
    'COOSALUD -CM': 'COOSALUD',
    'COOSALUD E.S.S.': 'COOSALUD',
    'COOSALUD E.S.S. -CM': 'COOSALUD',
    'COOSALUD ENTIDAD PROMOTORA DE SALUD S.A.': 'COOSALUD',
    
    'E.P.S. SANITAS': 'SANITAS',
    'EPS SANITAS - CM': 'SANITAS',
    
    'EMPRESA PROMOTORA DE SALUD ECOOPSOS EPS S.A.S.':'ECOOPSOS',
    
    'EPS Y MEDICINA PREPAGADA SURAMERICANA S.A': 'SURAMERICANA',
    
    'FAMISANAR E.P.S. LTDA - CAFAM - COLSUBSIDIO': 'COLSUBSIDIO',
    
    'FAMISANAR E.P.S. LTDA - CAFAM - COLSUBSIDIO -CM': 'COLSUBSIDIO',
    
    'FUERZAS MILITARES': 'FUERZAS MILITARES',
    
    'FUNDACION SALUD MIA EPS': 'SALUD MIA',
    
    'MAGISTERIO': 'MAGISTERIO',
    
    'NO ASEGURADO': 'NO ASEGURADO',
    
    'NUEVA EPS S.A.': 'NUEVA EPS',
    'NUEVA EPS S.A. -CM': 'NUEVA EPS',
    
    'POLICIA NACIONAL': 'POLICIA NACIONAL',
    
    'SALUD TOTAL E.P.S. -CM': 'SALUD TOTAL',
    'SALUD TOTAL S.A.': 'SALUD TOTAL'
}



REQUIRED_COLUMNS = {
    'Fecha_Nacimiento',
    'Departamento Nacimiento',
    'Municipio',
    'Area',
    'Sexo',
    'Tiempo_Gestación',
    'Tipo_Parto',
    'Multiplicidad_Embarazo',
    'Régimen_Seguridad_Social',
    'EPS',
    'Peso',
    'Periodo'
}

TEXT_COLUMNS = {'Departamento Nacimiento': 'string',
                'Municipio': 'string',
                'Area': 'string',
                'Sexo': 'string',

                'Tipo_Parto': 'string',
                'Multiplicidad_Embarazo': 'string',
                'Régimen_Seguridad_Social': 'string',
                'EPS': 'string',
}


# Definimos las columnas de fecha para que pandas las parseé como fecha, lo que nos permitirá hacer análisis de datos relacionados con el tiempo.

PARSE_DATE_COLUMNS = ['Fecha_Nacimiento']

# Leemos el archivo CSV, especificando que la columna "Fecha_Nacimiento" debe ser parseada como fecha y las columnas de texto deben ser leídas como string.

try:
    borns = load_dataset(BORN_LIVE_FILE)
    validate_structure(borns, REQUIRED_COLUMNS)

    print("Dataset cargado correctamente")

except Exception as e:
    print(f"Proceso detenido: {e}")

## Hacemos limpieza de datos, reemplazando los valores de peso y periodo, para convertirlos a tipo numérico. En el caso de peso, reemplazamos la coma por un punto
## y en el caso de periodo, eliminamos la coma. Luego convertimos ambos a tipo numérico.

borns["Peso"] = borns["Peso"].str.replace(',', '.').astype("float64")
borns["Periodo"] = borns["Periodo"].str.replace(',', '').astype("int64")
borns["EPS_NORMALIZADA"] = borns["EPS"].replace(EPS_MAPPING)

print(borns['Peso'].value_counts())
# Columnas derivadas_______________________________________________________________
BIN_MATERNAL_AGE=[0, 20, 35, float('inf')]
LABELS_MATERNAL_AGE=[
        "Adolescente",
        "Edad reproductiva óptima",
        "Edad materna avanzada"
    ]
borns["RANGO_EDAD_MATERNA"] = pd.cut(
    borns["Edad_Madre"],
    bins=BIN_MATERNAL_AGE,
    labels=LABELS_MATERNAL_AGE,
    right=False
)

BINS_GESTATIONAL_AGE_GROUP=[0, 28, 32, 37, 42, float('inf')]
LABELS_GESTATIONAL_AGE_GROUP=[
        'Prematuro extremo',
        'Muy prematuro',
        'Prematuro moderado a tardío',
        'A término',
        'Postérmino'
    ]

borns['grupo_edad_gestacional'] = pd.cut(
    borns['Tiempo_Gestación'],
    bins=BINS_GESTATIONAL_AGE_GROUP,
    labels=LABELS_GESTATIONAL_AGE_GROUP,
    right=False
)



# #Calculo de la fecha de fecundacion o engendramiento estimada sugerida por chat GPT la diferencia de 
borns["FECHA_CONCEPCION_ESTIMADA"] = (
    borns["Fecha_Nacimiento"]
    - pd.to_timedelta(borns["Tiempo_Gestación"] * 7, unit="D", errors="coerce")
    + pd.Timedelta(days=14)
)

borns['anio_concepcion'] = borns['FECHA_CONCEPCION_ESTIMADA'].dt.isocalendar().year
borns['semana_concepcion'] = borns['FECHA_CONCEPCION_ESTIMADA'].dt.isocalendar().week

patron_semanal = (
    borns.groupby(['anio_concepcion', 'semana_concepcion'])
         .size()
         .reset_index(name='cantidad')
)




def generar_scatter_df(
    df,
    columna_x,
    columna_y,
    ruta_archivo,
    titulo=None
):
    fig, ax = plt.subplots()

    ax.scatter(df[columna_x], df[columna_y])

    ax.set_xlabel(columna_x)
    ax.set_ylabel(columna_y)

    if titulo:
        ax.set_title(titulo)

    fig.savefig(ruta_archivo, dpi=300, bbox_inches="tight")
    plt.close(fig)

generar_scatter_df(
    df=borns,
    columna_x="Tiempo_Gestación",
    columna_y="Peso",
    ruta_archivo="Graficas"+"/scatter_gestacion_peso.png",
    titulo="Tiempo de Gestación vs Peso"
)


# plt.figure(figsize=(16, 7))

# for anio in sorted(patron_semanal['anio_concepcion'].unique()):
#     datos = patron_semanal[
#         patron_semanal['anio_concepcion'] == anio
#     ].sort_values('semana_concepcion')

#     plt.plot(
#         datos['semana_concepcion'],
#         datos['cantidad'],
#         marker='o',
#         label=str(anio)
#     )

# # Navidad y Año Nuevo
# plt.axvspan(51, 53, alpha=0.15, label='Navidad-Año Nuevo')
# plt.axvspan(1, 2, alpha=0.15)

# # Semana Santa (aproximada)
# plt.axvspan(12, 16, alpha=0.15, label='Semana Santa')

# # Vacaciones mitad de año
# plt.axvspan(24, 29, alpha=0.15, label='Vacaciones mitad de año')

# # Ferias y Fiestas de San Gil
# plt.axvspan(44, 45, alpha=0.15, label='Ferias San Gil')


# plt.title('Concepciones estimadas por semana del año')
# plt.xlabel('Semana')
# plt.ylabel('Cantidad de concepciones')
# plt.xticks(range(1, 54, 2))
# plt.grid(True, alpha=0.3)
# plt.legend(title='Año')
# plt.show()

print(borns.info())
borns.to_csv("nacidos_vivos_limpio.csv", index=False, encoding="utf-8-sig")
# print(borns['Peso'].value_counts())
# print(borns['Periodo'].value_counts())
#print(borns['EPS'].unique())
print(borns['Talla'].value_counts())