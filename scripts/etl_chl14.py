# ETL para Región de Los Ríos (CHL14)
# Basado en buenas prácticas de ETL (Celan, Data Science Handbook)
# Solo se consideran datos de CHL14 (Región de Los Ríos)

import pandas as pd

# Cargar datos originales
input_path = '../data/INF_OI_12082025234959741.csv'
df = pd.read_csv(input_path)

# Filtrar solo Región de Los Ríos (CHL14)
df_clean = df[df['DTI_CL_REGION'] == 'CHL14']

# Limpiar columnas innecesarias (opcional, según análisis)
columns_to_keep = [
    'DTI_CL_INDICADOR', 'Indicador', 'DTI_CL_TRIMESTRE_MOVIL', 'Trimestre Móvil',
    'DTI_CL_REGION', 'Región', 'DTI_CL_SEXO', 'Sexo', 'Value', 'Flag Codes', 'Flags'
]
df_clean = df_clean[columns_to_keep]

# Guardar datos limpios
output_path = '../data_clean/INF_OI_CHL14_clean.csv'
df_clean.to_csv(output_path, index=False)

print(f'Datos limpios guardados en {output_path}')
