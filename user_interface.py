import pandas as pd

BORN_LIVE_FILE = "nacidos_vivos.csv"

# Definimos las columnas de texto para que pandas las lea como string, ya que por defecto las lee como object, lo que puede generar problemas al momento de hacer
# análisis de datos.

TEXT_COLUMNS = {'Departamento Nacimiento': 'string',
                'Municipio': 'string',
                'Area': 'string',
                'Sexo': 'string',
                'Tiempo_Gestación': 'string',
                'Tipo_Parto': 'string',
                'Multiplicidad_Embarazo': 'string',
                'Régimen_Seguridad_Social': 'string',
                'EPS': 'string',
}


# Definimos las columnas de fecha para que pandas las parseé como fecha, lo que nos permitirá hacer análisis de datos relacionados con el tiempo.

PARSE_DATE_COLUMNS = ['Fecha_Nacimiento']

# Leemos el archivo CSV, especificando que la columna "Fecha_Nacimiento" debe ser parseada como fecha y las columnas de texto deben ser leídas como string.

borns=pd.read_csv(
    BORN_LIVE_FILE,
    parse_dates=PARSE_DATE_COLUMNS,
    dtype=TEXT_COLUMNS,
)

## Hacemos limpieza de datos, reemplazando los valores de peso y periodo, para convertirlos a tipo numérico. En el caso de peso, reemplazamos la coma por un punto
## y en el caso de periodo, eliminamos la coma. Luego convertimos ambos a tipo numérico.

borns["Peso"] = borns["Peso"].str.replace(',', '.').astype("float64")
borns["Periodo"] = borns["Periodo"].str.replace(',', '').astype("int64")

print(borns.info())
# print(borns['Peso'].value_counts())
# print(borns['Periodo'].value_counts())
# print(borns['Fecha_Nacimiento'].value_counts())
print(borns['Hora_Nacimiento'].value_counts())