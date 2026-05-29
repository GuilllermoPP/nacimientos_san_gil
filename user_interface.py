import pandas as pd

PATIENTS_DATA_FILENAME = 'patients_data.csv'

DATE_COLUMNS = ['assessment_date', 'birth_date']

TEXT_COLUMNS = {'patient_id': 'string',
                'country': 'string',
                'biological_sex': 'string',
                'education_level': 'string',
                'urban_rural': 'string',
                'diabetes_type': 'string',
                'smoker': 'string',
                'physical_activity_level': 'string',
                'medication': 'string',
                'history_of_infarction': 'string',
                }

MISSING_VALUES = ["", "NA", "N/A",
                  'Unknown', 'not recorded']

patients = pd.read_csv(
    PATIENTS_DATA_FILENAME,
    parse_dates=DATE_COLUMNS,
    dtype=TEXT_COLUMNS,
    na_values=MISSING_VALUES
)

SEX_MAPPING = {
    "XX": "XX",
    "XY": "XY",
    "FEMALE": "XX",
    "F": "XX",
    "WOMAN": "XX",
    "MUJER": "XX",
    "X X": "XX",
    "MALE": "XY",
    "M": "XY",
    "MAN": "XY",
    "HOMBRE": "XY",
    "X-Y": "XY",
}

URBAN_RURAL_MAPPING = {
    "URBANO": "URBAN",
    "R": "RURAL",
    "U": "URBAN",
}

EDUCATION_MAPPING = {
    "university": "Undergraduate",
    "technical": "Technical",
    "Secundary": "Secondary",
    "Under graduate": "Undergraduate",
    "Tecnico": "Technical",
    "primary": "Primary",
    "Postgraduate": "Graduate",
    "Primaria": "Primary",
    "Grad": "Graduate",
    "SECONDARY": "Secondary",
}



patients['biological_sex'] = patients['biological_sex'].str.strip().str.upper().replace(SEX_MAPPING)
patients['urban_rural'] = patients['urban_rural'].str.strip().str.upper().replace(URBAN_RURAL_MAPPING)
patients['education_level'] = patients['education_level'].str.strip().str.upper().replace(EDUCATION_MAPPING)

print(patients['biological_sex'].value_counts(dropna=False))
print(patients['urban_rural'].value_counts(dropna=False))
print(patients['education_level'].value_counts(dropna=False))


print(patients.info())

height_mask = patients['height_m'] > 3
patients.loc[height_mask, 'height_m'] = patients.loc[height_mask, 'height_m'] / 100
print(patients['height_m'].describe().round(2))

implausible_weight_mask = (patients['weight_kg'] < 40) | (patients['weight_kg'] > 160)
implausible_waist_mask = patients['waist_circumference_cm'] > 200
patients = patients[~implausible_weight_mask & ~implausible_waist_mask].copy()

print(patients.shape)


heart_rate_mask = (patients['heart_rate_bpm'] < 40) | (patients['heart_rate_bpm'] > 110)
print(patients['heart_rate_bpm'].describe().round(2))
patients = patients[~heart_rate_mask].copy()

print(patients.shape)


total_colesterol_mask = (patients['total_cholesterol_mgdl'] < 50) | (patients['total_cholesterol_mgdl'] > 500)
print(patients['total_cholesterol_mgdl'].describe().round(2))
patients = patients[~total_colesterol_mask].copy()

print(patients.shape)


body_temperature_mask = (patients['body_temperature_c'] < 35) | (patients['body_temperature_c'] > 42)
print(patients['body_temperature_c'].describe().round(2))
patients = patients[~body_temperature_mask].copy()

print(patients.shape)

null_counts = patients.isna().sum()
print(null_counts[null_counts > 0])

patients = patients.dropna(subset=['biological_sex', 'urban_rural', 'education_level', 'smoker'])
print(patients.shape)

NUMERIC_COLUMNS_TO_IMPUTE = [
    'height_m', 'weight_kg', 'waist_circumference_cm', 'heart_rate_bpm',
    'total_cholesterol_mgdl', 'fasting_glucose_mgdl', 'body_temperature_c',
    'systolic_pressure', 'diastolic_pressure'
]

for column in NUMERIC_COLUMNS_TO_IMPUTE:
    patients[f"{column}_imputed"] = patients[column].isna()
    patients[column] = patients[column].fillna(patients[column].median())

imputed_flags = [f"{c}_imputed" for c in NUMERIC_COLUMNS_TO_IMPUTE]
print(patients[imputed_flags].sum())
print(patients[NUMERIC_COLUMNS_TO_IMPUTE].isna().sum().sum())

CLEAN_DATA_FILENAME = 'patients_data_clean.csv'

patients.to_csv(CLEAN_DATA_FILENAME, index=False)
print(f"Cleaned data saved to {CLEAN_DATA_FILENAME}")
print(f"Final shape: {patients.shape}")
print(f"Total missing values: {patients.isna().sum().sum()}")

patients["bmi"] = patients["weight_kg"] / (patients["height_m"] ** 2).round(2)

print(patients[["patient_id", "height_m", "weight_kg", "bmi"]].head())

BMI_BINS = [0, 18.5, 25.0, 30.0, float('inf')]
BMI_LABELS = ['Underweight', 'Normal', 'Overweight', 'Obese']

patients["weight_level"] = pd.cut(patients["bmi"],
                                        bins=BMI_BINS,
                                        labels=BMI_LABELS,
                                        right=False)
print(patients["weight_level"].value_counts())

patients["pulse_pressure"] = patients['systolic_pressure'] - patients['diastolic_pressure']
print(patients['pulse_pressure'].value_counts())

patients['glucose_level'] = pd.cut(patients['fasting_glucose_mgdl'],
                                    bins=[0, 100, 125, float('inf')],
                                    labels=['Normal', 'Prediabetes', 'Diabetes'],
                                    right=False)
print(patients['glucose_level'].value_counts())

patients['arterial_pressure_category'] = pd.cut(patients['systolic_pressure'],
                                                bins=[0, 120, 130, 140, float('inf')],
                                                labels=['Normal', 'Elevated', 'Hypertension Stage 1', 'Hypertension Stage 2'],
                                                right=False)
print(patients['arterial_pressure_category'].value_counts())

patients['age_group'] =pd.cut(
                               bins=[0, 30, 45, 60, float('inf')],
                               labels=['Young Adult', 'Adult', 'Middle-aged', 'Older Adult'],
                               right=False)
print(patients['age_group'].value_counts())
