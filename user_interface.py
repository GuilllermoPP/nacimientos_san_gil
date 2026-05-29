import pandas as pd

BORN_LIVE_FILE = "nacidos_vivos.csv"

# Definimos las columnas de texto para que pandas las lea como string, ya que por defecto las lee como object, lo que puede generar problemas al momento de hacer
# análisis de datos.
EPS_MAPPING = {
    'A.R.S. CONVIDA': 'CONVIDA',
    
    'ASMET SALUD EPS SAS': 'ASMET SALUD',
    
    'ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD E.S.S':
        'MUTUAL SER',
    
    'CAJA DE COMPENSACION FAMILIAR  CAJACOPI ATLANTICO':
        'CAJACOPI',
    
    'CAPITAL SALUD E.P.S.': 'CAPITAL SALUD',
    
    'COMFAORIENTE': 'COMFAORIENTE',
    
    'COOSALUD -CM': 'COOSALUD',
    'COOSALUD E.S.S.': 'COOSALUD',
    'COOSALUD E.S.S. -CM': 'COOSALUD',
    'COOSALUD ENTIDAD PROMOTORA DE SALUD S.A.': 'COOSALUD',
    
    'E.P.S. SANITAS': 'SANITAS',
    'EPS SANITAS - CM': 'SANITAS',
    
    'EMPRESA PROMOTORA DE SALUD ECOOPSOS EPS S.A.S.':
        'ECOOPSOS',
    
    'EPS Y MEDICINA PREPAGADA SURAMERICANA S.A':
        'SURAMERICANA',
    
    'FAMISANAR E.P.S. LTDA - CAFAM - COLSUBSIDIO':
        'COLSUBSIDIO',
    
    'FAMISANAR E.P.S. LTDA - CAFAM - COLSUBSIDIO -CM':
        'COLSUBSIDIO',
    
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
borns['EPS_NORMALIZADA'] = borns['EPS'].replace(EPS_MAPPING)



print(borns.info())
# print(borns['Peso'].value_counts())
# print(borns['Periodo'].value_counts())
#print(borns['EPS'].unique())
print(borns['Talla'].value_counts())